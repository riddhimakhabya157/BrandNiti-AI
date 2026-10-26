"""Tests for New Content Review stepper rendering and state persistence."""
from styles.theme import render_stepper
import streamlit as st


def test_render_stepper_zero_indentation_and_clean_markup():
    """Verify stepper HTML contains zero 4-space indented lines and renders all 4 steps without duplicate numbering."""
    captured_html = []

    def mock_markdown(body, unsafe_allow_html=False):
        captured_html.append(body)

    st.markdown = mock_markdown

    for step in [1, 2, 3, 4]:
        captured_html.clear()
        render_stepper(step)
        assert len(captured_html) == 1
        html = captured_html[0]

        # Verify no 4-space indentation anywhere (which triggers CommonMark pre/code blocks)
        for line in html.splitlines():
            assert not line.startswith("    "), f"Found 4 leading spaces in line: {line}"

        # Verify step labels do not repeat the number (no duplicate numbering)
        assert "1. Content Draft" not in html
        assert "2. Policy Analysis" not in html
        assert "3. Corrections" not in html
        assert "4. Human Decision" not in html

        # Verify clean step labels exist
        assert "Content Draft" in html
        assert "Policy Analysis" in html
        assert "Corrections" in html
        assert "Human Decision" in html

        # Verify stepper container and divider lines exist
        assert '<div class="stepper-container">' in html
        assert 'step-divider-line' in html


def test_render_stepper_active_and_completion_states():
    """Verify active step receives .step-active and preceding steps receive .step-complete."""
    captured_html = []

    def mock_markdown(body, unsafe_allow_html=False):
        captured_html.append(body)

    st.markdown = mock_markdown

    # Test Step 1: Step 1 active, 2/3/4 pending, 0 complete dividers
    captured_html.clear()
    render_stepper(1)
    h1 = captured_html[0]
    assert '<div class="step-circle">1</div>' in h1
    assert 'step-divider-complete' not in h1

    # Test Step 2: Step 1 complete with checkmark, Step 2 active, 1 complete divider
    captured_html.clear()
    render_stepper(2)
    h2 = captured_html[0]
    assert '<div class="step-circle">✔</div>' in h2
    assert '<div class="step-circle">2</div>' in h2
    assert h2.count('step-divider-complete') == 1

    # Test Step 3: Steps 1 & 2 complete, Step 3 active, 2 complete dividers
    captured_html.clear()
    render_stepper(3)
    h3 = captured_html[0]
    assert h3.count('<div class="step-circle">✔</div>') == 2
    assert '<div class="step-circle">3</div>' in h3
    assert h3.count('step-divider-complete') == 2

    # Test Step 4: Steps 1, 2, 3 complete, Step 4 active, 3 complete dividers
    captured_html.clear()
    render_stepper(4)
    h4 = captured_html[0]
    assert h4.count('<div class="step-circle">✔</div>') == 3
    assert '<div class="step-circle">4</div>' in h4
    assert h4.count('step-divider-complete') == 3


def test_stepper_workflow_navigation_and_data_preservation():
    """Verify that moving between all 4 steps preserves draft, findings, corrections, and decision."""
    from database.schema import init_database
    from database.seed_data import seed_nivara_pro_if_not_exists
    from database.queries import (
        get_all_brands,
        create_submission,
        get_submission_by_id,
        create_content_revision,
        get_decisions_for_submission
    )
    from services.review_workflow import run_content_review_workflow, submit_human_decision

    init_database()
    seed_nivara_pro_if_not_exists()

    brands = get_all_brands()
    brand_id = brands[0].id

    # Step 1: Content Draft
    sub = create_submission(
        title="Stepper Test Campaign",
        content_type="advertisement",
        channel="Instagram",
        campaign_name="Diwali Festive Offer",
        brand_id=brand_id,
        initial_content="Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!",
        supporting_evidence="",
        creator="Growth Marketing Team"
    )
    assert sub.id is not None
    assert sub.current_version_number == 1

    # Step 2: Policy Analysis
    run1 = run_content_review_workflow(sub.id)
    assert run1.overall_recommendation in ["REVIEW", "HOLD"]
    assert len(run1.findings) > 0
    assert run1.suggested_revised_copy != ""

    # Step 3: Corrections & Re-audit
    rev2 = create_content_revision(
        submission_id=sub.id,
        new_content_text=run1.suggested_revised_copy,
        supporting_evidence="Authorized Promo Code: FESTIVE-799-AUTH",
        change_summary="Applied recommended pricing and required variation disclaimer",
        actor="Content Creator"
    )
    run2 = run_content_review_workflow(sub.id, revision_id=rev2.id)
    sub_v2 = get_submission_by_id(sub.id)
    assert sub_v2.current_version_number == 2
    assert run2.overall_recommendation == "PASS"

    # Step 4: Human Governance Decision
    dec = submit_human_decision(
        submission_id=sub.id,
        revision_id=rev2.id,
        review_run_id=run2.id,
        decision="APPROVED",
        reviewer_name="Priya Sharma",
        reviewer_role="Brand Governance Director",
        reviewer_comments="Verified against brand guidelines."
    )
    decisions = get_decisions_for_submission(sub.id)
    assert len(decisions) >= 1
    assert decisions[0].decision == "APPROVED"
    assert decisions[0].is_currently_valid == 1

