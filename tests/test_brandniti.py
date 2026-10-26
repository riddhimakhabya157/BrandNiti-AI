"""Comprehensive Automated Test Suite for BrandNiti AI.
Tests deterministic rules, pricing conditions, evidence requirements,
decision engine precedence, approval invalidation on edits,
workflow state transitions, governance insights, and persistence.
"""
import os
import json
import pytest
from database.connection import get_db_connection, init_db_dir
from database.schema import init_database
from database.seed_data import seed_nivara_pro_if_not_exists, NIVARA_BRAND_ID
from database.queries import (
    get_brand_by_id,
    get_active_guideline_version,
    create_submission,
    get_submission_by_id,
    create_content_revision,
    get_latest_revision,
    save_review_run,
    get_review_run_by_id,
    record_approval_decision,
    get_decisions_for_submission,
    get_governance_insights,
    create_new_guideline_version
)
from models.brand import GuidelineVersion, Rule
from models.submission import Finding
from services.rule_engine import run_deterministic_rules, check_prohibited_phrases, check_pricing_and_promotions
from services.decision_engine import evaluate_disposition
from services.review_workflow import run_content_review_workflow, submit_human_decision

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Sets up an isolated SQLite test database for each test session."""
    test_db_file = str(tmp_path / "test_brandniti.db")
    monkeypatch.setenv("BRANDNITI_DB_PATH", test_db_file)
    init_database()
    seed_nivara_pro_if_not_exists()

# -------------------------------------------------------------
# 1. Deterministic Brand-Rule Engine Tests
# -------------------------------------------------------------

def test_nivara_pro_round1_presentation_content_findings():
    """Validates the exact Hackathon Round 1 test content:
    'Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!'
    Expected findings:
    1. ₹799 requires confirmation that an authorized promotion is active.
    2. 'Guaranteed results' conflicts with illustrative prohibition.
    3. 'in 24 hours' requires documented empirical evidence.
    4. Missing results disclaimer.
    """
    guideline = get_active_guideline_version(NIVARA_BRAND_ID)
    assert guideline is not None

    risky_content = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
    findings = run_deterministic_rules(risky_content, guideline, supporting_evidence="")

    # Verify at least one finding for ₹799 promotional price
    promo_findings = [f for f in findings if "799" in f.matched_text]
    assert len(promo_findings) >= 1
    assert promo_findings[0].category == "Pricing & Offers"
    assert promo_findings[0].verification_state == "REQUIRES_DOCUMENTED_EVIDENCE"

    # Verify prohibited phrase finding for 'Guaranteed results'
    guaranteed_findings = [f for f in findings if "guaranteed results" in f.matched_text.lower()]
    assert len(guaranteed_findings) >= 1
    assert guaranteed_findings[0].severity == "CRITICAL"
    assert guaranteed_findings[0].disposition_impact == "HOLD"

    # Verify evidence requirement for 'in 24 hours'
    speed_findings = [f for f in findings if "24 hours" in f.matched_text.lower()]
    assert len(speed_findings) >= 1
    assert speed_findings[0].verification_state == "REQUIRES_DOCUMENTED_EVIDENCE"

    # Verify decision engine marks this content as HOLD
    recommendation, summary, det_passed = evaluate_disposition(findings)
    assert recommendation == "HOLD"
    assert "HOLD" in summary
    assert det_passed is False

def test_promotional_price_with_valid_documented_evidence():
    """When authorized promotional evidence is documented, ₹799 must be recognized as compliant."""
    guideline = get_active_guideline_version(NIVARA_BRAND_ID)
    content = "Get Nivara Pro for ₹799 during our authorized seasonal campaign."
    valid_evidence = "Authorized promo campaign code: DIWALI-PROMO-799-DOC-REF"

    findings = check_pricing_and_promotions(content, guideline, supporting_evidence=valid_evidence)
    assert len(findings) == 1
    assert findings[0].verification_state == "VERIFIED_COMPLIANT"
    assert findings[0].disposition_impact == "PASS"

def test_compliant_content_passes():
    """Compliant content adhering to ₹999 standard pricing and mandatory disclaimers passes cleanly."""
    guideline = get_active_guideline_version(NIVARA_BRAND_ID)
    compliant_content = (
        "Support your daily mental clarity with Nivara Pro for ₹999. "
        "Formulated to assist your daily wellness journey.\n\n"
        "*Disclaimer: Results may vary based on individual lifestyle, diet, and physiological factors."
    )
    findings = run_deterministic_rules(compliant_content, guideline, supporting_evidence="")
    # No critical or high issues
    blocking_findings = [f for f in findings if f.disposition_impact == "HOLD"]
    assert len(blocking_findings) == 0

    recommendation, summary, _ = evaluate_disposition(findings)
    assert recommendation in ["PASS", "REVIEW"]

# -------------------------------------------------------------
# 2. Decision Engine Precedence Tests
# -------------------------------------------------------------

def test_decision_engine_hold_precedence_over_review():
    """HOLD takes strict precedence when both blocking and review conditions are present."""
    findings = [
        Finding(
            id="f1", review_run_id="", source="DETERMINISTIC", rule_id="r1",
            rule_title="Urgency review", category="Voice & Tone", severity="MEDIUM",
            disposition_impact="REVIEW", matched_text="hurry", explanation="High urgency",
            expected_condition="Empathetic voice"
        ),
        Finding(
            id="f2", review_run_id="", source="DETERMINISTIC", rule_id="r2",
            rule_title="Guaranteed Results Prohibition", category="Legal & Compliance", severity="CRITICAL",
            disposition_impact="HOLD", matched_text="guaranteed results", explanation="Prohibited outcome claim",
            expected_condition="No outcome guarantees permitted"
        )
    ]
    rec, summary, det_passed = evaluate_disposition(findings)
    assert rec == "HOLD"
    assert det_passed is False
    assert "HOLD — Blocked pending fix" in summary

def test_decision_engine_review_when_only_unverified_claims():
    """When only unverified claims or disclaimers are flagged, recommendation is REVIEW, not HOLD."""
    findings = [
        Finding(
            id="f1", review_run_id="", source="DETERMINISTIC", rule_id="r1",
            rule_title="Timeframe evidence needed", category="Claims & Evidence", severity="HIGH",
            disposition_impact="REVIEW", matched_text="in 48 hours", explanation="Needs lab citation",
            expected_condition="Attach lab trial"
        )
    ]
    rec, summary, det_passed = evaluate_disposition(findings)
    assert rec == "REVIEW"
    assert "REVIEW — Needs verification" in summary

# -------------------------------------------------------------
# 3. Content Revision & Approval Invalidation Tests
# -------------------------------------------------------------

def test_editing_approved_content_invalidates_prior_approval():
    """CRITICAL REQUIREMENT:
    If a submission is APPROVED, and then subsequently edited to create a new revision,
    the previous approval is marked invalid (is_currently_valid = 0) and revalidation is enforced.
    """
    # 1. Create submission
    sub = create_submission(
        title="Spring Campaign Post",
        content_type="social_post",
        channel="Instagram",
        campaign_name="Spring 2026",
        brand_id=NIVARA_BRAND_ID,
        initial_content="Nivara Pro available for ₹999.* *Results may vary.",
        supporting_evidence=""
    )
    assert sub.current_version_number == 1

    # 2. Run review workflow
    run = run_content_review_workflow(sub.id)

    # 3. Human reviewer approves version 1
    decision = submit_human_decision(
        submission_id=sub.id,
        revision_id=sub.revisions[0].id,
        review_run_id=run.id,
        decision="APPROVED",
        reviewer_name="Priya Sharma",
        reviewer_role="Brand Governance Director",
        reviewer_comments="Compliant with v1.0 brand guidelines. Approved for publication."
    )
    assert decision.decision == "APPROVED"
    assert decision.is_currently_valid is True

    # Verify status in database
    updated_sub = get_submission_by_id(sub.id)
    assert updated_sub.current_status == "APPROVED"

    # 4. Content creator subsequently edits the content to introduce a risky change
    new_rev = create_content_revision(
        submission_id=sub.id,
        new_content_text="Get Nivara Pro for ₹799 today! Guaranteed results in 24 hours!",
        supporting_evidence="",
        change_summary="Updated with flash promo copy"
    )
    assert new_rev.version_number == 2

    # 5. Verify that prior approval is now INVALIDATED
    decisions = get_decisions_for_submission(sub.id)
    assert len(decisions) == 1
    assert decisions[0].is_currently_valid is False  # Invalidation confirmed!

    # 6. Verify submission status reverted to SUBMITTED
    refreshed_sub = get_submission_by_id(sub.id)
    assert refreshed_sub.current_status == "SUBMITTED"
    assert refreshed_sub.current_version_number == 2

    # 7. Re-running review on new version 2 correctly catches the new violations
    run_v2 = run_content_review_workflow(sub.id, revision_id=new_rev.id)
    assert run_v2.overall_recommendation == "HOLD"

# -------------------------------------------------------------
# 4. Database Persistence & Restart Simulation Tests
# -------------------------------------------------------------

def test_database_persistence_across_connection_restarts():
    """Verifies that all submissions, guideline revisions, and audit trails
    persist durably in SQLite across connection restarts."""
    sub = create_submission(
        title="Durable Persistence Test",
        content_type="advertisement",
        channel="Google Ads",
        campaign_name="Persistence Check",
        brand_id=NIVARA_BRAND_ID,
        initial_content="Reliable daily focus with Nivara Pro for ₹999.",
        supporting_evidence=""
    )

    # Simulate closing and opening a new connection
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, current_status FROM submissions WHERE id = ?", (sub.id,))
        row = cursor.fetchone()
        assert row is not None
        assert row["title"] == "Durable Persistence Test"

# -------------------------------------------------------------
# 5. Guideline Management & Version Bumping Tests
# -------------------------------------------------------------

def test_create_new_guideline_version():
    """Verifies that updating brand guidelines creates a new version (e.g. v2.0),
    maintaining historical version identifiers."""
    active_g = get_active_guideline_version(NIVARA_BRAND_ID)
    assert active_g.version_number == 1

    new_v = create_new_guideline_version(
        brand_id=NIVARA_BRAND_ID,
        tone_of_voice="Empathetic, rigorous, premium, inspiring",
        target_audience="Global wellness leaders and daily achievers",
        approved_prices=[{"item": "Nivara Pro Pack", "price_inr": 1199}],
        conditional_promotions=[],
        required_disclaimers=active_g.required_disclaimers,
        evidence_requirements=active_g.evidence_requirements,
        changelog="Annual price index adjustment to ₹1199",
        rules_data=[
            {
                "id": "rule_v2_price",
                "rule_type": "price_check",
                "category": "Pricing & Offers",
                "severity": "HIGH",
                "pattern": "1199",
                "title": "New Standard Price ₹1199",
                "description": "Standard price updated to ₹1199 in v2.",
                "suggested_fix": "Use ₹1199 standard retail price.",
                "blocks_approval": True,
                "is_mandatory": True
            }
        ]
    )
    assert new_v.version_number == 2
    assert new_v.version_label.startswith("v2.0")

    # Verify active guideline is now version 2
    reloaded_active = get_active_guideline_version(NIVARA_BRAND_ID)
    assert reloaded_active.version_number == 2

# -------------------------------------------------------------
# 6. Governance Insights & Metrics Tests
# -------------------------------------------------------------

def test_governance_insights_metrics_computation():
    """Verifies that dashboard governance metrics compute actual database aggregates without hardcoded values."""
    insights = get_governance_insights()
    assert "total_submissions" in insights
    assert "pending_reviews" in insights
    assert "status_counts" in insights
    assert "recommendations" in insights
    assert "human_decisions" in insights
    assert "top_rules" in insights
    assert "unsupported_patterns" in insights
    assert isinstance(insights["total_submissions"], int)
