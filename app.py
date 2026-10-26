"""BrandNiti AI — Every Brand Message. On Brand.
Team TWIN SOCH — Two Minds. One Vision.
Round 2 Hackathon Functional Prototype.

Main Streamlit Application Entrypoint.
"""
import os
import sys
from pathlib import Path

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = str(Path(__file__).parent.resolve())
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import streamlit as st
from datetime import datetime, timezone

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

# Initialize Streamlit Page Config
st.set_page_config(
    page_title="BrandNiti AI | Every Brand Message. On Brand.",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure Database & Demo Fixture
init_database()
seed_nivara_pro_if_not_exists()

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="font-family: 'Cinzel', serif; font-size: 1.4rem; font-weight: 700; color: #F59E0B; letter-spacing: 0.05em;">
            BRAND<span style="color: #FFFFFF;">NITI</span> AI
        </div>
        <div style="font-size: 0.78rem; color: #99F6E4; font-weight: 500;">Every Brand Message. On Brand.</div>
        <div style="font-size: 0.68rem; color: #FDE68A; background: rgba(217, 119, 6, 0.25); border: 1px solid rgba(245, 158, 11, 0.4); padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">
            TWIN SOCH • Round 2 Prototype
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_choice = st.radio(
        "Navigation",
        [
            "1. Overview",
            "2. New Content Review",
            "3. Review Queue",
            "4. Brand Guidelines",
            "5. Insights",
            "6. Review History"
        ],
        index=0
    )

    st.markdown("---")
    # AI Status indicator in sidebar
    ai_status = is_ai_available()
    if ai_status:
        st.success("🟢 Gemini AI: Connected")
    else:
        st.info("🟡 Gemini AI: Sample Mode\n(Deterministic rules active + illustrative fallback)")

    st.markdown("""
    <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 1rem; line-height: 1.4;">
        <b>Demo Brand:</b> Nivara Pro (Fictional)<br>
        <b>Storage:</b> SQLite Persistent Store<br>
        <b>Integrity:</b> Zero Hallucinated Claims
    </div>
    """, unsafe_allow_html=True)


# =============================================================
# SECTION 1: OVERVIEW
# =============================================================
if nav_choice == "1. Overview":
    render_header("Executive Governance Dashboard")

    # High-level stats from SQLite
    insights = get_governance_insights()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="num">{insights['total_submissions']}</div>
            <div class="lbl">Total Submissions</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-tile" style="border-top: 3px solid #F59E0B;">
            <div class="num" style="color: #D97706;">{insights['pending_reviews']}</div>
            <div class="lbl">Pending Action</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        pass_count = insights['recommendations'].get('PASS', 0)
        st.markdown(f"""
        <div class="metric-tile" style="border-top: 3px solid #10B981;">
            <div class="num" style="color: #059669;">{pass_count}</div>
            <div class="lbl">Pass Clear</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        hold_count = insights['recommendations'].get('HOLD', 0)
        st.markdown(f"""
        <div class="metric-tile" style="border-top: 3px solid #EF4444;">
            <div class="num" style="color: #DC2626;">{hold_count}</div>
            <div class="lbl">Hold Blocked</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        approved_count = insights['human_decisions'].get('APPROVED', 0)
        st.markdown(f"""
        <div class="metric-tile" style="border-top: 3px solid #0F766E;">
            <div class="num" style="color: #0F766E;">{approved_count}</div>
            <div class="lbl">Human Approved</div>
        </div>
        """, unsafe_allow_html=True)

    render_divider("❖")

    # Round 1 Demo Walkthrough & Architecture Card
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("""
        <div class="bn-card">
            <div class="bn-card-title">What is BrandNiti AI?</div>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.55;">
                In the era of rapid content creation across in-house teams, external agencies, and generative AI tools, 
                enterprises face substantial brand and legal risk: inconsistent messaging, outdated price promotions, 
                unsupported efficacy guarantees, and fragmented approval trails.
            </p>
            <p style="color: #1E1B4B; font-size: 0.92rem; font-weight: 600; line-height: 1.55;">
                BrandNiti AI establishes a closed-loop governance pipeline:
            </p>
            <div style="background-color: #F8FAFC; border-radius: 8px; padding: 0.85rem; border: 1px dashed #CBD5E1; font-size: 0.88rem;">
                <b>1. Ingest & Version</b>: Content submitted with channel & target guidelines.<br>
                <b>2. Deterministic Audit</b>: Instant check against non-negotiable prohibited phrases, pricing rules, and disclaimers.<br>
                <b>3. Contextual AI Review</b>: Deep contextual tone, superlative, and evidence requirement checks (Gemini integration).<br>
                <b>4. Explainable Disposition</b>: Strict <code>HOLD</code> &gt; <code>REVIEW</code> &gt; <code>PASS</code> decision model.<br>
                <b>5. Human Approval Workflow</b>: Traceable audit logs with automatic approval invalidation upon content edit.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="bn-card bn-card-gold">
            <div class="bn-card-title">Demo Scenario: "Nivara Pro" Fictional Brand</div>
            <p style="color: #475569; font-size: 0.9rem;">
                To evaluate the prototype immediately without manual setup, the system is seeded with 
                <b>Nivara Pro</b>—a fictional wellness brand illustrating our Hackathon Round 1 case study.
            </p>
            <ul style="color: #334155; font-size: 0.88rem; line-height: 1.6;">
                <li><b>Standard Price:</b> ₹999</li>
                <li><b>Promotional Price:</b> ₹799 (strictly requires documented active promo authorization)</li>
                <li><b>Prohibited Phrasing:</b> "Guaranteed results", "100% cure" (Strict HOLD)</li>
                <li><b>Evidence Requirement:</b> Turnaround speed claims like "in 24 hours" require clinical/lab citations.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="bn-card" style="border-left-color: #1E1B4B;">
            <div class="bn-card-title">Quick Actions for Judges</div>
            <p style="color: #64748B; font-size: 0.85rem;">Click below to explore the core review flow directly:</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Audit Round 1 Risky Ad Sample", use_container_width=True, type="primary"):
            # Create the sample risky submission if not already there, and switch to New Content Review
            sub = create_submission(
                title="Flash Sale Launch Post (Demo)",
                content_type="social_post",
                channel="Instagram",
                campaign_name="Diwali Flash 2026",
                brand_id=NIVARA_BRAND_ID,
                initial_content="Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!",
                supporting_evidence="",
                creator="Growth Marketing Agency"
            )
            st.session_state["active_submission_id"] = sub.id
            st.session_state["quick_loaded_text"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
            st.success(f"Loaded demo submission '{sub.title}'! Navigate to '2. New Content Review' or '3. Review Queue'.")

        if st.button("📋 Inspect Nivara Pro Brand Guidelines", use_container_width=True):
            st.info("Select '4. Brand Guidelines' in the sidebar to inspect or modify active governance rules.")

        if st.button("📊 View Governance Insights", use_container_width=True):
            st.info("Select '5. Insights' to analyze historical rule frequency and unsupported claim patterns.")

        st.markdown("""
        <div style="background-color: #FAF5FF; border: 1px solid #E9D5FF; border-radius: 8px; padding: 0.85rem; margin-top: 1rem;">
            <div style="font-weight: 700; color: #6B21A8; font-size: 0.88rem; margin-bottom: 4px;">Indian Heritage × Modern AI</div>
            <div style="font-size: 0.82rem; color: #4A044E; line-height: 1.45;">
                Crafted with an Indian-rooted design philosophy: deep indigo contrast, peacock teal precision, 
                and subtle geometric jaali accents, paired with enterprise-grade deterministic governance.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================
# SECTION 2: NEW CONTENT REVIEW
# =============================================================
elif nav_choice == "2. New Content Review":
    render_header("Content Audit & Explainable Verification Studio")

    brands = get_all_brands()
    brand_map = {b.name: b.id for b in brands}
    brand_names = list(brand_map.keys())

    # Demo Quick Presets
    st.markdown("""
    <div style="background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; padding: 0.85rem 1.2rem; margin-bottom: 1rem;">
        <span style="font-weight: 700; color: #1E1B4B; font-size: 0.88rem; margin-right: 12px;">Preset Demo Content:</span>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        if st.button("⚠️ Load Risky Round 1 Ad", use_container_width=True):
            st.session_state["form_title"] = "Flash Promo Instagram Ad"
            st.session_state["form_content"] = "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"
            st.session_state["form_evidence"] = ""
            st.session_state["form_channel"] = "Instagram"
            st.session_state["form_type"] = "advertisement"
            st.rerun()

    with col_p2:
        if st.button("✔ Load Compliant Brand Post", use_container_width=True):
            st.session_state["form_title"] = "Daily Wellness Morning Post"
            st.session_state["form_content"] = (
                "Support your daily mental clarity with Nivara Pro for ₹999. "
                "Formulated with natural adaptogens to assist your daily wellness journey.\n\n"
                "*Disclaimer: Results may vary based on individual lifestyle, diet, and physiological factors."
            )
            st.session_state["form_evidence"] = "Batch Formulation Cert: ISO-9001-NIVARA"
            st.session_state["form_channel"] = "LinkedIn"
            st.session_state["form_type"] = "social_post"
            st.rerun()

    with col_p3:
        if st.button("📄 Load Promo with Valid Evidence", use_container_width=True):
            st.session_state["form_title"] = "Authorized Seasonal Email Promo"
            st.session_state["form_content"] = (
                "Exclusive festival offer: Claim Nivara Pro for ₹799 during our Diwali celebration! "
                "Formulated to support your daily wellness journey.\n\n"
                "*Results may vary based on individual lifestyle and physiological factors."
            )
            st.session_state["form_evidence"] = "Authorized Promo Code: DIWALI-2026-PROMO-AUTH (Valid until Nov 10)"
            st.session_state["form_channel"] = "Email"
            st.session_state["form_type"] = "email"
            st.rerun()

    # Content Submission Form
    with st.form("new_content_form"):
        st.markdown("### Content Metadata")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            title_val = st.text_input("Content Title*", value=st.session_state.get("form_title", "Nivara Pro Campaign Copy"))
            brand_choice = st.selectbox("Brand Guidelines Profile*", brand_names, index=0)
            channel_val = st.selectbox("Intended Channel*", ["Instagram", "LinkedIn", "Google Ads", "Email", "Website", "Print"], index=0)
        with col_f2:
            type_val = st.selectbox("Content Type*", ["social_post", "advertisement", "email", "blog_article", "product_copy"], index=1)
            campaign_val = st.text_input("Campaign Name (Optional)", value="Q4 Festive Launch")
            creator_val = st.text_input("Creator / Agency Identity", value="Brand Marketing Team")

        st.markdown("### Content Body")
        content_val = st.text_area(
            "Draft Content Copy*",
            value=st.session_state.get("form_content", "Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"),
            height=130,
            help="Enter marketing copy to be audited against brand rules and contextual AI checks."
        )

        evidence_val = st.text_area(
            "Approved Supporting Evidence / Documentation References (Optional)",
            value=st.session_state.get("form_evidence", ""),
            height=70,
            help="Include clinical study links, promotional authorization codes, or trial references."
        )

        submit_audit = st.form_submit_button("🔍 Run Full Governance Audit", type="primary", use_container_width=True)

    if submit_audit:
        if not content_val.strip() or not title_val.strip():
            st.error("Please provide both a Content Title and Content Body to proceed.")
        else:
            selected_brand_id = brand_map[brand_choice]
            # 1. Save submission to SQLite
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

            # 2. Execute review workflow
            with st.spinner("Running deterministic rules & AI contextual analysis..."):
                review_run = run_content_review_workflow(new_sub.id)
                st.session_state["latest_review_run"] = review_run

            st.success(f"Audit completed! Submission saved as ID: {new_sub.id}")

    # Display Results if active run exists
    active_sub_id = st.session_state.get("active_submission_id")
    if active_sub_id:
        sub = get_submission_by_id(active_sub_id)
        run = get_latest_review_run_for_submission(active_sub_id)

        if sub and run:
            render_divider("◆")
            st.markdown(f"## Audit Results: {sub.title} (Version v{sub.current_version_number})")

            # Top Disposition Banner
            rec = run.overall_recommendation
            badge_html = render_disposition_badge(rec)
            st.markdown(f"""
            <div style="background: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; padding: 1.25rem 1.5rem; margin-bottom: 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>{badge_html}</div>
                    <div style="font-size: 0.85rem; color: #64748B;">
                        AI Mode: <b>{run.ai_provider_mode}</b> | Guideline: <code>{run.guideline_version_id}</code>
                    </div>
                </div>
                <div style="font-size: 0.95rem; color: #1E1B4B; line-height: 1.5; white-space: pre-wrap;">
                    <b>Executive Rationale:</b><br>{run.summary}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Severity Counts
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-tile" style="border-left: 4px solid #DC2626;">
                    <div class="num" style="color: #DC2626;">{run.critical_count}</div>
                    <div class="lbl">Critical Blockers</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-tile" style="border-left: 4px solid #EA580C;">
                    <div class="num" style="color: #EA580C;">{run.high_count}</div>
                    <div class="lbl">High Severity</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-tile" style="border-left: 4px solid #F59E0B;">
                    <div class="num" style="color: #D97706;">{run.medium_count}</div>
                    <div class="lbl">Medium Issues</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-tile" style="border-left: 4px solid #0F766E;">
                    <div class="num" style="color: #0F766E;">{run.low_count}</div>
                    <div class="lbl">Low / Advisory</div>
                </div>
                """, unsafe_allow_html=True)

            # Detailed Findings
            st.markdown("### Itemized Explainable Findings")
            if not run.findings:
                st.info("No policy violations or evidence requirements detected. Clean content!")
            else:
                for idx, f in enumerate(run.findings):
                    # Severity color border
                    border_class = "finding-crit" if f.severity == "CRITICAL" else ("finding-high" if f.severity == "HIGH" else ("finding-med" if f.severity == "MEDIUM" else "finding-low"))
                    st.markdown(f"""
                    <div class="finding-box {border_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-weight: 700; color: #1E1B4B; font-size: 0.95rem;">
                                #{idx+1} [{f.severity}] {f.rule_title}
                            </span>
                            <span style="font-size: 0.75rem; background: #F1F5F9; color: #475569; padding: 2px 8px; border-radius: 4px;">
                                {f.category} • Impact: <b>{f.disposition_impact}</b>
                            </span>
                        </div>
                        <div style="font-size: 0.88rem; color: #334155; margin-bottom: 4px;">
                            <b>Matched Copy:</b> <code style="color: #DC2626; background: #FEF2F2;">{f.matched_text}</code>
                        </div>
                        <div style="font-size: 0.88rem; color: #475569; margin-bottom: 4px;">
                            <b>Governance Explanation:</b> {f.explanation}
                        </div>
                        <div style="font-size: 0.85rem; color: #0F766E; margin-bottom: 4px;">
                            <b>Policy Requirement:</b> {f.expected_condition}
                        </div>
                        <div style="font-size: 0.85rem; color: #B45309;">
                            <b>Recommended Correction:</b> {f.recommended_correction}
                        </div>
                        <div style="font-size: 0.78rem; color: #64748B; margin-top: 4px;">
                            <b>Verification State:</b> <code>{f.verification_state}</code> | <b>Source:</b> {f.source}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Comparison and Suggested Revision
            st.markdown("### Suggested Revision & Diff")
            c_orig, c_sugg = st.columns(2)
            latest_rev = get_latest_revision(active_sub_id)
            with c_orig:
                st.markdown("**Original Submitted Text (v1):**")
                st.markdown(f"""
                <div class="diff-box">{latest_rev.content_text if latest_rev else ""}</div>
                """, unsafe_allow_html=True)

            with c_sugg:
                st.markdown("**Suggested Compliant Copy:**")
                st.markdown(f"""
                <div class="diff-box" style="border-color: #0F766E; background-color: #F0FDF4;">{run.suggested_revised_copy}</div>
                """, unsafe_allow_html=True)

            # Revision Action Form
            st.markdown("### Revise and Resubmit")
            with st.expander("✏️ Edit and Submit Revised Version (v2)", expanded=False):
                with st.form("revise_form"):
                    revised_text_input = st.text_area(
                        "Revised Content",
                        value=run.suggested_revised_copy,
                        height=120
                    )
                    revised_evidence_input = st.text_area(
                        "Updated Supporting Evidence",
                        value=latest_rev.supporting_evidence if latest_rev else "",
                        height=60
                    )
                    rev_summary_input = st.text_input("Change Summary", value="Applied recommended on-brand phrasing and variation disclaimer")
                    submit_new_rev = st.form_submit_button("Submit Revised Version for Re-audit", type="primary")

                if submit_new_rev:
                    new_revision = create_content_revision(
                        submission_id=active_sub_id,
                        new_content_text=revised_text_input.strip(),
                        supporting_evidence=revised_evidence_input.strip(),
                        change_summary=rev_summary_input.strip(),
                        actor="Content Creator"
                    )
                    # Run review on new revision
                    new_run = run_content_review_workflow(active_sub_id, revision_id=new_revision.id)
                    st.success(f"Created Version v{new_revision.version_number}! New Recommendation: {new_run.overall_recommendation}")
                    st.rerun()


# =============================================================
# SECTION 3: REVIEW QUEUE
# =============================================================
elif nav_choice == "3. Review Queue":
    render_header("Human Governance & Approval Queue")

    col_q1, col_q2 = st.columns([1, 3])
    with col_q1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["ALL", "SUBMITTED", "IN_REVIEW", "CHANGES_REQUESTED", "APPROVED", "REJECTED"],
            index=0
        )

    submissions = get_all_submissions(status_filter=status_filter)

    st.markdown(f"Showing **{len(submissions)}** submission(s) in review queue.")

    if not submissions:
        st.info("No submissions matching the selected status filter.")
    else:
        for sub in submissions:
            latest_run = get_latest_review_run_for_submission(sub.id)
            latest_rev = get_latest_revision(sub.id)
            decisions = get_decisions_for_submission(sub.id)

            rec_badge = render_disposition_badge(latest_run.overall_recommendation if latest_run else "REVIEW")

            with st.expander(f"📌 {sub.title} ({sub.content_type} • {sub.channel}) — Status: {sub.current_status} (v{sub.current_version_number})", expanded=False):
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>{rec_badge}</div>
                    <div style="font-size: 0.85rem; color: #64748B;">ID: <code>{sub.id}</code> | Created: {sub.created_at[:16]}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Current Content Copy:**")
                st.markdown(f"""
                <div class="diff-box">{latest_rev.content_text if latest_rev else ""}</div>
                """, unsafe_allow_html=True)

                if latest_rev and latest_rev.supporting_evidence:
                    st.markdown(f"**Submitted Evidence / Citations:** `{latest_rev.supporting_evidence}`")

                if latest_run:
                    st.markdown(f"**Automated System Assessment ({latest_run.overall_recommendation}):**")
                    st.markdown(f"""
                    <div style="font-size: 0.88rem; color: #334155; background: #F8FAFC; padding: 0.75rem; border-radius: 6px;">
                        {latest_run.summary}
                    </div>
                    """, unsafe_allow_html=True)

                # Previous Human Decisions
                if decisions:
                    st.markdown("#### Previous Human Decision History")
                    for d in decisions:
                        valid_tag = "<span style='color: #059669;'>[CURRENTLY VALID]</span>" if d.is_currently_valid else "<span style='color: #DC2626;'>[INVALIDATED BY CONTENT EDIT]</span>"
                        st.markdown(f"""
                        <div style="font-size: 0.85rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.5rem 0.75rem; border-radius: 6px; margin-bottom: 4px;">
                            <b>{d.decision}</b> by <b>{d.reviewer_name}</b> ({d.reviewer_role}) at {d.created_at[:16]} — {valid_tag}<br>
                            <i>Comments:</i> {d.reviewer_comments}
                        </div>
                        """, unsafe_allow_html=True)

                # Human Action Form
                st.markdown("#### Record Human Approval Decision")
                st.markdown("""
                <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 8px;">
                    <i>Note: Automated recommendations (PASS/REVIEW/HOLD) are advisory. Publication requires human sign-off.</i>
                </div>
                """, unsafe_allow_html=True)

                with st.form(f"decision_form_{sub.id}"):
                    c_rev1, c_rev2 = st.columns(2)
                    with c_rev1:
                        rev_name = st.text_input("Reviewer Name", value="Priya Sharma (Demo Reviewer)", key=f"rname_{sub.id}")
                        rev_role = st.selectbox("Reviewer Role", ["Brand Governance Director", "Legal Counsel", "Marketing Lead"], key=f"rrole_{sub.id}")
                    with c_rev2:
                        decision_choice = st.radio("Decision", ["APPROVED", "CHANGES_REQUESTED", "REJECTED"], key=f"dchoice_{sub.id}")
                        rev_comments = st.text_area("Reviewer Comments", value="Content verified against active policy rules.", height=70, key=f"rcomm_{sub.id}")

                    submit_dec = st.form_submit_button("Confirm Human Decision", type="primary")

                if submit_dec:
                    if not latest_run:
                        st.error("Cannot approve content before running an automated governance check.")
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
                        st.success(f"Decision '{decision_choice}' recorded! Audit event registered.")
                        st.rerun()

                # Invalidation Demonstration Notice
                st.markdown("---")
                st.markdown("""
                <div style="font-size: 0.82rem; color: #475569; background: #FFFBEB; padding: 0.6rem; border-radius: 6px; border: 1px solid #FDE68A;">
                    <b>Governance Rule:</b> Editing approved content automatically revokes the prior approval for the new draft and mandates revalidation.
                </div>
                """, unsafe_allow_html=True)


# =============================================================
# SECTION 4: BRAND GUIDELINES
# =============================================================
elif nav_choice == "4. Brand Guidelines":
    render_header("Brand Guideline Management & Rule Configuration")

    brands = get_all_brands()
    brand_map = {b.name: b.id for b in brands}
    brand_names = list(brand_map.keys())

    selected_brand_name = st.selectbox("Select Brand Profile", brand_names, index=0)
    selected_brand_id = brand_map[selected_brand_name]
    brand = get_brand_by_id(selected_brand_id)
    guideline = get_active_guideline_version(selected_brand_id)

    if brand and guideline:
        demo_banner = ""
        if brand.is_demo:
            demo_banner = """
            <div style="background-color: #FEF3C7; border: 1.5px solid #F59E0B; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; color: #92400E; font-size: 0.88rem;">
                <b>[FICTIONAL DEMONSTRATION DATA]</b> Nivara Pro is an illustrative brand created for Hackathon Round 2. 
                Not an actual company or verified commercial product.
            </div>
            """
        st.markdown(demo_banner, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="bn-card">
            <div class="bn-card-title">{brand.name} — {brand.tagline}</div>
            <div style="font-size: 0.88rem; color: #64748B; margin-bottom: 0.5rem;">
                Active Guideline Version: <b>{guideline.version_label}</b> | Industry: {brand.industry}
            </div>
            <div style="font-size: 0.9rem; color: #334155;">{brand.description}</div>
        </div>
        """, unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown(f"""
            <div class="bn-card" style="border-left-color: #0F766E;">
                <div style="font-weight: 700; color: #1E1B4B; margin-bottom: 4px;">Desired Tone of Voice</div>
                <div style="font-size: 0.9rem; color: #334155;">{guideline.tone_of_voice}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_g2:
            st.markdown(f"""
            <div class="bn-card" style="border-left-color: #D97706;">
                <div style="font-weight: 700; color: #1E1B4B; margin-bottom: 4px;">Target Audience</div>
                <div style="font-size: 0.9rem; color: #334155;">{guideline.target_audience}</div>
            </div>
            """, unsafe_allow_html=True)

        # Configured Rules Table
        st.markdown(f"### Active Deterministic Rules ({len(guideline.rules)} rules configured)")
        for r in guideline.rules:
            sev_color = "#DC2626" if r.severity == "CRITICAL" else ("#EA580C" if r.severity == "HIGH" else ("#D97706" if r.severity == "MEDIUM" else "#0F766E"))
            blocks_tag = "<span style='color: #DC2626; font-weight: 700;'>[BLOCKS APPROVAL / HOLD]</span>" if r.blocks_approval else "<span style='color: #D97706;'>[REVIEW ONLY]</span>"

            st.markdown(f"""
            <div class="finding-box" style="border-left: 4px solid {sev_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #1E1B4B; font-size: 0.92rem;">
                        [{r.severity}] {r.title}
                    </span>
                    <span style="font-size: 0.78rem;">
                        Category: <b>{r.category}</b> | {blocks_tag}
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #475569; margin-bottom: 4px;">
                    <b>Pattern:</b> <code>{r.pattern}</code> | <b>Rule Type:</b> <code>{r.rule_type}</code>
                </div>
                <div style="font-size: 0.85rem; color: #334155; margin-bottom: 4px;">
                    <b>Description:</b> {r.description}
                </div>
                <div style="font-size: 0.85rem; color: #0F766E;">
                    <b>Suggested Fix:</b> {r.suggested_fix}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Guideline Editor: Publish new guideline version
        render_divider("❖")
        st.markdown("### Update Guideline & Publish New Version")
        with st.expander(f"➕ Publish New Guideline Version (Current: v{guideline.version_number}.0)", expanded=False):
            with st.form("edit_guideline_form"):
                new_tone = st.text_input("Tone of Voice", value=guideline.tone_of_voice)
                new_aud = st.text_input("Target Audience", value=guideline.target_audience)
                changelog_text = st.text_input("Version Changelog / Notes", value="Updated pricing thresholds and added stricter medical claim filters")

                st.markdown("#### Add Custom Prohibited Phrase Rule")
                new_rule_title = st.text_input("Rule Title", value="Prohibit 'No Prescription Needed'")
                new_rule_pattern = st.text_input("Pattern / Keywords (pipe separated)", value="no prescription needed|no rx needed")
                new_rule_fix = st.text_input("Suggested Fix", value="Consult a qualified healthcare practitioner")

                publish_btn = st.form_submit_button("Publish New Guideline Version", type="primary")

            if publish_btn:
                # Build updated rules list
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
                # Add the new rule
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
                st.success(f"Published Guideline Version {new_gv.version_label}! Future content audits will apply this version.")
                st.rerun()


# =============================================================
# SECTION 5: INSIGHTS
# =============================================================
elif nav_choice == "5. Insights":
    render_header("Governance Analytics & Recurring Risk Insights")

    insights = get_governance_insights()

    # Metric Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="num">{insights['total_submissions']}</div>
            <div class="lbl">Total Submissions</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        pass_ratio = (
            (insights['recommendations'].get('PASS', 0) / max(insights['total_submissions'], 1)) * 100
        )
        st.markdown(f"""
        <div class="metric-tile">
            <div class="num" style="color: #059669;">{pass_ratio:.0f}%</div>
            <div class="lbl">Clean Pass Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        hold_count = insights['recommendations'].get('HOLD', 0)
        st.markdown(f"""
        <div class="metric-tile">
            <div class="num" style="color: #DC2626;">{hold_count}</div>
            <div class="lbl">Blocked on Hold</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="num" style="color: #0F766E;">{insights['human_decisions'].get('APPROVED', 0)}</div>
            <div class="lbl">Human Approved</div>
        </div>
        """, unsafe_allow_html=True)

    render_divider("❖")

    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown("### Most Frequently Triggered Brand Rules")
        if not insights['top_rules']:
            st.info("No rule violations logged yet. Audit content to view recurring trends.")
        else:
            for r in insights['top_rules']:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.85rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #D97706;">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1E1B4B; font-size: 0.9rem;">
                        <span>{r['rule_title']}</span>
                        <span style="color: #D97706;">{r['trigger_count']} times</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
                        Category: {r['category']} • Severity: {r['severity']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_i2:
        st.markdown("### Recurring Unsupported Claim Patterns")
        if not insights['unsupported_patterns']:
            st.info("No repeated claim patterns recorded.")
        else:
            for p in insights['unsupported_patterns']:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.85rem; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #DC2626;">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1E1B4B; font-size: 0.9rem;">
                        <code>{p['matched_text']}</code>
                        <span style="color: #DC2626;">Flagged {p['count']}x</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
                        Category: {p['category']} • Requires lab proof or promo authorization
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Category Breakdown & Recent Activity
    st.markdown("### Findings by Category Breakdown")
    cat_items = insights.get("category_breakdown", {})
    if cat_items:
        cols = st.columns(len(cat_items))
        for idx, (cat, cnt) in enumerate(cat_items.items()):
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-tile" style="padding: 0.75rem;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1E1B4B;">{cnt}</div>
                    <div style="font-size: 0.72rem; color: #64748B;">{cat}</div>
                </div>
                """, unsafe_allow_html=True)


# =============================================================
# SECTION 6: REVIEW HISTORY & AUDIT TRAIL
# =============================================================
elif nav_choice == "6. Review History":
    render_header("Immutable Governance Audit Trail")

    st.markdown("""
    <div style="font-size: 0.88rem; color: #475569; margin-bottom: 1rem;">
        Every submission, rule evaluation, human approval, and approval invalidation is recorded 
        in a tamper-resistant SQLite audit log with exact timestamps and version numbers.
    </div>
    """, unsafe_allow_html=True)

    audit_events = get_audit_trail(limit=50)

    if not audit_events:
        st.info("No audit events logged yet.")
    else:
        for ev in audit_events:
            color = "#0F766E"
            if "INVALIDATED" in ev.event_type:
                color = "#DC2626"
            elif "DECISION" in ev.event_type:
                color = "#D97706"
            elif "SUBMISSION" in ev.event_type:
                color = "#1E1B4B"

            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid {color}; padding: 0.85rem 1rem; border-radius: 6px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                    <span style="font-weight: 700; color: {color}; font-size: 0.88rem;">
                        [{ev.event_type}]
                    </span>
                    <span style="font-size: 0.78rem; color: #94A3B8;">
                        {ev.created_at[:19].replace('T', ' ')} UTC
                    </span>
                </div>
                <div style="font-size: 0.88rem; color: #334155; margin-bottom: 3px;">
                    {ev.description}
                </div>
                <div style="font-size: 0.78rem; color: #64748B;">
                    <b>Actor:</b> {ev.actor} {f"| <b>Submission:</b> <code>{ev.submission_id}</code>" if ev.submission_id else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
