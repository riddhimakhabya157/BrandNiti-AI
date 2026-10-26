"""Review workflow orchestrator and state management for BrandNiti AI.
Coordinates deterministic verification, AI contextual audit, disposition evaluation,
result persistence, and human approval workflow transitions.
"""
from typing import Optional, List, Dict, Any, Tuple
from database.queries import (
    get_brand_by_id,
    get_active_guideline_version,
    get_guideline_version_by_id,
    get_submission_by_id,
    get_latest_revision,
    save_review_run,
    create_content_revision,
    record_approval_decision
)
from models.submission import ReviewRun, Finding, Submission, ContentRevision, ApprovalDecision
from services.rule_engine import run_deterministic_rules
from services.decision_engine import evaluate_disposition
from services.ai_review import (
    is_ai_available,
    generate_live_gemini_review,
    generate_sample_fallback_review
)

def run_content_review_workflow(
    submission_id: str,
    revision_id: Optional[str] = None,
    guideline_version_id: Optional[str] = None
) -> ReviewRun:
    """Executes the full review workflow:
    1. Loads submission and target revision.
    2. Loads active or specified brand guideline.
    3. Executes deterministic brand-rule validation.
    4. Executes AI-assisted contextual audit (Live Gemini if key available, else Sample Mode).
    5. Merges findings and removes duplicate issues.
    6. Computes PASS / REVIEW / HOLD recommendation via decision engine.
    7. Persists review run and findings in SQLite.
    """
    sub = get_submission_by_id(submission_id)
    if not sub:
        raise ValueError(f"Submission '{submission_id}' not found.")

    # Target revision
    if revision_id:
        from database.queries import get_revision_by_id
        target_rev = get_revision_by_id(revision_id)
    else:
        target_rev = get_latest_revision(submission_id)

    if not target_rev:
        raise ValueError(f"No revision found for submission '{submission_id}'.")

    # Load guideline
    if guideline_version_id:
        guideline = get_guideline_version_by_id(guideline_version_id)
    else:
        guideline = get_active_guideline_version(sub.brand_id)

    if not guideline:
        raise ValueError(f"No active guideline found for brand '{sub.brand_id}'.")

    # 1. Deterministic Rule Checks (Zero Hallucination)
    det_findings = run_deterministic_rules(
        content_text=target_rev.content_text,
        guideline=guideline,
        supporting_evidence=target_rev.supporting_evidence
    )

    # 2. AI-assisted Contextual Audit
    ai_findings: List[Finding] = []
    ai_summary = ""
    suggested_copy = target_rev.content_text
    ai_mode = "SAMPLE_MOCK_FALLBACK"
    ai_performed = False

    if is_ai_available():
        try:
            ai_findings, ai_summary, suggested_copy = generate_live_gemini_review(
                content_text=target_rev.content_text,
                channel=sub.channel,
                content_type=sub.content_type,
                guideline=guideline,
                supporting_evidence=target_rev.supporting_evidence
            )
            ai_mode = "LIVE_GEMINI"
            ai_performed = True
        except Exception as e:
            # Graceful error handling: catch rate limits, timeouts, network errors
            # Fall back to sample mode with clear explanation
            ai_findings, ai_summary, suggested_copy = generate_sample_fallback_review(
                content_text=target_rev.content_text,
                channel=sub.channel,
                content_type=sub.content_type,
                guideline=guideline,
                supporting_evidence=target_rev.supporting_evidence
            )
            ai_mode = "SAMPLE_MOCK_FALLBACK"
            ai_summary = f"[LIVE GEMINI ERROR - FALLBACK TO SAMPLE]: {str(e)[:100]}. " + ai_summary
            ai_performed = False
    else:
        # Transparent fallback mode clearly labeled
        ai_findings, ai_summary, suggested_copy = generate_sample_fallback_review(
            content_text=target_rev.content_text,
            channel=sub.channel,
            content_type=sub.content_type,
            guideline=guideline,
            supporting_evidence=target_rev.supporting_evidence
        )
        ai_mode = "SAMPLE_MOCK_FALLBACK"
        ai_performed = False

    # 3. Deduplicate findings:
    # If deterministic checks already flagged a specific text, don't duplicate with generic AI finding
    merged_findings: List[Finding] = list(det_findings)
    existing_matched_texts = {f.matched_text.lower() for f in det_findings if f.matched_text}

    for aif in ai_findings:
        if aif.matched_text and aif.matched_text.lower() in existing_matched_texts:
            continue
        merged_findings.append(aif)

    # 4. Compute overall recommendation via Decision Engine
    overall_rec, summary_rationale, det_passed = evaluate_disposition(merged_findings)

    combined_summary = f"{summary_rationale}\n\nAI Contextual Evaluation ({ai_mode}): {ai_summary}"

    # 5. Save Review Run and Findings to SQLite
    run = save_review_run(
        submission_id=submission_id,
        revision_id=target_rev.id,
        guideline_version_id=guideline.id,
        overall_recommendation=overall_rec,
        deterministic_passed=det_passed,
        ai_review_performed=ai_performed,
        ai_provider_mode=ai_mode,
        summary=combined_summary,
        suggested_revised_copy=suggested_copy,
        findings=merged_findings
    )

    return run

def submit_human_decision(
    submission_id: str,
    revision_id: str,
    review_run_id: str,
    decision: str, # 'APPROVED', 'CHANGES_REQUESTED', 'REJECTED'
    reviewer_name: str,
    reviewer_role: str,
    reviewer_comments: str
) -> ApprovalDecision:
    """Records human approval decision. Validates state transition and stores immutable audit trail."""
    valid_decisions = ["APPROVED", "CHANGES_REQUESTED", "REJECTED"]
    if decision not in valid_decisions:
        raise ValueError(f"Invalid decision '{decision}'. Must be one of {valid_decisions}.")

    return record_approval_decision(
        submission_id=submission_id,
        revision_id=revision_id,
        review_run_id=review_run_id,
        decision=decision,
        reviewer_name=reviewer_name,
        reviewer_role=reviewer_role,
        reviewer_comments=reviewer_comments
    )
