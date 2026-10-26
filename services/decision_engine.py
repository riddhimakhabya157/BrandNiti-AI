"""Decision Engine for BrandNiti AI.
Computes the overall recommendation (PASS, REVIEW, HOLD) following
Round 1 governance hierarchy and strict precedence rules:
- HOLD takes precedence over REVIEW and PASS.
- Any unresolved mandatory prohibition or blocking rule forces HOLD.
- Any unverified claim, missing disclaimer, or ambiguous tone issue requires REVIEW.
- PASS is only awarded when all mandatory rules are satisfied with zero high-risk findings.
All recommendations are advisory; final publication requires human sign-off.
"""
from typing import List, Tuple
from models.submission import Finding

def evaluate_disposition(findings: List[Finding]) -> Tuple[str, str, bool]:
    """Evaluates findings to determine overall recommendation (PASS / REVIEW / HOLD),
    an explainable executive summary, and whether deterministic checks passed.
    
    Returns:
        (overall_recommendation, summary_rationale, deterministic_passed)
    """
    if not findings:
        return (
            "PASS",
            "Clear to Proceed: Content satisfies all active brand governance rules. Ready for final human approval.",
            True
        )

    hold_reasons = []
    review_reasons = []

    # Check for blocking conditions
    for f in findings:
        if f.disposition_impact == "HOLD" or f.severity == "CRITICAL":
            hold_reasons.append(f"• [{f.severity}] {f.rule_title}: {f.explanation}")
        elif f.disposition_impact == "REVIEW" or f.severity in ["HIGH", "MEDIUM"]:
            review_reasons.append(f"• [{f.severity}] {f.rule_title}: {f.explanation}")

    # HOLD takes absolute precedence
    if hold_reasons:
        summary = (
            f"HOLD — Blocked pending fix ({len(hold_reasons)} blocking violation(s)):\n"
            + "\n".join(hold_reasons[:3])
        )
        if len(hold_reasons) > 3:
            summary += f"\n...and {len(hold_reasons) - 3} other blocking issues."
        return ("HOLD", summary, False)

    # REVIEW is required if evidence or human assessment is needed
    if review_reasons:
        summary = (
            f"REVIEW — Needs verification ({len(review_reasons)} item(s) require verification or refinement):\n"
            + "\n".join(review_reasons[:3])
        )
        if len(review_reasons) > 3:
            summary += f"\n...and {len(review_reasons) - 3} other review items."
        return ("REVIEW", summary, True)

    # If only LOW or PASS advisory items remain
    return (
        "PASS",
        "PASS — Clear to proceed: All mandatory policies satisfied. No critical or unverified blockers identified.",
        True
    )
