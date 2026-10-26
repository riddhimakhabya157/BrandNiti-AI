"""BrandNiti AI — Every Brand Message. On Brand.
AI-Powered Brand Governance: Create Confidently. Review Intelligently. Publish Responsibly.

Enterprise SaaS Application.
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
    create_new_guideline_version,
    create_brand
)
from services.review_workflow import run_content_review_workflow, submit_human_decision
from services.ai_review import is_ai_available, get_gemini_api_key
from styles.theme import (
    CUSTOM_CSS,
    render_header,
    render_disposition_badge,
    render_divider
)

# Helper for strictly unindented HTML rendering (guarantees CommonMark never converts HTML into code blocks)
def render_html(html_str: str):
    """Renders HTML strictly unindented so CommonMark never treats it as a code block."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="BrandNiti AI | Enterprise Brand Governance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure Database & Seed Fixture
init_database()
seed_nivara_pro_if_not_exists()

# Initialize session state for navigation
if "active_nav" not in st.session_state:
    st.session_state["active_nav"] = "Overview"

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
with st.sidebar:
    sidebar_brand_html = """
<div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid rgba(226, 232, 240, 0.15);">
    <div style="font-family: 'Cinzel', serif; font-size: 1.35rem; font-weight: 700; color: #FFFFFF; letter-spacing: 0.04em;">
        BRAND<span style="color: #F59E0B;">NITI</span> AI
    </div>
    <div style="font-size: 0.82rem; color: #99F6E4; font-weight: 500; margin-top: 2px;">
        Enterprise Governance Studio
    </div>
    <div style="font-size: 0.74rem; color: #CBD5E1; margin-top: 4px;">
        Every Brand Message. On Brand.
    </div>
</div>
"""
    render_html(sidebar_brand_html)

    nav_options = [
        "Overview",
        "New Content Review",
        "Review Queue",
        "Brand Guidelines",
        "Insights",
        "Review History"
    ]

    current_idx = nav_options.index(st.session_state["active_nav"]) if st.session_state["active_nav"] in nav_options else 0
    selected_nav = st.radio(
        "Governance Navigation",
        nav_options,
        index=current_idx,
        label_visibility="collapsed"
    )
    st.session_state["active_nav"] = selected_nav

    st.markdown("---")

    # Engine Status indicator
    ai_status = is_ai_available()
    if ai_status:
        ai_badge_html = """
<div style="background: rgba(15, 118, 110, 0.25); border: 1px solid #14B8A6; border-radius: 6px; padding: 0.55rem 0.75rem; margin-bottom: 0.75rem;">
    <div style="font-size: 0.82rem; font-weight: 700; color: #99F6E4;">🟢 AI Engine: Connected</div>
    <div style="font-size: 0.72rem; color: #E2E8F0; margin-top: 2px;">Gemini Contextual Analysis Active</div>
</div>
"""
        render_html(ai_badge_html)
    else:
        det_badge_html = """
<div style="background: rgba(217, 119, 6, 0.2); border: 1px solid #F59E0B; border-radius: 6px; padding: 0.55rem 0.75rem; margin-bottom: 0.75rem;">
    <div style="font-size: 0.82rem; font-weight: 700; color: #FDE68A;">🟡 Deterministic Engine: Active</div>
    <div style="font-size: 0.72rem; color: #E2E8F0; margin-top: 2px;">Rule-based checks with deterministic fallback</div>
</div>
"""
        render_html(det_badge_html)

    sidebar_footer_html = """
<div style="font-size: 0.76rem; color: #94A3B8; line-height: 1.5; padding: 0.4rem 0;">
    <b>Active Profile:</b> Nivara Pro (Sample)<br>
    <b>Storage:</b> SQLite Persistent Store<br>
    <b>Policy Mode:</b> Strict Verification
</div>
<div style="margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid rgba(226, 232, 240, 0.1); font-size: 0.7rem; color: #64748B;">
    BrandNiti AI Enterprise Edition<br>
    Powered by TWIN SOCH
</div>
"""
    render_html(sidebar_footer_html)


# =============================================================
# SECTION 1: OVERVIEW (PRACTICAL GOVERNANCE DASHBOARD)
# =============================================================
if st.session_state["active_nav"] == "Overview":
    render_header("Executive Governance Dashboard")

    # Welcome Banner with direct action
    col_w1, col_w2 = st.columns([3, 1])
    with col_w1:
        st.markdown(
            "**Welcome to the BrandNiti AI Governance Portal.** Pre-publication verification, deterministic guideline enforcement, "
            "and traceable human approval workflows for marketing teams, corporate communications, and external agencies."
        )
    with col_w2:
        if st.button("✨ Review New Content", type="primary", use_container_width=True):
            st.session_state["active_nav"] = "New Content Review"
            st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # High-level stats from SQLite
    insights = get_governance_insights()
    hold_count = insights['recommendations'].get('HOLD', 0)
    approved_count = insights['human_decisions'].get('APPROVED', 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="TOTAL ASSETS AUDITED", value=insights['total_submissions'])
    with c2:
        st.metric(label="AWAITING REVIEW", value=insights['pending_reviews'])
    with c3:
        st.metric(label="POLICY BLOCKERS (HOLD)", value=hold_count)
    with c4:
        st.metric(label="HUMAN APPROVED", value=approved_count)

    render_divider("❖")

    # Governance Framework & Disposition Model
    col_left, col_right = st.columns([3, 2])

    with col_left:
        with st.container(border=True):
            st.markdown("#### Closed-Loop Brand Governance Architecture")
            st.markdown(
                "BrandNiti AI protects brand integrity and legal compliance by verifying marketing messages against configured brand rules before publication.\n\n"
                "- **1. Content Ingestion & Channel Context:** Ingest copy across Instagram, LinkedIn, Google Ads, Email, and Web with version tracking.\n"
                "- **2. Deterministic Validation Layer:** Non-negotiable checks on prohibited terminology, conditional pricing (₹799 vs standard ₹999), and required legal disclaimers.\n"
                "- **3. Contextual AI Review:** Evaluates tone mismatch, hyperbolic promises, and unverified efficacy claims without hallucinating sources.\n"
                "- **4. Explainable Disposition (HOLD > REVIEW > PASS):** Instant itemized findings with exact matched text, policy rules, and suggested corrections.\n"
                "- **5. Human Approval Workflow:** Traceable decisions with automatic invalidation if approved copy is subsequently edited."
            )

    with col_right:
        with st.container(border=True):
            st.markdown("#### System Disposition Standards")
            pass_badge = render_disposition_badge("PASS")
            review_badge = render_disposition_badge("REVIEW")
            hold_badge = render_disposition_badge("HOLD")

            standards_html = f"""
<div style="font-size: 0.9rem; line-height: 1.6;">
    <div style="margin-bottom: 8px;">{pass_badge}<br><span style="color: #334155; font-size: 0.84rem;">All mandatory policies satisfied. Advisory clear to proceed.</span></div>
    <div style="margin-bottom: 8px;">{review_badge}<br><span style="color: #334155; font-size: 0.84rem;">Unverified claim, conditional promo, or tone review required.</span></div>
    <div style="margin-bottom: 8px;">{hold_badge}<br><span style="color: #334155; font-size: 0.84rem;">Mandatory prohibition violated. Blocked pending correction.</span></div>
</div>
<div style="background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 6px; padding: 0.6rem 0.8rem; margin-top: 10px; font-size: 0.8rem; color: #92400E;">
    <b>Governance Rule:</b> System recommendations are advisory. Official publication requires authorized human sign-off.
</div>
"""
            render_html(standards_html)

    # Recent Governance Activity
    st.markdown("### Recent Governance Activity")
    recent_activity = insights.get("recent_activity", [])

    if not recent_activity:
        st.info("No review activity logged yet. Submit your first campaign asset in 'New Content Review' to view real-time governance activity.")
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
# SECTION 2: NEW CONTENT REVIEW (THE CORE WORKFLOW)
# =============================================================
elif st.session_state["active_nav"] == "New Content Review":
    render_header("Content Review & Compliance Verification")

    brands = get_all_brands()
    brand_map = {b.name: b.id for b in brands}
    brand_names = list(brand_map.keys())

    # Standard Campaign Presets
    st.markdown("**Standard Campaign Templates:** Load sample copy to test deterministic & contextual policy verification")

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        if st.button("⚠️ Promotional Offer (Conditional Pricing)", use_container_width=True):
            st.session_state["form_title"] = "Festival Flash Sale Ad"
            st.session_state["form_content"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
            st.session_state["form_evidence"] = ""
            st.session_state["form_channel"] = "Instagram"
            st.session_state["form_type"] = "advertisement"
            st.rerun()

    with col_p2:
        if st.button("✔ Standard Brand Awareness Copy", use_container_width=True):
            st.session_state["form_title"] = "Daily Clarity & Wellness Post"
            st.session_state["form_content"] = (
                "Support your daily mental clarity with Nivara Pro for ₹999. "
                "Formulated with natural adaptogens to assist your daily wellness journey.\n\n"
                "*Disclaimer: Results may vary based on individual lifestyle, diet, and physiological factors."
            )
            st.session_state["form_evidence"] = "Formulation Quality Certificate: ISO-9001-NIVARA"
            st.session_state["form_channel"] = "LinkedIn"
            st.session_state["form_type"] = "social_post"
            st.rerun()

    with col_p3:
        if st.button("📄 Promotional Offer with Verified Evidence", use_container_width=True):
            st.session_state["form_title"] = "Authorized Seasonal Email Offer"
            st.session_state["form_content"] = (
                "Exclusive festive offer: Claim Nivara Pro for ₹799 during our festive celebration! "
                "Formulated to support your daily wellness journey.\n\n"
                "*Results may vary based on individual lifestyle and physiological factors."
            )
            st.session_state["form_evidence"] = "Authorized Promo Code: DIWALI-2026-PROMO-AUTH (Valid until Nov 10)"
            st.session_state["form_channel"] = "Email"
            st.session_state["form_type"] = "email"
            st.rerun()

    # Content Intake Form
    with st.form("new_content_form"):
        st.markdown("### 1. Asset Metadata")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            title_val = st.text_input("Content Title*", value=st.session_state.get("form_title", "Festive Campaign Launch Copy"))
            brand_choice = st.selectbox("Applicable Brand Guidelines*", brand_names, index=0)
            channel_val = st.selectbox("Publishing Channel*", ["Instagram", "LinkedIn", "Google Ads", "Email", "Website", "Print"], index=0)
        with col_f2:
            type_val = st.selectbox("Content Format*", ["social_post", "advertisement", "email", "blog_article", "product_copy"], index=1)
            campaign_val = st.text_input("Campaign Name (Optional)", value="Q4 Festive Campaign")
            creator_val = st.text_input("Creator / Agency Attribution", value="Brand Marketing Lead")

        st.markdown("### 2. Content Draft & Documentation")
        content_val = st.text_area(
            "Content Body Text*",
            value=st.session_state.get("form_content", "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"),
            height=140,
            help="Enter marketing copy to audit against brand rules and contextual AI checks."
        )

        evidence_val = st.text_area(
            "Approved Supporting Evidence / Authorization References (Optional)",
            value=st.session_state.get("form_evidence", ""),
            height=70,
            help="Provide promotional approval codes, clinical trial citations, or documentation URLs."
        )

        submit_audit = st.form_submit_button("🔍 Run Full Governance Audit", type="primary", use_container_width=True)

    if submit_audit:
        if not content_val.strip() or not title_val.strip():
            st.error("Please provide both a Content Title and Content Body to proceed.")
        else:
            selected_brand_id = brand_map[brand_choice]
            new_sub = create_submission(
                title=title_val.strip(),
                content_type=type_val,
                channel=channel_val,
                campaign_name=campaign_val.strip(),
                brand_id=selected_brand_id,
                initial_content=content_val.strip(),
                supporting_evidence=evidence_val.strip(),
                creator=creator_val.strip()
            )
            st.session_state["active_submission_id"] = new_sub.id

            with st.spinner("Analyzing content against brand rules & contextual standards..."):
                review_run = run_content_review_workflow(new_sub.id)
                st.session_state["latest_review_run"] = review_run

            st.success(f"Audit completed successfully! Asset registered as ID: {new_sub.id}")

    # Display Results if active run exists
    active_sub_id = st.session_state.get("active_submission_id")
    if active_sub_id:
        sub = get_submission_by_id(active_sub_id)
        run = get_latest_review_run_for_submission(active_sub_id)

        if sub and run:
            render_divider("◆")
            st.markdown(f"## Compliance Audit Report: {sub.title} (v{sub.current_version_number})")

            # Top Recommendation Banner
            badge_html = render_disposition_badge(run.overall_recommendation)
            banner_html = f"""
<div style="background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <div>{badge_html}</div>
        <div style="font-size: 0.85rem; color: #64748B;">
            Engine: <b>{run.ai_provider_mode}</b> | Guideline: <code>{run.guideline_version_id}</code>
        </div>
    </div>
    <div style="font-size: 0.95rem; color: #1E293B; line-height: 1.6; white-space: pre-wrap;">
        <b>Executive Rationale:</b><br>{run.summary}
    </div>
</div>
"""
            render_html(banner_html)

            # Severity Counters
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric(label="CRITICAL BLOCKERS", value=run.critical_count)
            with m2:
                st.metric(label="HIGH SEVERITY", value=run.high_count)
            with m3:
                st.metric(label="MEDIUM ISSUES", value=run.medium_count)
            with m4:
                st.metric(label="LOW / ADVISORY", value=run.low_count)

            # Itemized Findings
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

            # Suggested Revision Diff
            st.markdown("### Suggested Revision & Comparison")
            c_orig, c_sugg = st.columns(2)
            latest_rev = get_latest_revision(active_sub_id)
            with c_orig:
                st.markdown("**Submitted Copy (v1):**")
                with st.container(border=True):
                    st.text(latest_rev.content_text if latest_rev else "")

            with c_sugg:
                st.markdown("**On-Brand Suggested Copy:**")
                with st.container(border=True):
                    st.text(run.suggested_revised_copy)

            # Inline Revision Editor
            st.markdown("### Edit & Re-audit")
            with st.expander(f"✏️ Refine Content & Submit Version v{sub.current_version_number + 1}", expanded=False):
                with st.form("revise_form"):
                    revised_text_input = st.text_area(
                        "Revised Content Copy",
                        value=run.suggested_revised_copy,
                        height=130
                    )
                    revised_evidence_input = st.text_area(
                        "Updated Supporting Evidence / Citations",
                        value=latest_rev.supporting_evidence if latest_rev else "",
                        height=60
                    )
                    rev_summary_input = st.text_input("Revision Summary", value="Applied on-brand pricing and required variation disclaimer")
                    submit_new_rev = st.form_submit_button("Submit Revised Version & Re-run Audit", type="primary")

                if submit_new_rev:
                    new_revision = create_content_revision(
                        submission_id=active_sub_id,
                        new_content_text=revised_text_input.strip(),
                        supporting_evidence=revised_evidence_input.strip(),
                        change_summary=rev_summary_input.strip(),
                        actor="Content Creator"
                    )
                    new_run = run_content_review_workflow(active_sub_id, revision_id=new_revision.id)
                    st.success(f"Published Version v{new_revision.version_number}! New Recommendation: {new_run.overall_recommendation}")
                    st.rerun()


# =============================================================
# SECTION 3: REVIEW QUEUE
# =============================================================
elif st.session_state["active_nav"] == "Review Queue":
    render_header("Content Approval & Governance Queue")

    col_q1, col_q2 = st.columns([1, 2])
    with col_q1:
        status_filter = st.selectbox(
            "Filter by Status",
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
        st.info("No content records matching the selected status filter.")
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

                st.markdown("#### Record Official Human Approval")
                with st.form(f"decision_form_{sub.id}"):
                    c_rev1, c_rev2 = st.columns(2)
                    with c_rev1:
                        rev_name = st.text_input("Reviewer Name", value="Priya Sharma", key=f"rname_{sub.id}")
                        rev_role = st.selectbox("Reviewer Authority", ["Brand Governance Director", "Legal Counsel", "Marketing Lead"], key=f"rrole_{sub.id}")
                    with c_rev2:
                        decision_choice = st.radio("Decision", ["APPROVED", "CHANGES_REQUESTED", "REJECTED"], key=f"dchoice_{sub.id}")
                        rev_comments = st.text_area("Reviewer Rationale & Notes", value="Verified against brand guidelines and statutory disclaimers.", height=70, key=f"rcomm_{sub.id}")

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
elif st.session_state["active_nav"] == "Brand Guidelines":
    render_header("Brand Guidelines & Policy Configuration")

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
elif st.session_state["active_nav"] == "Insights":
    render_header("Governance Analytics & Recurring Risk Intelligence")

    insights = get_governance_insights()
    pass_ratio = (insights['recommendations'].get('PASS', 0) / max(insights['total_submissions'], 1)) * 100
    hold_count = insights['recommendations'].get('HOLD', 0)
    approved_count = insights['human_decisions'].get('APPROVED', 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="TOTAL ASSETS AUDITED", value=insights['total_submissions'])
    with c2:
        st.metric(label="CLEAN PASS RATE", value=f"{pass_ratio:.0f}%")
    with c3:
        st.metric(label="BLOCKED VIOLATIONS (HOLD)", value=hold_count)
    with c4:
        st.metric(label="HUMAN APPROVED", value=approved_count)

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
                st.metric(label=cat.upper(), value=cnt)


# =============================================================
# SECTION 6: REVIEW HISTORY & AUDIT TRAIL
# =============================================================
elif st.session_state["active_nav"] == "Review History":
    render_header("Immutable Governance Audit Trail")

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
