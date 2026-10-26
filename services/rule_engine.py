"""Deterministic Brand Rule Engine for BrandNiti AI.
Performs deterministic, rule-based verification against active brand guidelines,
checking prohibited phrases, approved terminology, conditional pricing,
required disclaimers, and mandatory claim evidence.
"""
import re
import uuid
from typing import List, Dict, Any, Optional
from models.brand import GuidelineVersion, Rule
from models.submission import Finding

def clean_text_for_search(text: str) -> str:
    """Normalizes text for robust token and phrase matching."""
    return re.sub(r'\s+', ' ', text).strip()

def check_prohibited_phrases(content_text: str, rules: List[Rule]) -> List[Finding]:
    findings = []
    text_lower = content_text.lower()

    for rule in rules:
        if rule.rule_type != "prohibited_phrase":
            continue

        patterns = [p.strip() for p in rule.pattern.split("|") if p.strip()]
        for pat in patterns:
            # Case-insensitive phrase match
            escaped_pat = re.escape(pat.lower())
            match = re.search(r'\b' + escaped_pat + r'\b', text_lower, re.IGNORECASE)
            if match or pat.lower() in text_lower:
                # Extract exact matched substring from original text
                start_idx = text_lower.find(pat.lower())
                matched_span = content_text[start_idx:start_idx + len(pat)] if start_idx != -1 else pat

                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id=rule.id,
                    rule_title=rule.title,
                    category=rule.category,
                    severity=rule.severity,
                    disposition_impact="HOLD" if rule.blocks_approval else "REVIEW",
                    matched_text=matched_span,
                    explanation=f"Prohibited phrasing detected: '{matched_span}'. {rule.description}",
                    expected_condition=f"Content must not contain prohibited phrasing '{pat}'.",
                    supporting_evidence_reference="",
                    recommended_correction=rule.suggested_fix,
                    verification_state="VIOLATION_CONFIRMED"
                ))
                break  # Don't duplicate for alternate pipe patterns in the same rule
    return findings

def check_approved_terminology(content_text: str, rules: List[Rule]) -> List[Finding]:
    findings = []
    for rule in rules:
        if rule.rule_type != "approved_terminology":
            continue

        # Pattern holds improper variants, e.g. "NivaraPro|nivara pro|Nivara-Pro"
        patterns = [p.strip() for p in rule.pattern.split("|") if p.strip()]
        for pat in patterns:
            # Check if this exact variant is present in text
            if pat in content_text:
                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id=rule.id,
                    rule_title=rule.title,
                    category=rule.category,
                    severity=rule.severity,
                    disposition_impact="REVIEW",
                    matched_text=pat,
                    explanation=f"Non-standard brand terminology detected: '{pat}'. {rule.description}",
                    expected_condition=f"Brand terminology should follow approved style guidelines.",
                    supporting_evidence_reference="",
                    recommended_correction=rule.suggested_fix,
                    verification_state="VIOLATION_CONFIRMED"
                ))
    return findings

def check_pricing_and_promotions(content_text: str, guideline: GuidelineVersion, supporting_evidence: str) -> List[Finding]:
    findings = []
    evidence_lower = (supporting_evidence or "").lower()

    # Regex to find Indian Rupee amounts: ₹799, Rs. 799, INR 799, Rs 799, or standalone 799
    price_matches = re.finditer(r'(?:₹|rs\.?|inr)\s*([0-9,]+)', content_text, re.IGNORECASE)
    detected_prices = []
    for m in price_matches:
        raw_num = m.group(1).replace(",", "")
        try:
            detected_prices.append((int(raw_num), m.group(0)))
        except ValueError:
            continue

    # Also detect bare currency figures matching conditional promo prices
    for promo in guideline.conditional_promotions:
        promo_p = promo.get("promo_price_inr")
        if not promo_p:
            continue
        # Check if bare number or currency formatted exists
        promo_regex = rf'(?:₹|rs\.?|inr)?\s*\b{promo_p}\b'
        match = re.search(promo_regex, content_text, re.IGNORECASE)
        if match:
            matched_str = match.group(0).strip()
            # Check if valid documented evidence is provided
            # The system must not claim promo is active unless stored evidence establishes it!
            has_promo_evidence = any(
                keyword in evidence_lower
                for keyword in ["promo", "authorized", "campaign", "approved promo", "discount code", "authorization"]
            ) and len(evidence_lower.strip()) > 5

            if not has_promo_evidence:
                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id="rule_nivara_price_promo_799",
                    rule_title="Conditional Promotional Price Verification Required",
                    category="Pricing & Offers",
                    severity="HIGH",
                    disposition_impact="REVIEW",
                    matched_text=matched_str,
                    explanation=(
                        f"Promotional price '{matched_str}' detected. Under brand governance policy, "
                        f"promotional pricing requires confirmation of an active, authorized marketing promotion. "
                        f"No documented promotional authorization was verified in submission metadata."
                    ),
                    expected_condition=promo.get("condition_description", "Requires active promotional authorization."),
                    supporting_evidence_reference=supporting_evidence if supporting_evidence else "None provided",
                    recommended_correction=f"Provide an authorized promotional campaign code / documentation link, or update to standard price of ₹999.",
                    verification_state="REQUIRES_DOCUMENTED_EVIDENCE"
                ))
            else:
                # Evidence was supplied! We note it as verified under submitted evidence
                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id="rule_nivara_price_promo_799",
                    rule_title="Conditional Promotional Price Documented",
                    category="Pricing & Offers",
                    severity="LOW",
                    disposition_impact="PASS",
                    matched_text=matched_str,
                    explanation=f"Promotional price '{matched_str}' referenced with submitted promotional evidence.",
                    expected_condition="Promotional evidence verified against submission metadata.",
                    supporting_evidence_reference=supporting_evidence,
                    recommended_correction="Maintain documentation in campaign audit folder.",
                    verification_state="VERIFIED_COMPLIANT"
                ))

    return findings

def check_evidence_requirements(content_text: str, guideline: GuidelineVersion, supporting_evidence: str) -> List[Finding]:
    findings = []
    text_lower = content_text.lower()
    evidence_lower = (supporting_evidence or "").lower()

    # Check speed / efficacy triggers (e.g., 24 hours, overnight, guaranteed)
    speed_triggers = ["24 hours", "in 24 hours", "overnight", "within hours", "instant results"]
    for trig in speed_triggers:
        if trig in text_lower:
            start_idx = text_lower.find(trig)
            matched_span = content_text[start_idx:start_idx + len(trig)]

            has_clinical_evidence = any(
                keyword in evidence_lower
                for keyword in ["clinical", "trial", "lab", "study", "report", "certified", "http"]
            ) and len(evidence_lower.strip()) > 8

            if not has_clinical_evidence:
                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id="rule_nivara_speed_claim_evidence",
                    rule_title="Unverified Timeframe & Efficacy Claim",
                    category="Claims & Evidence",
                    severity="HIGH",
                    disposition_impact="REVIEW",
                    matched_text=matched_span,
                    explanation=(
                        f"Timeframe claim '{matched_span}' requires empirical or clinical trial backing. "
                        f"No supporting trial or lab evidence was cited in the submission."
                    ),
                    expected_condition="All timeframe/speed claims require verifiable scientific evidence or documented lab trials.",
                    supporting_evidence_reference=supporting_evidence if supporting_evidence else "None provided",
                    recommended_correction="Attach valid clinical trial citation or rephrase to sustainable lifestyle terminology without hard timeframes.",
                    verification_state="REQUIRES_DOCUMENTED_EVIDENCE"
                ))

    return findings

def check_required_disclaimers(content_text: str, guideline: GuidelineVersion) -> List[Finding]:
    findings = []
    text_lower = content_text.lower()

    # If content makes promotional or performance claims, check for disclaimers
    has_claim = any(kw in text_lower for kw in ["today", "buy", "results", "effective", "performance", "wellness", "cure", "guaranteed", "₹", "rs"])

    if has_claim:
        for disc in guideline.required_disclaimers:
            disc_text = disc.get("disclaimer_text", "")
            # Check for core phrasing e.g. "results may vary"
            if "results may vary" not in text_lower and "*disclaimer" not in text_lower:
                findings.append(Finding(
                    id=f"det_{uuid.uuid4().hex[:8]}",
                    review_run_id="",
                    source="DETERMINISTIC",
                    rule_id="rule_nivara_required_disclaimer",
                    rule_title="Missing Mandatory Results Disclaimer",
                    category="Legal & Compliance",
                    severity="MEDIUM",
                    disposition_impact="REVIEW",
                    matched_text="[Missing disclaimer in content]",
                    explanation="Promotional content making efficacy assertions must include a variation disclaimer.",
                    expected_condition=f"Include standard disclaimer: '{disc_text}'",
                    supporting_evidence_reference="",
                    recommended_correction=f"Append the required disclaimer to footer: '{disc_text}'",
                    verification_state="REQUIRES_DOCUMENTED_EVIDENCE"
                ))
    return findings

def run_deterministic_rules(
    content_text: str,
    guideline: GuidelineVersion,
    supporting_evidence: str = ""
) -> List[Finding]:
    """Runs all deterministic brand-rule validations.
    Returns list of Findings without any LLM hallucination."""
    all_findings: List[Finding] = []

    # 1. Prohibited phrases (Critical / Blocking)
    all_findings.extend(check_prohibited_phrases(content_text, guideline.rules))

    # 2. Approved terminology checks
    all_findings.extend(check_approved_terminology(content_text, guideline.rules))

    # 3. Pricing and conditional promotion checks
    all_findings.extend(check_pricing_and_promotions(content_text, guideline, supporting_evidence))

    # 4. Evidence requirement checks for timeframe/efficacy
    all_findings.extend(check_evidence_requirements(content_text, guideline, supporting_evidence))

    # 5. Required disclaimers check
    all_findings.extend(check_required_disclaimers(content_text, guideline))

    return all_findings
