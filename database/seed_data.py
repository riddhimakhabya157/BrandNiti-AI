"""Seed fixture for fictional demonstration brand 'Nivara Pro'."""
import json
import uuid
from datetime import datetime, timezone
from database.connection import get_db_connection

NIVARA_BRAND_ID = "brand_nivara_pro"
NIVARA_GUIDELINE_ID = "gv_nivara_pro_v1"

def seed_nivara_pro_if_not_exists():
    """Seeds the fictional Nivara Pro brand and baseline rules if they do not exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM brands WHERE id = ?", (NIVARA_BRAND_ID,))
        row = cursor.fetchone()
        if row:
            return  # Already seeded

        now = datetime.now(timezone.utc).isoformat()

        # 1. Insert Nivara Pro brand
        cursor.execute("""
            INSERT INTO brands (id, name, tagline, description, industry, is_demo, active_guideline_version_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            NIVARA_BRAND_ID,
            "Nivara Pro",
            "Clarity, Balance & Daily Performance",
            "[FICTIONAL DEMO BRAND] Nivara Pro is an illustrative premium wellness and productivity supplement brand used strictly for hackathon demonstration and policy testing. Not a real product.",
            "Health & Wellness (Fictional Demo)",
            1, # is_demo = True
            NIVARA_GUIDELINE_ID,
            now,
            now
        ))

        # 2. Insert Guideline Version 1.0
        approved_prices = [
            {"item": "Nivara Pro Single Pack (30-day)", "price_inr": 999, "currency": "INR", "condition": "Standard approved retail price"}
        ]
        conditional_promotions = [
            {
                "item": "Nivara Pro Flash / Seasonal Promotion",
                "promo_price_inr": 799,
                "requires_active_promo": True,
                "required_evidence_type": "promotional_authorization",
                "condition_description": "Promotional price of ₹799 is only authorized during active corporate campaigns with documented promotional approval code."
            }
        ]
        required_disclaimers = [
            {
                "trigger_topic": "health_and_speed_claims",
                "disclaimer_text": "*Disclaimer: Results may vary based on individual lifestyle, diet, and physiological factors. Statements have not been evaluated by FDA/FSSAI.",
                "placement": "Mandatory in footer or marked with asterisk"
            }
        ]
        evidence_requirements = [
            {
                "claim_pattern": "speed_or_efficacy_claims",
                "evidence_type": "clinical_study_or_promotional_authorization",
                "description": "Any claim specifying speed of action (e.g., '24 hours', 'instant') or guaranteed efficacy requires documented empirical evidence reference."
            }
        ]

        cursor.execute("""
            INSERT INTO guideline_versions (
                id, brand_id, version_number, version_label, tone_of_voice, target_audience,
                approved_prices, conditional_promotions, required_disclaimers, evidence_requirements,
                is_active, changelog, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            NIVARA_GUIDELINE_ID,
            NIVARA_BRAND_ID,
            1,
            "v1.0 - Baseline Governance Policy (Demo)",
            "Empathetic, scientifically grounded, transparent, encouraging, non-sensational",
            "Working professionals, fitness enthusiasts, and wellness-focused adults (Ages 24-45)",
            json.dumps(approved_prices),
            json.dumps(conditional_promotions),
            json.dumps(required_disclaimers),
            json.dumps(evidence_requirements),
            1,
            "Initial seeded brand rules for Hackathon Round 2 demonstration",
            now
        ))

        # 3. Insert Specific Seed Rules
        seed_rules = [
            (
                "rule_nivara_price_regular",
                NIVARA_GUIDELINE_ID,
                "price_check",
                "Pricing & Offers",
                "HIGH",
                "₹999",
                "Standard Approved Retail Price",
                "Standard approved product price is ₹999. Unauthorized deviations or unapproved discounts are not permitted.",
                "Verify standard price is set to ₹999.",
                0, 1, "{}"
            ),
            (
                "rule_nivara_price_promo_799",
                NIVARA_GUIDELINE_ID,
                "price_check",
                "Pricing & Offers",
                "HIGH",
                "799",
                "Conditional Promotional Price ₹799 Check",
                "Promotional price ₹799 requires confirmation of an active, authorized marketing promotion and documentation reference.",
                "Attach authorized promo reference or restore standard price of ₹999.",
                1, 1, '{"trigger_price": 799, "currency": "INR", "requires_promo_evidence": true}'
            ),
            (
                "rule_nivara_prohibit_guaranteed_results",
                NIVARA_GUIDELINE_ID,
                "prohibited_phrase",
                "Legal & Compliance",
                "CRITICAL",
                "guaranteed results",
                "Prohibition on Absolute Outcome Guarantees",
                "The phrase 'guaranteed results' or absolute efficacy guarantees are strictly prohibited under company governance policy unless authorized under a clinical validation exemption.",
                "Replace with compliant phrasing such as 'Formulated to support your daily wellness journey' and include the mandatory asterisk disclaimer.",
                1, 1, "{}"
            ),
            (
                "rule_nivara_prohibit_cure_claims",
                NIVARA_GUIDELINE_ID,
                "prohibited_phrase",
                "Legal & Compliance",
                "CRITICAL",
                "100% cure|miracle cure|permanently eliminates",
                "Prohibition on Unsubstantiated Medical Claims",
                "Wellness products must never claim to cure, treat, or permanently eliminate medical conditions.",
                "Remove medical treatment claims and focus on functional lifestyle support.",
                1, 1, "{}"
            ),
            (
                "rule_nivara_speed_claim_evidence",
                NIVARA_GUIDELINE_ID,
                "evidence_requirement",
                "Claims & Evidence",
                "HIGH",
                "24 hours|in 24 hours|overnight|instant results",
                "Timeframe & Speed Claim Evidence Requirement",
                "Specific turnaround time claims such as 'in 24 hours' or 'overnight' require verifiable empirical trial citations or must be removed.",
                "Provide lab trial citation or replace with 'gradual, sustainable improvement with daily use'.",
                1, 1, "{}"
            ),
            (
                "rule_nivara_required_disclaimer",
                NIVARA_GUIDELINE_ID,
                "disclaimer_check",
                "Legal & Compliance",
                "MEDIUM",
                "Results may vary",
                "Mandatory Variation Disclaimer",
                "Promotional content making efficacy or benefit assertions must incorporate the standard variation disclaimer.",
                "Add footnote: '*Results may vary based on individual lifestyle, diet, and physiological factors.'",
                0, 1, "{}"
            ),
            (
                "rule_nivara_approved_term_nivara_pro",
                NIVARA_GUIDELINE_ID,
                "approved_terminology",
                "Terminology",
                "LOW",
                "NivaraPro|nivara pro|Nivara-Pro",
                "Standard Brand Capitalization",
                "The brand name should be formatted strictly as 'Nivara Pro' with proper title casing and a space.",
                "Format as 'Nivara Pro'.",
                0, 0, "{}"
            )
        ]

        for r in seed_rules:
            cursor.execute("""
                INSERT INTO rules (
                    id, guideline_version_id, rule_type, category, severity,
                    pattern, title, description, suggested_fix, blocks_approval,
                    is_mandatory, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], now
            ))

        # 4. Insert an illustrative initial audit event
        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            None,
            "SYSTEM_INITIALIZED",
            "Seeded baseline demonstration brand 'Nivara Pro' and Rule Set v1.0",
            "System Seed Service",
            json.dumps({"brand_id": NIVARA_BRAND_ID}),
            now
        ))
