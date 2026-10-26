"""BrandNiti AI — Every Brand Message. On Brand.
AI-Powered Brand Governance: Create Confidently. Review Intelligently. Publish Responsibly.

Enterprise SaaS Application with Horizontal Navigation and 4-Step Review Workflow.
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
    render_divider
)

# Helper for strictly unindented HTML rendering (guarantees CommonMark never converts HTML into code blocks)
def render_html(html_str: str):
    """Renders HTML strictly unindented so CommonMark never treats it as a code block."""
    clean_html = "\n".join(line.strip() for line in html_str.splitlines() if line.strip())
    st.markdown(clean_html, unsafe_allow_html=True)

# Page configuration - Clean full-width enterprise layout with collapsed sidebar
st.set_page_config(
    page_title="BrandNiti AI | Enterprise Brand Governance",
    page_icon="⚖️",
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

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


# =============================================================
# SECTION 1: OVERVIEW (PRACTICAL GOVERNANCE DASHBOARD)
# =============================================================
if st.session_state["active_tab"] == "Overview":
    # Welcome & Action Card
    with st.container(border=True):
        col_w1, col_w2 = st.columns([3, 1])
        with col_w1:
            st.markdown("### Executive Governance Dashboard")
            st.markdown(
                "Autonomous brand governance platform for marketing, agency partners, and corporate communications. "
                "Enforce non-negotiable brand rules, verify conditional promotional claims, detect unverified promises, "
                "and maintain an immutable human approval audit trail."
            )
        with col_w2:
            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
            if st.button("✨ Review New Content", type="primary", use_container_width=True):
                st.session_state["active_tab"] = "New Content Review"
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # High-level stats from SQLite
    insights = get_governance_insights()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.metric(label="TOTAL ASSETS AUDITED", value=insights['total_submissions'])
    with c2:
        with st.container(border=True):
            st.metric(label="AWAITING REVIEW", value=insights['pending_reviews'])
    with c3:
        with st.container(border=True):
            st.metric(label="ISSUES REQUIRING ATTENTION", value=insights['issues_requiring_attention'])
    with c4:
        with st.container(border=True):
            st.metric(label="HUMAN APPROVED", value=insights['approved_count'])

    render_divider("❖")

    # Architecture & Standards
    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.container(border=True):
            st.markdown("#### Closed-Loop Governance Pipeline")
            st.markdown(
                "BrandNiti AI protects brand integrity and legal compliance by verifying marketing messages before publication.\n\n"
                "- **1. Content Ingestion & Channel Context:** Ingest copy across Instagram, LinkedIn, Google Ads, Email, and Web with version tracking.\n"
                "- **2. Deterministic Validation Layer:** Non-negotiable checks on prohibited terminology, conditional pricing (₹799 vs standard ₹999), and required legal disclaimers.\n"
                "- **3. Contextual AI Review:** Evaluates tone mismatch, hyperbolic promises, and unverified efficacy claims without hallucinating sources.\n"
                "- **4. Explainable Disposition (HOLD > REVIEW > PASS):** Instant itemized findings with exact matched text, policy rules, and suggested corrections.\n"
                "- **5. Human Approval Workflow:** Traceable decisions with automatic invalidation if approved copy is subsequently edited."
            )

    with col_right:
        with st.container(border=True):
            st.markdown("#### Policy Disposition Model")
            pass_badge = render_disposition_badge("PASS")
            review_badge = render_disposition_badge("REVIEW")
            hold_badge = render_disposition_badge("HOLD")

            standards_html = f"""
<div style="font-size: 0.92rem; line-height: 1.6;">
    <div style="margin-bottom: 8px;">{pass_badge}<br><span style="color: #334155; font-size: 0.85rem;">All mandatory policies satisfied. Advisory clear to proceed.</span></div>
    <div style="margin-bottom: 8px;">{review_badge}<br><span style="color: #334155; font-size: 0.85rem;">Unverified claim, conditional promo, or tone review required.</span></div>
    <div style="margin-bottom: 8px;">{hold_badge}<br><span style="color: #334155; font-size: 0.85rem;">Mandatory prohibition violated. Blocked pending correction.</span></div>
</div>
<div style="background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 6px; padding: 0.65rem 0.85rem; margin-top: 10px; font-size: 0.82rem; color: #92400E;">
    <b>Governance Standard:</b> System recommendations are advisory. Official publication requires authorized human sign-off.
</div>
"""
            render_html(standards_html)

    # Recent Governance Activity
    st.markdown("### Recent Governance Activity")
    recent_activity = insights.get("recent_activity", [])

    if not recent_activity:
        st.info("No review activity logged yet. Click 'Review New Content' above to audit your first campaign asset.")
    else:
        for act in recent_activity:
            rec_badge = render_disposition_badge(act["recommendation"])
            act_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.85rem 1.25rem; margin-bottom: 0.65rem; display: flex; justify-content: space-between; align-items: center;">
    <div>
        <div style="font-weight: 700; color: #1E1B4B; font-size: 0.95rem;">{act['title']}</div>
        <div style="font-size: 0.82rem; color: #64748B;">
            Channel: <b>{act['channel']}</b> &bull; Format: <b>{act['content_type']}</b> &bull; Audited: {act['created_at'][:16].replace('T', ' ')} UTC
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
            st.markdown("**Load Standard Campaign Templates:**")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                if st.button("⚠️ Promotional Offer (Conditional Pricing)", use_container_width=True):
                    st.session_state["cr_title"] = "Festival Flash Sale Ad"
                    st.session_state["cr_content"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
                    st.session_state["cr_evidence"] = ""
                    st.session_state["cr_channel"] = "Instagram"
                    st.session_state["cr_type"] = "advertisement"
                    st.rerun()

            with col_p2:
                if st.button("✔ Standard Brand Awareness Copy", use_container_width=True):
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
                if st.button("📄 Promotional Offer with Verified Evidence", use_container_width=True):
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
                help="Enter marketing copy to audit against brand rules and contextual AI checks."
            )

            st.session_state["cr_evidence"] = st.text_area(
                "Supporting Evidence / Authorization Codes / URLs (Optional)",
                value=st.session_state["cr_evidence"],
                height=70,
                help="Provide promotional authorization codes, clinical study citations, or documentation URLs."
            )

            col_btn1, col_btn2 = st.columns([3, 1])
            with col_btn2:
                if st.button("Analyze Content & Proceed →", type="primary", use_container_width=True):
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
                            # Re-running on existing submission
                            sub = get_submission_by_id(st.session_state["cr_sub_id"])

                        with st.spinner("Executing deterministic rules & contextual analysis..."):
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
            if st.button("← Return to Step 1"):
                st.session_state["review_step"] = 1
                st.rerun()
        else:
            with st.container(border=True):
                st.markdown(f"#### Step 2: Policy Analysis Report — {sub.title} (v{sub.current_version_number})")

                # Recommendation banner
                badge_html = render_disposition_badge(run.overall_recommendation)
                banner_html = f"""
<div style="background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; padding: 1.15rem 1.4rem; margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;">
        <div>{badge_html}</div>
        <div style="font-size: 0.85rem; color: #64748B;">
            Engine Mode: <b>{run.ai_provider_mode}</b> | Guideline: <code>{run.guideline_version_id}</code>
        </div>
    </div>
    <div style="font-size: 0.95rem; color: #1E293B; line-height: 1.6; white-space: pre-wrap;">
        <b>Executive Rationale:</b><br>{run.summary}
    </div>
</div>
"""
                render_html(banner_html)

                # Severity counters
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric(label="CRITICAL BLOCKERS", value=run.critical_count)
                with m2:
                    st.metric(label="HIGH SEVERITY", value=run.high_count)
                with m3:
                    st.metric(label="MEDIUM ISSUES", value=run.medium_count)
                with m4:
                    st.metric(label="LOW / ADVISORY", value=run.low_count)

                st.markdown("### Itemized Policy Findings")
                if not run.findings:
                    st.success("✔ No policy violations detected. Content satisfies all active brand rules.")
                else:
                    for idx, f in enumerate(run.findings):
                        border_class = "finding-crit" if f.severity == "CRITICAL" else ("finding-high" if f.severity == "HIGH" else ("finding-med" if f.severity == "MEDIUM" else "finding-low"))
                        finding_html = f"""
<div class="finding-box {border_class}">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
        <span style="font-weight: 700; color: #1E1B4B; font-size: 0.98rem;">#{idx+1} [{f.severity}] {f.rule_title}</span>
        <span style="font-size: 0.78rem; background: #F1F5F9; color: #334155; padding: 3px 10px; border-radius: 4px; font-weight: 600;">{f.category} &bull; Impact: <b>{f.disposition_impact}</b></span>
    </div>
    <div style="font-size: 0.92rem; color: #1E293B; margin-bottom: 4px;"><b>Matched Text:</b> <code style="color: #DC2626; background: #FEF2F2; font-size: 0.9rem; padding: 2px 6px;">{f.matched_text}</code></div>
    <div style="font-size: 0.9rem; color: #475569; margin-bottom: 4px;"><b>Policy Explanation:</b> {f.explanation}</div>
    <div style="font-size: 0.9rem; color: #0F766E; margin-bottom: 4px;"><b>Brand Condition:</b> {f.expected_condition}</div>
    <div style="font-size: 0.9rem; color: #B45309; margin-bottom: 4px;"><b>Recommended Correction:</b> {f.recommended_correction}</div>
    <div style="font-size: 0.8rem; color: #64748B; margin-top: 5px;"><b>Verification State:</b> <code>{f.verification_state}</code> | <b>Source:</b> {f.source}</div>
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
            if st.button("← Return to Step 1"):
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
            if st.button("← Return to Step 1"):
                st.session_state["review_step"] = 1
                st.rerun()
        else:
            with st.container(border=True):
                st.markdown(f"#### Step 4: Human Governance Decision — {sub.title} (v{sub.current_version_number})")

                rec_badge = render_disposition_badge(run.overall_recommendation)
                sub_meta_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
    <div>{rec_badge}</div>
    <div style="font-size: 0.85rem; color: #64748B;">
        Status: <b>{sub.current_status}</b> | Version: <b>v{sub.current_version_number}</b> | Channel: <b>{sub.channel}</b>
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
                        valid_tag = "<span style='color: #059669; font-weight: 700;'>[ACTIVE APPROVAL]</span>" if d.is_currently_valid else "<span style='color: #DC2626; font-weight: 700;'>[REVOKED BY CONTENT EDIT]</span>"
                        dec_html = f"""
<div style="font-size: 0.88rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.65rem 0.85rem; border-radius: 6px; margin-bottom: 6px;">
    <b>{d.decision}</b> by <b>{d.reviewer_name}</b> ({d.reviewer_role}) at {d.created_at[:16].replace('T', ' ')} UTC &bull; {valid_tag}<br>
    <i>Rationale:</i> {d.reviewer_comments}
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

                st.info("Governance Policy: Editing approved content automatically revokes the prior approval for the new draft and mandates revalidation.")

            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b1:
                if st.button("← Back to Corrections", use_container_width=True):
                    st.session_state["review_step"] = 3
                    st.rerun()
            with col_b3:
                if st.button("Start Fresh Review", use_container_width=True):
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

    st.markdown(f"Displaying **{len(submissions)}** content record(s) in review queue.")

    if not submissions:
        st.info("No content records matching the selected filter.")
    else:
        for sub in submissions:
            latest_run = get_latest_review_run_for_submission(sub.id)
            latest_rev = get_latest_revision(sub.id)
            decisions = get_decisions_for_submission(sub.id)
            rec_badge = render_disposition_badge(latest_run.overall_recommendation if latest_run else "REVIEW")

            with st.expander(f"📌 {sub.title} ({sub.content_type} • {sub.channel}) — Status: {sub.current_status} (v{sub.current_version_number})", expanded=False):
                sub_meta_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
    <div>{rec_badge}</div>
    <div style="font-size: 0.85rem; color: #64748B;">ID: <code>{sub.id}</code> | Created: {sub.created_at[:16].replace('T', ' ')} UTC</div>
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
                    st.markdown("#### Decision History")
                    for d in decisions:
                        valid_tag = "<span style='color: #059669; font-weight: 700;'>[ACTIVE APPROVAL]</span>" if d.is_currently_valid else "<span style='color: #DC2626; font-weight: 700;'>[REVOKED BY CONTENT EDIT]</span>"
                        dec_html = f"""
<div style="font-size: 0.88rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.65rem 0.85rem; border-radius: 6px; margin-bottom: 6px;">
    <b>{d.decision}</b> by <b>{d.reviewer_name}</b> ({d.reviewer_role}) at {d.created_at[:16].replace('T', ' ')} UTC &bull; {valid_tag}<br>
    <i>Rationale:</i> {d.reviewer_comments}
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

                st.info("Governance Policy: Editing approved content automatically revokes the prior approval for the new draft and mandates revalidation.")


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
            st.info("Sample Brand Profile: Nivara Pro is an illustrative premium wellness and daily performance brand profile used to demonstrate policy enforcement, conditional promotional checks, and evidence verification.")

        with st.container(border=True):
            st.markdown(f"### {brand.name} — {brand.tagline}")
            st.markdown(f"**Active Policy Version:** `{guideline.version_label}` | **Industry:** {brand.industry}")
            st.markdown(brand.description)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            with st.container(border=True):
                st.markdown("#### Tone of Voice")
                st.markdown(guideline.tone_of_voice)
        with col_g2:
            with st.container(border=True):
                st.markdown("#### Target Audience")
                st.markdown(guideline.target_audience)

        st.markdown(f"### Active Deterministic Brand Rules ({len(guideline.rules)} rules configured)")
        for r in guideline.rules:
            sev_color = "#DC2626" if r.severity == "CRITICAL" else ("#EA580C" if r.severity == "HIGH" else ("#D97706" if r.severity == "MEDIUM" else "#0F766E"))
            blocks_tag = "<span style='color: #DC2626; font-weight: 700;'>[BLOCKS APPROVAL / HOLD]</span>" if r.blocks_approval else "<span style='color: #D97706; font-weight: 600;'>[REVIEW ONLY]</span>"

            rule_html = f"""
<div class="finding-box" style="border-left: 4px solid {sev_color};">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
        <span style="font-weight: 700; color: #1E1B4B; font-size: 0.98rem;">[{r.severity}] {r.title}</span>
        <span style="font-size: 0.8rem;">Category: <b>{r.category}</b> &bull; {blocks_tag}</span>
    </div>
    <div style="font-size: 0.88rem; color: #475569; margin-bottom: 4px;"><b>Trigger Pattern:</b> <code>{r.pattern}</code> | <b>Rule Type:</b> <code>{r.rule_type}</code></div>
    <div style="font-size: 0.9rem; color: #334155; margin-bottom: 4px;"><b>Description:</b> {r.description}</div>
    <div style="font-size: 0.88rem; color: #0F766E;"><b>Mandated Fix:</b> {r.suggested_fix}</div>
</div>
"""
            render_html(rule_html)

        render_divider("❖")
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
# SECTION 5: INSIGHTS
# =============================================================
elif st.session_state["active_tab"] == "Insights":
    st.markdown("## Governance Analytics & Recurring Risk Intelligence")

    insights = get_governance_insights()
    pass_ratio = (insights['pass_count'] / max(insights['total_submissions'], 1)) * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.metric(label="TOTAL ASSETS AUDITED", value=insights['total_submissions'])
    with c2:
        with st.container(border=True):
            st.metric(label="CLEAN PASS RATE", value=f"{pass_ratio:.0f}%")
    with c3:
        with st.container(border=True):
            st.metric(label="BLOCKED VIOLATIONS (HOLD)", value=insights['hold_count'])
    with c4:
        with st.container(border=True):
            st.metric(label="HUMAN APPROVED", value=insights['approved_count'])

    render_divider("❖")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown("### Top Frequently Triggered Brand Rules")
        if not insights['top_rules']:
            st.info("No rule violations logged yet.")
        else:
            for r in insights['top_rules']:
                rule_stat_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.85rem 1rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #D97706;">
    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1E1B4B; font-size: 0.95rem;">
        <span>{r['rule_title']}</span>
        <span style="color: #D97706;">{r['trigger_count']} times</span>
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 3px;">
        Category: {r['category']} &bull; Severity: {r['severity']}
    </div>
</div>
"""
                render_html(rule_stat_html)

    with col_i2:
        st.markdown("### Repeated Unsupported Claim Patterns")
        if not insights['unsupported_patterns']:
            st.info("No repeated unsupported patterns detected.")
        else:
            for p in insights['unsupported_patterns']:
                claim_stat_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.85rem 1rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #DC2626;">
    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1E1B4B; font-size: 0.95rem;">
        <code>{p['matched_text']}</code>
        <span style="color: #DC2626;">Flagged {p['count']}x</span>
    </div>
    <div style="font-size: 0.82rem; color: #64748B; margin-top: 3px;">
        Category: {p['category']} &bull; Requires empirical proof or promotional authorization
    </div>
</div>
"""
                render_html(claim_stat_html)

    st.markdown("### Policy Findings by Category")
    cat_items = insights.get("category_breakdown", {})
    if cat_items:
        cols = st.columns(len(cat_items))
        for idx, (cat, cnt) in enumerate(cat_items.items()):
            with cols[idx]:
                with st.container(border=True):
                    st.metric(label=cat.upper(), value=cnt)


# =============================================================
# SECTION 6: REVIEW HISTORY & AUDIT TRAIL
# =============================================================
elif st.session_state["active_tab"] == "Review History":
    st.markdown("## Immutable Governance Audit Trail")
    st.markdown("Every draft submission, automated policy check, human approval decision, and approval invalidation is recorded in a tamper-resistant SQLite audit log with exact UTC timestamps.")

    audit_events = get_audit_trail(limit=50)

    if not audit_events:
        st.info("No audit records found in the database.")
    else:
        for ev in audit_events:
            color = "#0F766E"
            if "INVALIDATED" in ev.event_type:
                color = "#DC2626"
            elif "DECISION" in ev.event_type:
                color = "#D97706"
            elif "SUBMISSION" in ev.event_type:
                color = "#1E1B4B"

            asset_str = f" &bull; <b>Asset ID:</b> <code>{ev.submission_id}</code>" if ev.submission_id else ""
            ev_html = f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid {color}; padding: 0.85rem 1.15rem; border-radius: 6px; margin-bottom: 0.65rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-weight: 700; color: {color}; font-size: 0.92rem;">[{ev.event_type}]</span>
        <span style="font-size: 0.8rem; color: #94A3B8;">{ev.created_at[:19].replace('T', ' ')} UTC</span>
    </div>
    <div style="font-size: 0.92rem; color: #334155; margin-bottom: 4px;">{ev.description}</div>
    <div style="font-size: 0.8rem; color: #64748B;"><b>Actor:</b> {ev.actor}{asset_str}</div>
</div>
"""
            render_html(ev_html)
