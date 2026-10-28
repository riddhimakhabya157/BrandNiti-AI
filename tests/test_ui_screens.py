"""Automated tests for BrandNiti AI UI redesign, color tokens, and screen components."""
import re
import pytest
from styles.theme import (
    CUSTOM_CSS,
    render_header,
    render_stepper,
    render_disposition_badge,
    render_status_badge,
    render_divider,
    render_empty_state_html,
    render_severity_badge,
    render_metric_card_html
)


def test_color_tokens_in_theme():
    """Verify that all required design color tokens exist in CUSTOM_CSS."""
    required_tokens = [
        "#F8FAFC",  # Main background
        "#FFFFFF",  # Cards and panels
        "#166534",  # Primary green
        "#14532D",  # Dark green headings
        "#DCFCE7",  # Light green surfaces
        "#0F172A",  # Primary text
        "#64748B",  # Secondary text
        "#E2E8F0",  # Borders
        "#DC2626",  # Critical/HOLD red
        "#FEE2E2",  # Light red warning surface
        "#A16207",  # REVIEW amber
        "#FEF3C7",  # Light amber surface
    ]
    for token in required_tokens:
        assert token.lower() in CUSTOM_CSS.lower(), f"Missing color token {token} in CUSTOM_CSS"


def test_disposition_badges_styling_and_labels():
    """Verify PASS, REVIEW, and HOLD disposition badges use proper colors, text, and icons."""
    pass_html = render_disposition_badge("PASS")
    assert "✔ PASS — Compliant" in pass_html
    assert "bn-badge-pass" in pass_html

    review_html = render_disposition_badge("REVIEW")
    assert "⚠ REVIEW — Verification Required" in review_html
    assert "bn-badge-review" in review_html

    hold_html = render_disposition_badge("HOLD")
    assert "✖ HOLD — Policy Blocked" in hold_html
    assert "bn-badge-hold" in hold_html


def test_status_badges_labels():
    """Verify workflow status badges render with proper labels and icons."""
    app_html = render_status_badge("APPROVED")
    assert "✔ APPROVED" in app_html
    assert "bn-status-approved" in app_html

    chg_html = render_status_badge("CHANGES_REQUESTED")
    assert "✎ CHANGES REQUESTED" in chg_html
    assert "bn-status-changes" in chg_html

    rej_html = render_status_badge("REJECTED")
    assert "✖ REJECTED" in rej_html
    assert "bn-status-rejected" in rej_html


def test_empty_state_clean_markup():
    """Verify empty states produce clean HTML with zero 4-space indentations."""
    empty_html = render_empty_state_html("🔍", "No Items Found", "Please adjust your filter.")
    assert "bn-empty-state" in empty_html
    assert "No Items Found" in empty_html
    for line in empty_html.splitlines():
        assert not line.startswith("    "), f"Found 4 leading spaces in line: {line}"


def test_metric_card_clean_markup():
    """Verify metric cards produce clean HTML without markdown-breaking indentation."""
    metric_html = render_metric_card_html("Total Submissions", 42, "All-time assets", "#166534")
    assert "Total Submissions" in metric_html
    assert "42" in metric_html
    for line in metric_html.splitlines():
        assert not line.startswith("    "), f"Found 4 leading spaces in line: {line}"


def test_app_py_screen_sections_exist():
    """Verify that all six requested screens exist in app.py."""
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()

    expected_screens = [
        'st.session_state["active_tab"] == "Overview"',
        'st.session_state["active_tab"] == "New Content Review"',
        'st.session_state["active_tab"] == "Review Queue"',
        'st.session_state["active_tab"] == "Brand Guidelines"',
        'st.session_state["active_tab"] == "Insights"',
        'st.session_state["active_tab"] == "Review History"',
    ]
    for screen_check in expected_screens:
        assert screen_check in content, f"Screen condition missing: {screen_check}"
