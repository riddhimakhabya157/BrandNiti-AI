"""BrandNiti AI — Every Brand Message. On Brand.
AI-Powered Brand Governance: Create Confidently. Review Intelligently. Publish Responsibly.

Modern Enterprise SaaS Application with White + Deep Green + Red Visual Identity.
"""
import os
import sys
import textwrap
from pathlib import Path

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = str(Path(__file__).parent.resolve())
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import streamlit as st

from database.schema import init_database
from database.seed_data import seed_nivara_pro_if_not_exists, NIVARA_BRAND_ID
from database.queries import (
    get_all_brands,
    get_brand_by_id,
    get_active_guideline_version,
    get_all_submissions,
    get_submission_by_id,
    create_submission,
    create_content_revision,
    get_latest_revision,
    get_review_runs_for_submission,
    get_latest_review_run_for_submission,
    get_decisions_for_submission,
    get_audit_trail,
    get_governance_insights,
    create_new_guideline_version
)
from services.review_workflow import run_content_review_workflow, submit_human_decision
from services.ai_review import is_ai_available
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

# Helper for strictly unindented HTML rendering (guarantees CommonMark never converts HTML into code blocks)
def render_html(html_str: str):
    """Renders HTML strictly unindented so CommonMark never treats it as a code block."""
    clean_html = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)

def format_utc_timestamp(ts_str: str) -> str:
    """Formats ISO timestamp string into readable UTC timestamp."""
    if not ts_str:
        return "N/A"
    try:
        clean = ts_str.split(".")[0].replace("T", " ")
        if not clean.endswith("UTC"):
            clean += " UTC"
        return clean
    except Exception:
        return ts_str

# Page configuration - Modern enterprise full-width layout with collapsed sidebar
st.set_page_config(
    page_title="BrandNiti AI | Enterprise Brand Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ensure Database & Seed Fixture
init_database()
seed_nivara_pro_if_not_exists()

# Initialize session state for navigation and review stepper
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Overview"

if "review_step" not in st.session_state:
    st.session_state["review_step"] = 1

# Initialize draft inputs in session state to guarantee preservation across reruns and tab switches
if "cr_title" not in st.session_state:
    st.session_state["cr_title"] = "Festival Flash Sale Ad"
if "cr_content" not in st.session_state:
    st.session_state["cr_content"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
if "cr_evidence" not in st.session_state:
    st.session_state["cr_evidence"] = ""
if "cr_channel" not in st.session_state:
    st.session_state["cr_channel"] = "Instagram"
if "cr_type" not in st.session_state:
    st.session_state["cr_type"] = "advertisement"
if "cr_campaign" not in st.session_state:
    st.session_state["cr_campaign"] = "Q4 Festive Launch"
if "cr_creator" not in st.session_state:
    st.session_state["cr_creator"] = "Brand Marketing Lead"
if "cr_sub_id" not in st.session_state:
    st.session_state["cr_sub_id"] = None
if "cr_revised_content" not in st.session_state:
    st.session_state["cr_revised_content"] = ""

# -------------------------------------------------------------
# Top Enterprise Brand Header
# -------------------------------------------------------------
ai_connected = is_ai_available()
render_header(ai_connected=ai_connected)

# -------------------------------------------------------------
# Horizontal Navigation Bar (6 Tabs)
# -------------------------------------------------------------
nav_tabs = [
    ("📊 Overview", "Overview"),
    ("✍️ New Content Review", "New Content Review"),
    ("📋 Review Queue", "Review Queue"),
    ("📖 Brand Guidelines", "Brand Guidelines"),
    ("📈 Insights", "Insights"),
    ("📜 Review History", "Review History"),
]

nav_cols = st.columns(6)
for idx, (tab_label, tab_name) in enumerate(nav_tabs):
    with nav_cols[idx]:
        is_active = (st.session_state["active_tab"] == tab_name)
        btn_type = "primary" if is_active else "secondary"
        if st.button(tab_label, key=f"nav_btn_{tab_name}", type=btn_type, use_container_width=True):
            st.session_state["active_tab"] = tab_name
            st.rerun()

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# =============================================================
# SECTION 1: OVERVIEW (EXECUTIVE GOVERNANCE DASHBOARD)
# =============================================================
if st.session_state["active_tab"] == "Overview":
    # Executive Welcome Hero Panel
    with st.container(border=True):
        col_w1, col_w2 = st.columns([3, 1])
        with col_w1:
            st.markdown(
                """
<div style="padding: 0.35rem 0.2rem;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
        <span style="background: #DCFCE7; color: #166534; font-size: 0.76rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; border: 1px solid #86EFAC;">
            ENTERPRISE PLATFORM
        </span>
        <span style="color: #64748B; font-size: 0.84rem;">Real-time Policy Enforcement</span>
    </div>
    <div style="color: #14532D; font-size: 1.45rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.25; margin-bottom: 6px;">
        AI-Powered Brand Governance & Compliance Dashboard
    </div>
    <div style="color: #475569; font-size: 0.92rem; line-height: 1.55; max-width: 820px;">
        Enforce non-negotiable brand rules, verify conditional pricing and promotional claims, flag unsupported efficacy promises, and maintain a traceable human approval audit trail.
    </div>
</div>
""",
                unsafe_allow_html=True
            )
        with col_w2:
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Audit New Content", type="primary", use_container_width=True):
                st.session_state["active_tab"] = "New Content Review"
                st.session_state["review_step"] = 1
                st.rerun()
            if st.button("📋 Open Review Queue", type="secondary", use_container_width=True):
                st.session_state["active_tab"] = "Review Queue"
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Database-Derived Summary Metrics
    insights = get_governance_insights()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        c1_html = render_metric_card_html("Total Assets Audited", insights['total_submissions'], "Cumulative submissions in system", accent_color="#166534")
        render_html(c1_html)
    with c2:
        c2_html = render_metric_card_html("Awaiting Review", insights['pending_reviews'], "Assets pending human disposition", accent_color="#A16207")
        render_html(c2_html)
    with c3:
        c3_html = render_metric_card_html("Policy Holds", insights['hold_count'], "Violations blocked by rules", accent_color="#DC2626")
        render_html(c3_html)
    with c4:
        c4_html = render_metric_card_html("Human Approved", insights['approved_count'], "Signed off for publication", accent_color="#166534")
        render_html(c4_html)

    render_divider("•")

    # Architecture & Standards
    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.container(border=True):
            st.markdown("#### Closed-Loop Governance Pipeline")
            st.markdown(
                """
<div style="font-size: 0.9rem; line-height: 1.6; color: #334155;">
    <div style="margin-bottom: 10px; display: flex; gap: 10px;">
        <span style="font-weight: 700; color: #166534; min-width: 20px;">1.</span>
        <div><b>Content Ingestion & Metadata Context:</b> Evaluates draft copy across Instagram, LinkedIn, Google Ads, Email, and Web with full revision history.</div>
    </div>
    <div style="margin-bottom: 10px; display: flex; gap: 10px;">
        <span style="font-weight: 700; color: #166534; min-width: 20px;">2.</span>
        <div><b>Deterministic Rule Engine:</b> Applies non-negotiable checks on prohibited terminology, promotional pricing (e.g. ₹799 vs ₹999), and statutory legal disclaimers.</div>
    </div>
    <div style="margin-bottom: 10px; display: flex; gap: 10px;">
        <span style="font-weight: 700; color: #166534; min-width: 20px;">3.</span>
        <div><b>Contextual AI Analysis:</b> Identifies tone mismatches, unverified efficacy claims, and promotional risks without hallucinating citations.</div>
    </div>
    <div style="margin-bottom: 10px; display: flex; gap: 10px;">
        <span style="font-weight: 700; color: #166534; min-width: 20px;">4.</span>
        <div><b>Explainable Recommendations (HOLD &gt; REVIEW &gt; PASS):</b> Generates itemized findings with exact matched text, policy rules, and suggested corrections.</div>
    </div>
    <div style="display: flex; gap: 10px;">
        <span style="font-weight: 700; color: #166534; min-width: 20px;">5.</span>
        <div><b>Human Sign-off & Audit Trail:</b> Enforces authorized human decisions and automatically invalidates prior approvals when copy is edited.</div>
    </div>
</div>
""",
                unsafe_allow_html=True
            )

    with col_right:
        with st.container(border=True):
            st.markdown("#### Policy Disposition Model")
            pass_badge = render_disposition_badge("PASS")
            review_badge = render_disposition_badge("REVIEW")
            hold_badge = render_disposition_badge("HOLD")

            standards_html = f"""
<div style="font-size: 0.9rem; line-height: 1.55;">
    <div style="margin-bottom: 10px; padding: 8px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
        <div style="margin-bottom: 4px;">{pass_badge}</div>
        <span style="color: #475569; font-size: 0.83rem;">All mandatory policies satisfied. Copy is clear to proceed.</span>
    </div>
    <div style="margin-bottom: 10px; padding: 8px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
        <div style="margin-bottom: 4px;">{review_badge}</div>
        <span style="color: #475569; font-size: 0.83rem;">Unverified claim, conditional promo code, or tone review required.</span>
    </div>
    <div style="margin-bottom: 10px; padding: 8px 10px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px;">
        <div style="margin-bottom: 4px;">{hold_badge}</div>
        <span style="color: #475569; font-size: 0.83rem;">Critical rule or prohibited phrasing violated. Blocked from publication.</span>
    </div>
</div>
<div style="background-color: #FEF3C7; border: 1px solid #FCD34D; border-radius: 6px; padding: 0.65rem 0.85rem; margin-top: 8px; font-size: 0.82rem; color: #92400E; line-height: 1.45;">
    <b>Governance Standard:</b> Automated checks provide instant policy guidance; authorized human sign-off is required for official external publication.
</div>
"""
            render_html(standards_html)

    # Recent Governance Activity (Derived purely from SQLite database)
    st.markdown("### Recent Governance Activity")
    recent_activity = insights.get("recent_activity", [])

    if not recent_activity:
        empty_html = render_empty_state_html(
            "📋",
            "No Content Audits Logged Yet",
            "No campaign assets have been reviewed yet. Click 'Audit New Content' above to run your first compliance check."
        )
        render_html(empty_html)
    else:
        for act in recent_activity:
            rec_badge = render_disposition_badge(act["recommendation"])
            formatted_time = format_utc_timestamp(act['created_at'])
            act_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.9rem 1.25rem; margin-bottom: 0.65rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);">
    <div>
        <div style="font-weight: 700; color: #14532D; font-size: 0.95rem;">{act['title']}</div>
        <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">
            Channel: <b style="color: #0F172A;">{act['channel']}</b> &bull; Format: <b style="color: #0F172A;">{act['content_type']}</b> &bull; Audited: {formatted_time}
        </div>
    </div>
    <div>{rec_badge}</div>
</div>
"""
            render_html(act_html)


# =============================================================
# SECTION 2: NEW CONTENT REVIEW (4-STEP WORKFLOW)
# =============================================================
elif st.session_state["active_tab"] == "New Content Review":
    st.markdown("## Content Review & Compliance Verification")

    # Render 4-step visible progress stepper
    render_stepper(st.session_state["review_step"])

    brands = get_all_brands()
    brand_map = {b.name: b.id for b in brands}
    brand_names = list(brand_map.keys())

    # ---------------------------------------------------------
    # STEP 1: CONTENT DRAFT & METADATA
    # ---------------------------------------------------------
    if st.session_state["review_step"] == 1:
        with st.container(border=True):
            st.markdown("#### Step 1: Content Draft & Campaign Metadata")

            # Preset buttons to quickly test compliance rules
            st.markdown(
                "<span style='font-size: 0.85rem; color: #64748B; font-weight: 600;'>QUICK TEMPLATES TO TEST POLICY RULES:</span>",
                unsafe_allow_html=True
            )
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                if st.button("⚠️ Test Promotional Offer (Triggers HOLD)", use_container_width=True):
                    st.session_state["cr_title"] = "Festival Flash Sale Ad"
                    st.session_state["cr_content"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
                    st.session_state["cr_evidence"] = ""
                    st.session_state["cr_channel"] = "Instagram"
                    st.session_state["cr_type"] = "advertisement"
                    st.rerun()

            with col_p2:
                if st.button("✔ Test Standard Copy (100% PASS)", use_container_width=True):
                    st.session_state["cr_title"] = "Daily Clarity & Wellness Post"
                    st.session_state["cr_content"] = (
                        "Support your daily mental clarity with Nivara Pro for ₹999. "
                        "Formulated with natural adaptogens to assist your daily wellness journey.\n\n"
                        "*Disclaimer: Results may vary based on individual lifestyle, diet, and physiological factors."
                    )
                    st.session_state["cr_evidence"] = "Formulation Quality Certificate: ISO-9001-NIVARA"
                    st.session_state["cr_channel"] = "LinkedIn"
                    st.session_state["cr_type"] = "social_post"
                    st.rerun()

            with col_p3:
                if st.button("📄 Test Promo with Evidence (PASS)", use_container_width=True):
                    st.session_state["cr_title"] = "Authorized Seasonal Email Offer"
                    st.session_state["cr_content"] = (
                        "Exclusive festive offer: Claim Nivara Pro for ₹799 during our festive celebration! "
                        "Formulated to support your daily wellness journey.\n\n"
                        "*Results may vary based on individual lifestyle and physiological factors."
                    )
                    st.session_state["cr_evidence"] = "Authorized Promo Code: DIWALI-2026-PROMO-AUTH (Valid until Nov 10)"
                    st.session_state["cr_channel"] = "Email"
                    st.session_state["cr_type"] = "email"
                    st.rerun()

            st.markdown("---")

            # Form fields
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.session_state["cr_title"] = st.text_input("Content Title*", value=st.session_state["cr_title"])
                brand_choice = st.selectbox("Applicable Brand Guidelines*", brand_names, index=0)
                st.session_state["cr_channel"] = st.selectbox(
                    "Publishing Channel*",
                    ["Instagram", "LinkedIn", "Google Ads", "Email", "Website", "Print"],
                    index=["Instagram", "LinkedIn", "Google Ads", "Email", "Website", "Print"].index(st.session_state["cr_channel"])
                )
            with col_f2:
                st.session_state["cr_type"] = st.selectbox(
                    "Content Format*",
                    ["social_post", "advertisement", "email", "blog_article", "product_copy"],
                    index=["social_post", "advertisement", "email", "blog_article", "product_copy"].index(st.session_state["cr_type"])
                )
                st.session_state["cr_campaign"] = st.text_input("Campaign Name (Optional)", value=st.session_state["cr_campaign"])
                st.session_state["cr_creator"] = st.text_input("Creator / Agency Attribution", value=st.session_state["cr_creator"])

            st.session_state["cr_content"] = st.text_area(
                "Content Body Copy*",
                value=st.session_state["cr_content"],
                height=150,
                help="Enter marketing copy to audit against brand guidelines, pricing rules, and statutory disclaimers."
            )

            st.session_state["cr_evidence"] = st.text_area(
                "Supporting Evidence / Authorization Codes / Citations (Optional)",
                value=st.session_state["cr_evidence"],
                height=70,
                help="Provide promotional authorization codes, clinical study citations, or documentation references."
            )

            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn2:
                if st.button("Run Compliance Audit →", type="primary", use_container_width=True):
                    if not st.session_state["cr_title"].strip() or not st.session_state["cr_content"].strip():
                        st.error("Please provide both a Content Title and Content Body to proceed.")
                    else:
                        selected_brand_id = brand_map[brand_choice]
                        # Create or reuse submission
                        if not st.session_state["cr_sub_id"]:
                            sub = create_submission(
                                title=st.session_state["cr_title"].strip(),
                                content_type=st.session_state["cr_type"],
                                channel=st.session_state["cr_channel"],
                                campaign_name=st.session_state["cr_campaign"].strip(),
                                brand_id=selected_brand_id,
                                initial_content=st.session_state["cr_content"].strip(),
                                supporting_evidence=st.session_state["cr_evidence"].strip(),
                                creator=st.session_state["cr_creator"].strip()
                            )
                            st.session_state["cr_sub_id"] = sub.id
                        else:
                            sub = get_submission_by_id(st.session_state["cr_sub_id"])

                        with st.spinner("Executing deterministic policy rules & contextual analysis..."):
                            run = run_content_review_workflow(st.session_state["cr_sub_id"])
                            st.session_state["latest_review_run"] = run
                            st.session_state["cr_revised_content"] = run.suggested_revised_copy
                            st.session_state["review_step"] = 2
                            st.rerun()

    # ---------------------------------------------------------
    # STEP 2: POLICY ANALYSIS & FINDINGS
    # ---------------------------------------------------------
    elif st.session_state["review_step"] == 2:
        sub = get_submission_by_id(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        run = get_latest_review_run_for_submission(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None

        if not sub or not run:
            st.warning("No active audit run found. Please start by entering content in Step 1.")
            if st.button("← Return to Step 1", type="primary"):
                st.session_state["review_step"] = 1
                st.rerun()
        else:
            with st.container(border=True):
                st.markdown(f"#### Step 2: Policy Analysis Report — {sub.title} (v{sub.current_version_number})")

                # Recommendation banner matching color rules
                badge_html = render_disposition_badge(run.overall_recommendation)
                
                # Determine surface color based on recommendation
                if run.overall_recommendation == "PASS":
                    banner_bg = "#DCFCE7"
                    banner_border = "#86EFAC"
                    banner_title_color = "#14532D"
                elif run.overall_recommendation == "HOLD":
                    banner_bg = "#FEE2E2"
                    banner_border = "#FCA5A5"
                    banner_title_color = "#DC2626"
                else: # REVIEW
                    banner_bg = "#FEF3C7"
                    banner_border = "#FCD34D"
                    banner_title_color = "#A16207"

                banner_html = f"""
<div style="background: {banner_bg}; border-radius: 8px; border: 1.5px solid {banner_border}; padding: 1.15rem 1.4rem; margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;">
        <div>{badge_html}</div>
        <div style="font-size: 0.82rem; color: #475569;">
            Engine Mode: <b style="color: #0F172A;">{run.ai_provider_mode}</b> | Guideline: <code>{run.guideline_version_id}</code>
        </div>
    </div>
    <div style="font-size: 0.95rem; color: #0F172A; line-height: 1.6; white-space: pre-wrap;">
        <b style="color: {banner_title_color};">Executive Rationale:</b><br>{run.summary}
    </div>
</div>
"""
                render_html(banner_html)

                # Severity counters
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    m1_html = render_metric_card_html("Critical Blockers", run.critical_count, "Violations blocking pass", accent_color="#DC2626")
                    render_html(m1_html)
                with m2:
                    m2_html = render_metric_card_html("High Severity", run.high_count, "Significant risk items", accent_color="#EA580C")
                    render_html(m2_html)
                with m3:
                    m3_html = render_metric_card_html("Medium Issues", run.medium_count, "Verification required", accent_color="#A16207")
                    render_html(m3_html)
                with m4:
                    m4_html = render_metric_card_html("Low / Advisory", run.low_count, "Recommendations", accent_color="#166534")
                    render_html(m4_html)

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                st.markdown("### Itemized Policy Findings")
                if not run.findings:
                    st.success("✔ No policy violations detected. Content satisfies all active brand rules.")
                else:
                    for idx, f in enumerate(run.findings):
                        border_class = "finding-crit" if f.severity == "CRITICAL" else ("finding-high" if f.severity == "HIGH" else ("finding-med" if f.severity == "MEDIUM" else "finding-low"))
                        sev_badge = render_severity_badge(f.severity)
                        
                        source_label = "Deterministic Rule Engine" if "deterministic" in f.source.lower() else "Contextual AI Advisory"
                        source_style = "background: #DCFCE7; color: #14532D; border: 1px solid #86EFAC;" if "deterministic" in f.source.lower() else "background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE;"
                        source_badge = f'<span style="{source_style} font-size: 0.74rem; font-weight: 700; padding: 2px 7px; border-radius: 4px;">{source_label}</span>'

                        finding_html = f"""
<div class="finding-box {border_class}">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            {sev_badge}
            <span style="font-weight: 700; color: #14532D; font-size: 0.98rem;">#{idx+1} {f.rule_title}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            {source_badge}
            <span style="font-size: 0.78rem; background: #F1F5F9; color: #334155; padding: 2px 8px; border-radius: 4px; font-weight: 600; border: 1px solid #CBD5E1;">
                {f.category} &bull; Impact: <b>{f.disposition_impact}</b>
            </span>
        </div>
    </div>
    <div style="font-size: 0.92rem; color: #0F172A; margin-bottom: 6px;">
        <b>Matched Text:</b> <code style="color: #DC2626; background: #FEE2E2; font-size: 0.9rem; padding: 2px 6px; border-radius: 3px;">{f.matched_text}</code>
    </div>
    <div style="font-size: 0.9rem; color: #334155; margin-bottom: 6px;">
        <b>Policy Explanation:</b> {f.explanation}
    </div>
    <div style="font-size: 0.9rem; color: #166534; margin-bottom: 6px;">
        <b>Brand Condition:</b> {f.expected_condition}
    </div>
    <div style="font-size: 0.9rem; color: #A16207; margin-bottom: 6px;">
        <b>Recommended Correction:</b> {f.recommended_correction}
    </div>
    <div style="font-size: 0.78rem; color: #64748B; margin-top: 6px; border-top: 1px solid #F1F5F9; padding-top: 6px;">
        <b>Verification State:</b> <code>{f.verification_state}</code> | <b>Source Identifier:</b> {f.source}
    </div>
</div>
"""
                        render_html(finding_html)

            # Stepper Navigation
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b1:
                if st.button("← Back to Content Draft", use_container_width=True):
                    st.session_state["review_step"] = 1
                    st.rerun()
            with col_b3:
                if st.button("Proceed to Suggested Corrections →", type="primary", use_container_width=True):
                    st.session_state["review_step"] = 3
                    st.rerun()

    # ---------------------------------------------------------
    # STEP 3: SUGGESTED CORRECTIONS & RE-AUDIT
    # ---------------------------------------------------------
    elif st.session_state["review_step"] == 3:
        sub = get_submission_by_id(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        run = get_latest_review_run_for_submission(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        latest_rev = get_latest_revision(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None

        if not sub or not run:
            st.warning("No active submission. Please return to Step 1.")
            if st.button("← Return to Step 1", type="primary"):
                st.session_state["review_step"] = 1
                st.rerun()
        else:
            with st.container(border=True):
                st.markdown(f"#### Step 3: Suggested Corrections & Revision — {sub.title} (Current: v{sub.current_version_number})")

                c_orig, c_sugg = st.columns(2)
                with c_orig:
                    st.markdown("**Original Submitted Draft:**")
                    with st.container(border=True):
                        st.text(latest_rev.content_text if latest_rev else "")

                with c_sugg:
                    st.markdown("**On-Brand Suggested Compliant Copy:**")
                    with st.container(border=True):
                        st.text(run.suggested_revised_copy)

                st.markdown("---")
                st.markdown("### Refine & Publish Revision")
                rev_text_val = st.text_area(
                    "Editable Revised Copy",
                    value=st.session_state.get("cr_revised_content") or run.suggested_revised_copy,
                    height=130
                )
                rev_evidence_val = st.text_area(
                    "Updated Supporting Evidence / Citations",
                    value=latest_rev.supporting_evidence if latest_rev else "",
                    height=60
                )
                rev_summary_val = st.text_input("Revision Notes", value="Applied recommended on-brand pricing and required variation disclaimer")

                if st.button("⚡ Re-audit Revised Copy (Creates New Version)", type="primary"):
                    if not rev_text_val.strip():
                        st.error("Revised copy cannot be empty.")
                    else:
                        new_rev = create_content_revision(
                            submission_id=sub.id,
                            new_content_text=rev_text_val.strip(),
                            supporting_evidence=rev_evidence_val.strip(),
                            change_summary=rev_summary_val.strip(),
                            actor="Content Creator"
                        )
                        new_run = run_content_review_workflow(sub.id, revision_id=new_rev.id)
                        st.session_state["latest_review_run"] = new_run
                        st.session_state["cr_revised_content"] = rev_text_val.strip()
                        st.success(f"Published Version v{new_rev.version_number}! New Audit Recommendation: {new_run.overall_recommendation}")
                        st.rerun()

            # Stepper Navigation
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b1:
                if st.button("← Back to Policy Analysis", use_container_width=True):
                    st.session_state["review_step"] = 2
                    st.rerun()
            with col_b3:
                if st.button("Proceed to Human Sign-off →", type="primary", use_container_width=True):
                    st.session_state["review_step"] = 4
                    st.rerun()

    # ---------------------------------------------------------
    # STEP 4: HUMAN DECISION & SIGN-OFF
    # ---------------------------------------------------------
    elif st.session_state["review_step"] == 4:
        sub = get_submission_by_id(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        run = get_latest_review_run_for_submission(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        latest_rev = get_latest_revision(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else None
        decisions = get_decisions_for_submission(st.session_state["cr_sub_id"]) if st.session_state["cr_sub_id"] else []

        if not sub or not run:
            st.warning("No active submission. Please return to Step 1.")
            if st.button("← Return to Step 1", type="primary"):
                st.session_state["review_step"] = 1
                st.rerun()
        else:
            with st.container(border=True):
                st.markdown(f"#### Step 4: Human Governance Decision & Sign-off — {sub.title} (v{sub.current_version_number})")

                rec_badge = render_disposition_badge(run.overall_recommendation)
                sub_status_badge = render_status_badge(sub.current_status)
                
                sub_meta_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.9rem 1.15rem; margin-bottom: 0.85rem; display: flex; justify-content: space-between; align-items: center;">
    <div style="display: flex; align-items: center; gap: 10px;">
        {rec_badge}
        {sub_status_badge}
    </div>
    <div style="font-size: 0.85rem; color: #64748B;">
        Version: <b style="color: #0F172A;">v{sub.current_version_number}</b> &bull; Channel: <b style="color: #0F172A;">{sub.channel}</b> &bull; Asset ID: <code>{sub.id}</code>
    </div>
</div>
"""
                render_html(sub_meta_html)

                st.markdown("**Final Content Copy for Publication:**")
                with st.container(border=True):
                    st.text(latest_rev.content_text if latest_rev else "")

                if latest_rev and latest_rev.supporting_evidence:
                    st.markdown(f"**Supporting Evidence:** `{latest_rev.supporting_evidence}`")

                if decisions:
                    st.markdown("#### Prior Human Decisions")
                    for d in decisions:
                        valid_tag = "<span style='color: #166534; font-weight: 700; background: #DCFCE7; border: 1px solid #86EFAC; padding: 2px 7px; border-radius: 4px; font-size: 0.76rem;'>ACTIVE APPROVAL</span>" if d.is_currently_valid else "<span style='color: #DC2626; font-weight: 700; background: #FEE2E2; border: 1px solid #FCA5A5; padding: 2px 7px; border-radius: 4px; font-size: 0.76rem;'>REVOKED BY SUBSEQUENT EDIT</span>"
                        dec_formatted_time = format_utc_timestamp(d.created_at)
                        dec_html = f"""
<div style="font-size: 0.88rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.75rem 0.95rem; border-radius: 6px; margin-bottom: 6px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-weight: 700; color: #14532D;">{d.decision} by {d.reviewer_name} ({d.reviewer_role})</span>
        <div>{valid_tag}</div>
    </div>
    <div style="color: #64748B; font-size: 0.8rem; margin-bottom: 4px;">Timestamp: {dec_formatted_time}</div>
    <div style="color: #334155; font-style: italic;">Rationale: {d.reviewer_comments}</div>
</div>
"""
                        render_html(dec_html)

                st.markdown("#### Record Official Human Decision")
                with st.form("official_decision_form"):
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        rev_name = st.text_input("Reviewer Name", value="Priya Sharma")
                        rev_role = st.selectbox("Regulatory Role", ["Brand Governance Director", "Legal Counsel", "Marketing Lead"])
                    with col_d2:
                        decision_choice = st.radio("Decision", ["APPROVED", "CHANGES_REQUESTED", "REJECTED"], index=0)
                        rev_comments = st.text_area("Reviewer Rationale & Notes", value="Verified against brand guidelines and statutory disclaimers.", height=70)

                    submit_dec = st.form_submit_button("✔ Confirm & Record Official Decision", type="primary")

                if submit_dec:
                    submit_human_decision(
                        submission_id=sub.id,
                        revision_id=latest_rev.id,
                        review_run_id=run.id,
                        decision=decision_choice,
                        reviewer_name=rev_name,
                        reviewer_role=rev_role,
                        reviewer_comments=rev_comments
                    )
                    st.success(f"Official decision '{decision_choice}' recorded! Audit trail updated.")
                    st.rerun()

                st.info("Policy Safeguard: Editing approved content automatically revokes the prior approval for the new draft and mandates revalidation.")

            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b1:
                if st.button("← Back to Corrections", use_container_width=True):
                    st.session_state["review_step"] = 3
                    st.rerun()
            with col_b3:
                if st.button("Start Fresh Review", type="secondary", use_container_width=True):
                    st.session_state["review_step"] = 1
                    st.session_state["cr_sub_id"] = None
                    st.session_state["cr_title"] = ""
                    st.session_state["cr_content"] = ""
                    st.session_state["cr_evidence"] = ""
                    st.rerun()


# =============================================================
# SECTION 3: REVIEW QUEUE
# =============================================================
elif st.session_state["active_tab"] == "Review Queue":
    st.markdown("## Content Approval & Governance Queue")

    col_q1, col_q2 = st.columns([1, 2])
    with col_q1:
        status_filter = st.selectbox(
            "Filter by Workflow Status",
            ["ALL", "SUBMITTED", "IN_REVIEW", "CHANGES_REQUESTED", "APPROVED", "REJECTED"],
            index=0
        )
    with col_q2:
        search_query = st.text_input("Search content title or channel...", value="")

    submissions = get_all_submissions(status_filter=status_filter)
    if search_query.strip():
        q = search_query.lower()
        submissions = [s for s in submissions if q in s.title.lower() or q in s.channel.lower()]

    st.markdown(
        f"<span style='font-size: 0.88rem; color: #64748B;'>Displaying <b>{len(submissions)}</b> content record(s) matching filter.</span>",
        unsafe_allow_html=True
    )

    if not submissions:
        empty_html = render_empty_state_html(
            "🔍",
            "No Records Match Current Filter",
            "No content assets match the specified status or search query. Adjust the filters or submit new content for review."
        )
        render_html(empty_html)
    else:
        for sub in submissions:
            latest_run = get_latest_review_run_for_submission(sub.id)
            latest_rev = get_latest_revision(sub.id)
            decisions = get_decisions_for_submission(sub.id)
            rec_badge = render_disposition_badge(latest_run.overall_recommendation if latest_run else "REVIEW")
            status_tag = render_status_badge(sub.current_status)

            with st.expander(f"📌 {sub.title} ({sub.content_type} • {sub.channel}) — Status: {sub.current_status} (v{sub.current_version_number})", expanded=False):
                formatted_created = format_utc_timestamp(sub.created_at)
                sub_meta_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.75rem 1rem; border-radius: 6px;">
    <div style="display: flex; align-items: center; gap: 8px;">
        {rec_badge}
        {status_tag}
    </div>
    <div style="font-size: 0.82rem; color: #64748B;">Asset ID: <code>{sub.id}</code> &bull; Submitted: {formatted_created}</div>
</div>
"""
                render_html(sub_meta_html)

                st.markdown("**Current Content Text:**")
                with st.container(border=True):
                    st.text(latest_rev.content_text if latest_rev else "")

                if latest_rev and latest_rev.supporting_evidence:
                    st.markdown(f"**Supporting Evidence:** `{latest_rev.supporting_evidence}`")

                if latest_run:
                    st.markdown(f"**Automated System Recommendation ({latest_run.overall_recommendation}):**")
                    with st.container(border=True):
                        st.markdown(latest_run.summary)

                if decisions:
                    st.markdown("#### Prior Decision History")
                    for d in decisions:
                        valid_tag = "<span style='color: #166534; font-weight: 700; background: #DCFCE7; border: 1px solid #86EFAC; padding: 2px 7px; border-radius: 4px; font-size: 0.76rem;'>ACTIVE APPROVAL</span>" if d.is_currently_valid else "<span style='color: #DC2626; font-weight: 700; background: #FEE2E2; border: 1px solid #FCA5A5; padding: 2px 7px; border-radius: 4px; font-size: 0.76rem;'>REVOKED BY CONTENT EDIT</span>"
                        dec_formatted = format_utc_timestamp(d.created_at)
                        dec_html = f"""
<div style="font-size: 0.88rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.65rem 0.85rem; border-radius: 6px; margin-bottom: 6px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-weight: 700; color: #14532D;">{d.decision} by {d.reviewer_name} ({d.reviewer_role})</span>
        <div>{valid_tag}</div>
    </div>
    <div style="color: #64748B; font-size: 0.8rem; margin-bottom: 3px;">Recorded: {dec_formatted}</div>
    <div style="color: #334155; font-style: italic;">Rationale: {d.reviewer_comments}</div>
</div>
"""
                        render_html(dec_html)

                st.markdown("#### Record Official Human Decision")
                with st.form(f"queue_decision_form_{sub.id}"):
                    c_rev1, c_rev2 = st.columns(2)
                    with c_rev1:
                        rev_name = st.text_input("Reviewer Name", value="Priya Sharma", key=f"qrname_{sub.id}")
                        rev_role = st.selectbox("Regulatory Role", ["Brand Governance Director", "Legal Counsel", "Marketing Lead"], key=f"qrrole_{sub.id}")
                    with c_rev2:
                        decision_choice = st.radio("Decision", ["APPROVED", "CHANGES_REQUESTED", "REJECTED"], key=f"qdchoice_{sub.id}")
                        rev_comments = st.text_area("Reviewer Rationale & Notes", value="Verified against brand guidelines and statutory disclaimers.", height=70, key=f"qrcomm_{sub.id}")

                    submit_dec = st.form_submit_button("Record Official Decision", type="primary")

                if submit_dec:
                    if not latest_run:
                        st.error("Cannot approve content before running an automated governance audit.")
                    else:
                        submit_human_decision(
                            submission_id=sub.id,
                            revision_id=latest_rev.id,
                            review_run_id=latest_run.id,
                            decision=decision_choice,
                            reviewer_name=rev_name,
                            reviewer_role=rev_role,
                            reviewer_comments=rev_comments
                        )
                        st.success(f"Official decision '{decision_choice}' recorded! Audit trail updated.")
                        st.rerun()

                st.info("Policy Safeguard: Editing approved content automatically revokes prior approvals and mandates revalidation.")


# =============================================================
# SECTION 4: BRAND GUIDELINES
# =============================================================
elif st.session_state["active_tab"] == "Brand Guidelines":
    st.markdown("## Brand Guidelines & Policy Configuration")

    brands = get_all_brands()
    brand_map = {b.name: b.id for b in brands}
    brand_names = list(brand_map.keys())

    selected_brand_name = st.selectbox("Select Brand Profile", brand_names, index=0)
    selected_brand_id = brand_map[selected_brand_name]
    brand = get_brand_by_id(selected_brand_id)
    guideline = get_active_guideline_version(selected_brand_id)

    if brand and guideline:
        if brand.is_demo:
            st.info("Demonstration Profile: Nivara Pro is an illustrative premium wellness brand profile used to demonstrate deterministic rules, conditional promotional checks, and evidence verification.")

        with st.container(border=True):
            brand_header_html = f"""
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
    <div>
        <div style="font-size: 1.35rem; font-weight: 800; color: #14532D;">{brand.name}</div>
        <div style="font-size: 0.9rem; color: #64748B; margin-top: 2px;">{brand.tagline}</div>
    </div>
    <div style="display: flex; gap: 8px;">
        <span style="background: #DCFCE7; color: #14532D; font-size: 0.78rem; font-weight: 700; padding: 3px 9px; border-radius: 4px; border: 1px solid #86EFAC;">
            ACTIVE VERSION: {guideline.version_label}
        </span>
        <span style="background: #F1F5F9; color: #334155; font-size: 0.78rem; font-weight: 600; padding: 3px 9px; border-radius: 4px; border: 1px solid #CBD5E1;">
            INDUSTRY: {brand.industry}
        </span>
    </div>
</div>
<div style="font-size: 0.9rem; color: #334155; line-height: 1.5; margin-top: 8px;">
    {brand.description}
</div>
"""
            render_html(brand_header_html)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            with st.container(border=True):
                st.markdown("#### Tone of Voice")
                st.markdown(f"<div style='font-size: 0.92rem; color: #334155; line-height: 1.5;'>{guideline.tone_of_voice}</div>", unsafe_allow_html=True)
        with col_g2:
            with st.container(border=True):
                st.markdown("#### Target Audience")
                st.markdown(f"<div style='font-size: 0.92rem; color: #334155; line-height: 1.5;'>{guideline.target_audience}</div>", unsafe_allow_html=True)

        st.markdown(f"### Active Deterministic Brand Rules ({len(guideline.rules)} rules configured)")
        for r in guideline.rules:
            sev_badge = render_severity_badge(r.severity)
            border_color = "#DC2626" if r.severity == "CRITICAL" else ("#EA580C" if r.severity == "HIGH" else ("#A16207" if r.severity == "MEDIUM" else "#166534"))
            blocks_tag = "<span style='color: #DC2626; font-weight: 700; background: #FEE2E2; border: 1px solid #FCA5A5; padding: 2px 7px; border-radius: 4px; font-size: 0.74rem;'>BLOCKS APPROVAL / HOLD</span>" if r.blocks_approval else "<span style='color: #A16207; font-weight: 600; background: #FEF3C7; border: 1px solid #FCD34D; padding: 2px 7px; border-radius: 4px; font-size: 0.74rem;'>ADVISORY REVIEW</span>"

            rule_html = f"""
<div class="finding-box" style="border-left: 4px solid {border_color};">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            {sev_badge}
            <span style="font-weight: 700; color: #14532D; font-size: 0.98rem;">{r.title}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 0.78rem; background: #F1F5F9; color: #334155; padding: 2px 8px; border-radius: 4px; font-weight: 600; border: 1px solid #CBD5E1;">Category: <b>{r.category}</b></span>
            {blocks_tag}
        </div>
    </div>
    <div style="font-size: 0.88rem; color: #475569; margin-bottom: 4px;">
        <b>Trigger Pattern:</b> <code>{r.pattern}</code> | <b>Rule Type:</b> <code>{r.rule_type}</code>
    </div>
    <div style="font-size: 0.9rem; color: #0F172A; margin-bottom: 4px;">
        <b>Description:</b> {r.description}
    </div>
    <div style="font-size: 0.88rem; color: #166534;">
        <b>Mandated Fix:</b> {r.suggested_fix}
    </div>
</div>
"""
            render_html(rule_html)

        render_divider("•")
        st.markdown("### Guideline Revision Management")
        with st.expander(f"➕ Publish New Guideline Version (Current: v{guideline.version_number}.0)", expanded=False):
            with st.form("edit_guideline_form"):
                new_tone = st.text_input("Tone of Voice", value=guideline.tone_of_voice)
                new_aud = st.text_input("Target Audience", value=guideline.target_audience)
                changelog_text = st.text_input("Revision Notes", value="Updated medical disclaimer and added prescription restriction rule")

                st.markdown("#### Add Additional Prohibited Phrasing Rule")
                new_rule_title = st.text_input("Rule Title", value="Prohibit 'No Prescription Needed'")
                new_rule_pattern = st.text_input("Pattern / Keywords (pipe separated)", value="no prescription needed|no rx needed")
                new_rule_fix = st.text_input("Suggested Fix", value="Consult a qualified healthcare practitioner")

                publish_btn = st.form_submit_button("Publish New Guideline Revision", type="primary")

            if publish_btn:
                existing_rules_data = [
                    {
                        "rule_type": r.rule_type,
                        "category": r.category,
                        "severity": r.severity,
                        "pattern": r.pattern,
                        "title": r.title,
                        "description": r.description,
                        "suggested_fix": r.suggested_fix,
                        "blocks_approval": r.blocks_approval,
                        "is_mandatory": r.is_mandatory,
                        "metadata": r.metadata
                    }
                    for r in guideline.rules
                ]
                if new_rule_title and new_rule_pattern:
                    existing_rules_data.append({
                        "rule_type": "prohibited_phrase",
                        "category": "Legal & Compliance",
                        "severity": "CRITICAL",
                        "pattern": new_rule_pattern,
                        "title": new_rule_title,
                        "description": "Prohibited medical dispensing claim without authorized prescription.",
                        "suggested_fix": new_rule_fix,
                        "blocks_approval": True,
                        "is_mandatory": True,
                        "metadata": {}
                    })

                new_gv = create_new_guideline_version(
                    brand_id=selected_brand_id,
                    tone_of_voice=new_tone.strip(),
                    target_audience=new_aud.strip(),
                    approved_prices=guideline.approved_prices,
                    conditional_promotions=guideline.conditional_promotions,
                    required_disclaimers=guideline.required_disclaimers,
                    evidence_requirements=guideline.evidence_requirements,
                    changelog=changelog_text.strip(),
                    rules_data=existing_rules_data
                )
                st.success(f"Successfully published {new_gv.version_label}! Active for all subsequent audits.")
                st.rerun()


# =============================================================
# SECTION 5: INSIGHTS (GOVERNANCE ANALYTICS)
# =============================================================
elif st.session_state["active_tab"] == "Insights":
    st.markdown("## Governance Analytics & Recurring Risk Intelligence")

    insights = get_governance_insights()
    pass_ratio = (insights['pass_count'] / max(insights['total_submissions'], 1)) * 100 if insights['total_submissions'] > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        c1_html = render_metric_card_html("Total Assets Audited", insights['total_submissions'], "Cumulative submissions", accent_color="#166534")
        render_html(c1_html)
    with c2:
        c2_html = render_metric_card_html("Clean Pass Rate", f"{pass_ratio:.0f}%", "Unblocked on first audit", accent_color="#166534")
        render_html(c2_html)
    with c3:
        c3_html = render_metric_card_html("Blocked Violations (HOLD)", insights['hold_count'], "Critical rule infractions", accent_color="#DC2626")
        render_html(c3_html)
    with c4:
        c4_html = render_metric_card_html("Human Approved", insights['approved_count'], "Signed off for publication", accent_color="#166534")
        render_html(c4_html)

    render_divider("•")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown("### Top Frequently Triggered Brand Rules")
        if not insights['top_rules']:
            empty_r_html = render_empty_state_html(
                "🛡️",
                "No Rule Violations Logged",
                "No policy violations have been detected in submitted drafts yet."
            )
            render_html(empty_r_html)
        else:
            for r in insights['top_rules']:
                rule_stat_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.9rem 1.15rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #A16207; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);">
    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #14532D; font-size: 0.95rem;">
        <span>{r['rule_title']}</span>
        <span style="color: #A16207; background: #FEF3C7; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #FCD34D;">{r['trigger_count']} times</span>
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">
        Category: <b style="color: #0F172A;">{r['category']}</b> &bull; Severity: <b style="color: #0F172A;">{r['severity']}</b>
    </div>
</div>
"""
                render_html(rule_stat_html)

    with col_i2:
        st.markdown("### Repeated Unsupported Claim Patterns")
        if not insights['unsupported_patterns']:
            empty_c_html = render_empty_state_html(
                "📊",
                "No Repeated Claims Flagged",
                "No repeated unsupported claims or unverified promotional phrases logged."
            )
            render_html(empty_c_html)
        else:
            for p in insights['unsupported_patterns']:
                claim_stat_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.9rem 1.15rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #DC2626; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);">
    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #14532D; font-size: 0.95rem;">
        <code style="color: #DC2626; background: #FEE2E2; padding: 2px 6px; border-radius: 3px;">{p['matched_text']}</code>
        <span style="color: #DC2626; background: #FEE2E2; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #FCA5A5;">Flagged {p['count']}x</span>
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">
        Category: <b style="color: #0F172A;">{p['category']}</b> &bull; Requires empirical evidence or authorization
    </div>
</div>
"""
                render_html(claim_stat_html)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("### Policy Findings by Category")
    cat_items = insights.get("category_breakdown", {})
    if cat_items:
        cols = st.columns(len(cat_items))
        for idx, (cat, cnt) in enumerate(cat_items.items()):
            with cols[idx]:
                cat_card_html = render_metric_card_html(cat.upper(), cnt, "Findings logged", accent_color="#166534")
                render_html(cat_card_html)
    else:
        st.info("No policy categories logged yet.")


# =============================================================
# SECTION 6: REVIEW HISTORY & AUDIT TRAIL
# =============================================================
elif st.session_state["active_tab"] == "Review History":
    st.markdown("## Traceable Governance Audit Trail")
    st.markdown(
        "<div style='color: #475569; font-size: 0.92rem; margin-bottom: 12px;'>"
        "Logged audit trail with exact UTC timestamps recording every draft submission, automated policy check, "
        "human approval decision, and approval invalidation in the local SQLite database."
        "</div>",
        unsafe_allow_html=True
    )

    audit_events = get_audit_trail(limit=50)

    if not audit_events:
        empty_hist_html = render_empty_state_html(
            "📜",
            "No Audit Records Found",
            "No governance events have been recorded in the database yet."
        )
        render_html(empty_hist_html)
    else:
        for ev in audit_events:
            color = "#166534"
            if "INVALIDATED" in ev.event_type:
                color = "#DC2626"
            elif "DECISION" in ev.event_type:
                color = "#A16207"
            elif "SUBMISSION" in ev.event_type:
                color = "#14532D"

            asset_str = f" &bull; <b>Asset ID:</b> <code>{ev.submission_id}</code>" if ev.submission_id else ""
            formatted_ev_time = format_utc_timestamp(ev.created_at)

            ev_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid {color}; padding: 0.9rem 1.25rem; border-radius: 6px; margin-bottom: 0.65rem; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
        <span style="font-weight: 700; color: {color}; font-size: 0.92rem;">[{ev.event_type}]</span>
        <span style="font-size: 0.8rem; color: #64748B;">{formatted_ev_time}</span>
    </div>
    <div style="font-size: 0.92rem; color: #0F172A; margin-bottom: 5px; line-height: 1.5;">{ev.description}</div>
    <div style="font-size: 0.8rem; color: #64748B;"><b>Actor:</b> <span style="color: #0F172A;">{ev.actor}</span>{asset_str}</div>
</div>
"""
            render_html(ev_html)
