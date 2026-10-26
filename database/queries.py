"""Data access and query service for BrandNiti AI."""
import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from database.connection import get_db_connection
from models.brand import Brand, GuidelineVersion, Rule
from models.submission import (
    Submission,
    ContentRevision,
    ReviewRun,
    Finding,
    ApprovalDecision,
    AuditEvent
)

# -------------------------------------------------------------
# Brands & Guidelines
# -------------------------------------------------------------

def get_all_brands() -> List[Brand]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM brands ORDER BY is_demo DESC, name ASC")
        rows = cursor.fetchall()
        return [
            Brand(
                id=r["id"],
                name=r["name"],
                tagline=r["tagline"] or "",
                description=r["description"] or "",
                industry=r["industry"] or "",
                is_demo=bool(r["is_demo"]),
                active_guideline_version_id=r["active_guideline_version_id"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            for r in rows
        ]

def get_brand_by_id(brand_id: str) -> Optional[Brand]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM brands WHERE id = ?", (brand_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return Brand(
            id=r["id"],
            name=r["name"],
            tagline=r["tagline"] or "",
            description=r["description"] or "",
            industry=r["industry"] or "",
            is_demo=bool(r["is_demo"]),
            active_guideline_version_id=r["active_guideline_version_id"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

def get_active_guideline_version(brand_id: str) -> Optional[GuidelineVersion]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT gv.* FROM guideline_versions gv
            JOIN brands b ON b.id = gv.brand_id
            WHERE gv.brand_id = ? AND gv.is_active = 1
            ORDER BY gv.version_number DESC LIMIT 1
        """, (brand_id,))
        r = cursor.fetchone()
        if not r:
            return None
        
        # Load rules
        cursor.execute("SELECT * FROM rules WHERE guideline_version_id = ? ORDER BY severity DESC, title ASC", (r["id"],))
        rule_rows = cursor.fetchall()
        rules = [
            Rule(
                id=rr["id"],
                guideline_version_id=rr["guideline_version_id"],
                rule_type=rr["rule_type"],
                category=rr["category"],
                severity=rr["severity"],
                pattern=rr["pattern"],
                title=rr["title"],
                description=rr["description"],
                suggested_fix=rr["suggested_fix"] or "",
                blocks_approval=bool(rr["blocks_approval"]),
                is_mandatory=bool(rr["is_mandatory"]),
                metadata=json.loads(rr["metadata_json"] or "{}"),
                created_at=rr["created_at"]
            )
            for rr in rule_rows
        ]

        return GuidelineVersion(
            id=r["id"],
            brand_id=r["brand_id"],
            version_number=r["version_number"],
            version_label=r["version_label"],
            tone_of_voice=r["tone_of_voice"] or "",
            target_audience=r["target_audience"] or "",
            approved_prices=json.loads(r["approved_prices"] or "[]"),
            conditional_promotions=json.loads(r["conditional_promotions"] or "[]"),
            required_disclaimers=json.loads(r["required_disclaimers"] or "[]"),
            evidence_requirements=json.loads(r["evidence_requirements"] or "[]"),
            rules=rules,
            is_active=bool(r["is_active"]),
            changelog=r["changelog"] or "",
            created_at=r["created_at"]
        )

def get_guideline_version_by_id(guideline_id: str) -> Optional[GuidelineVersion]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM guideline_versions WHERE id = ?", (guideline_id,))
        r = cursor.fetchone()
        if not r:
            return None
        
        cursor.execute("SELECT * FROM rules WHERE guideline_version_id = ? ORDER BY severity DESC, title ASC", (guideline_id,))
        rule_rows = cursor.fetchall()
        rules = [
            Rule(
                id=rr["id"],
                guideline_version_id=rr["guideline_version_id"],
                rule_type=rr["rule_type"],
                category=rr["category"],
                severity=rr["severity"],
                pattern=rr["pattern"],
                title=rr["title"],
                description=rr["description"],
                suggested_fix=rr["suggested_fix"] or "",
                blocks_approval=bool(rr["blocks_approval"]),
                is_mandatory=bool(rr["is_mandatory"]),
                metadata=json.loads(rr["metadata_json"] or "{}"),
                created_at=rr["created_at"]
            )
            for rr in rule_rows
        ]

        return GuidelineVersion(
            id=r["id"],
            brand_id=r["brand_id"],
            version_number=r["version_number"],
            version_label=r["version_label"],
            tone_of_voice=r["tone_of_voice"] or "",
            target_audience=r["target_audience"] or "",
            approved_prices=json.loads(r["approved_prices"] or "[]"),
            conditional_promotions=json.loads(r["conditional_promotions"] or "[]"),
            required_disclaimers=json.loads(r["required_disclaimers"] or "[]"),
            evidence_requirements=json.loads(r["evidence_requirements"] or "[]"),
            rules=rules,
            is_active=bool(r["is_active"]),
            changelog=r["changelog"] or "",
            created_at=r["created_at"]
        )

def create_brand(name: str, tagline: str, description: str, industry: str) -> Brand:
    brand_id = f"brand_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()
    gv_id = f"gv_{uuid.uuid4().hex[:8]}"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO brands (id, name, tagline, description, industry, is_demo, active_guideline_version_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (brand_id, name, tagline, description, industry, 0, gv_id, now, now))

        cursor.execute("""
            INSERT INTO guideline_versions (
                id, brand_id, version_number, version_label, tone_of_voice, target_audience,
                approved_prices, conditional_promotions, required_disclaimers, evidence_requirements,
                is_active, changelog, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            gv_id, brand_id, 1, "v1.0 - Initial Baseline", "Professional, clear, trustworthy",
            "General consumers", "[]", "[]", "[]", "[]", 1, "Initial creation", now
        ))

    return get_brand_by_id(brand_id)

def create_new_guideline_version(
    brand_id: str,
    tone_of_voice: str,
    target_audience: str,
    approved_prices: List[Dict[str, Any]],
    conditional_promotions: List[Dict[str, Any]],
    required_disclaimers: List[Dict[str, Any]],
    evidence_requirements: List[Dict[str, Any]],
    changelog: str,
    rules_data: List[Dict[str, Any]]
) -> GuidelineVersion:
    now = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Find latest version number
        cursor.execute("SELECT MAX(version_number) as max_v FROM guideline_versions WHERE brand_id = ?", (brand_id,))
        row = cursor.fetchone()
        max_v = row["max_v"] if row and row["max_v"] is not None else 0
        new_v = max_v + 1

        # Deactivate old versions
        cursor.execute("UPDATE guideline_versions SET is_active = 0 WHERE brand_id = ?", (brand_id,))

        new_gv_id = f"gv_{brand_id}_{new_v}_{uuid.uuid4().hex[:6]}"
        cursor.execute("""
            INSERT INTO guideline_versions (
                id, brand_id, version_number, version_label, tone_of_voice, target_audience,
                approved_prices, conditional_promotions, required_disclaimers, evidence_requirements,
                is_active, changelog, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_gv_id,
            brand_id,
            new_v,
            f"v{new_v}.0 - Updated Guideline",
            tone_of_voice,
            target_audience,
            json.dumps(approved_prices),
            json.dumps(conditional_promotions),
            json.dumps(required_disclaimers),
            json.dumps(evidence_requirements),
            1,
            changelog,
            now
        ))

        # Insert rules
        for r in rules_data:
            rule_id = r.get("id") or f"rule_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT INTO rules (
                    id, guideline_version_id, rule_type, category, severity,
                    pattern, title, description, suggested_fix, blocks_approval,
                    is_mandatory, metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rule_id,
                new_gv_id,
                r.get("rule_type", "prohibited_phrase"),
                r.get("category", "General"),
                r.get("severity", "MEDIUM"),
                r.get("pattern", ""),
                r.get("title", ""),
                r.get("description", ""),
                r.get("suggested_fix", ""),
                1 if r.get("blocks_approval", True) else 0,
                1 if r.get("is_mandatory", True) else 0,
                json.dumps(r.get("metadata", {})),
                now
            ))

        # Update active version reference in brand
        cursor.execute("UPDATE brands SET active_guideline_version_id = ?, updated_at = ? WHERE id = ?", (new_gv_id, now, brand_id))

        # Audit event
        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            None,
            "GUIDELINE_UPDATED",
            f"Published Guideline Version v{new_v}.0 for brand {brand_id}: {changelog}",
            "Brand Manager",
            json.dumps({"brand_id": brand_id, "new_gv_id": new_gv_id, "version": new_v}),
            now
        ))

    return get_guideline_version_by_id(new_gv_id)

# -------------------------------------------------------------
# Submissions & Revisions
# -------------------------------------------------------------

def create_submission(
    title: str,
    content_type: str,
    channel: str,
    campaign_name: str,
    brand_id: str,
    initial_content: str,
    supporting_evidence: str = "",
    creator: str = "Content Creator"
) -> Submission:
    sub_id = f"sub_{uuid.uuid4().hex[:8]}"
    rev_id = f"rev_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissions (id, title, content_type, channel, campaign_name, brand_id, current_version_number, current_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, 'SUBMITTED', ?, ?)
        """, (sub_id, title, content_type, channel, campaign_name, brand_id, now, now))

        cursor.execute("""
            INSERT INTO content_revisions (id, submission_id, version_number, content_text, supporting_evidence, change_summary, is_approved, created_at)
            VALUES (?, ?, 1, ?, ?, 'Initial submission draft', 0, ?)
        """, (rev_id, sub_id, initial_content, supporting_evidence, now))

        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            sub_id,
            "SUBMISSION_CREATED",
            f"New content submission '{title}' ({content_type} on {channel}) created",
            creator,
            json.dumps({"submission_id": sub_id, "version": 1}),
            now
        ))

    return get_submission_by_id(sub_id)

def get_submission_by_id(submission_id: str) -> Optional[Submission]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,))
        r = cursor.fetchone()
        if not r:
            return None

        cursor.execute("SELECT * FROM content_revisions WHERE submission_id = ? ORDER BY version_number ASC", (submission_id,))
        rev_rows = cursor.fetchall()
        revisions = [
            ContentRevision(
                id=rr["id"],
                submission_id=rr["submission_id"],
                version_number=rr["version_number"],
                content_text=rr["content_text"],
                supporting_evidence=rr["supporting_evidence"] or "",
                change_summary=rr["change_summary"] or "",
                is_approved=bool(rr["is_approved"]),
                created_at=rr["created_at"]
            )
            for rr in rev_rows
        ]

        return Submission(
            id=r["id"],
            title=r["title"],
            content_type=r["content_type"],
            channel=r["channel"],
            campaign_name=r["campaign_name"] or "",
            brand_id=r["brand_id"],
            current_version_number=r["current_version_number"],
            current_status=r["current_status"],
            revisions=revisions,
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

def get_all_submissions(status_filter: Optional[str] = None, brand_id_filter: Optional[str] = None) -> List[Submission]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM submissions WHERE 1=1"
        params = []
        if status_filter and status_filter != "ALL":
            query += " AND current_status = ?"
            params.append(status_filter)
        if brand_id_filter and brand_id_filter != "ALL":
            query += " AND brand_id = ?"
            params.append(brand_id_filter)
        query += " ORDER BY updated_at DESC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        submissions = []
        for r in rows:
            # lightweight fetch
            sub = Submission(
                id=r["id"],
                title=r["title"],
                content_type=r["content_type"],
                channel=r["channel"],
                campaign_name=r["campaign_name"] or "",
                brand_id=r["brand_id"],
                current_version_number=r["current_version_number"],
                current_status=r["current_status"],
                revisions=[],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            )
            submissions.append(sub)
        return submissions

def create_content_revision(
    submission_id: str,
    new_content_text: str,
    supporting_evidence: str,
    change_summary: str,
    actor: str = "Content Creator"
) -> ContentRevision:
    """Creates a new version revision for an existing submission.
    CRITICAL RULE: If the previous version had an active approval, editing invalidates it!"""
    now = datetime.now(timezone.utc).isoformat()
    rev_id = f"rev_{uuid.uuid4().hex[:8]}"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT current_version_number, current_status FROM submissions WHERE id = ?", (submission_id,))
        sub_row = cursor.fetchone()
        if not sub_row:
            raise ValueError(f"Submission {submission_id} not found")

        old_version = sub_row["current_version_number"]
        new_version = old_version + 1

        # Check if previous approval existed and invalidate it for future publication
        cursor.execute("""
            UPDATE approval_decisions
            SET is_currently_valid = 0
            WHERE submission_id = ? AND is_currently_valid = 1
        """, (submission_id,))
        invalidated_count = cursor.rowcount

        # Insert new revision
        cursor.execute("""
            INSERT INTO content_revisions (id, submission_id, version_number, content_text, supporting_evidence, change_summary, is_approved, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """, (rev_id, submission_id, new_version, new_content_text, supporting_evidence, change_summary, now))

        # Update submission status to 'SUBMITTED' (needs revalidation)
        cursor.execute("""
            UPDATE submissions
            SET current_version_number = ?, current_status = 'SUBMITTED', updated_at = ?
            WHERE id = ?
        """, (new_version, now, submission_id))

        # Record audit events
        if invalidated_count > 0:
            cursor.execute("""
                INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                submission_id,
                "APPROVAL_INVALIDATED",
                f"Previous approval invalidated because content was edited in version v{new_version}. Mandatory revalidation required.",
                actor,
                json.dumps({"old_version": old_version, "new_version": new_version}),
                now
            ))

        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            submission_id,
            "REVISION_CREATED",
            f"Created version v{new_version}: {change_summary}",
            actor,
            json.dumps({"version": new_version, "change_summary": change_summary}),
            now
        ))

    return get_revision_by_id(rev_id)

def get_revision_by_id(revision_id: str) -> Optional[ContentRevision]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM content_revisions WHERE id = ?", (revision_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return ContentRevision(
            id=r["id"],
            submission_id=r["submission_id"],
            version_number=r["version_number"],
            content_text=r["content_text"],
            supporting_evidence=r["supporting_evidence"] or "",
            change_summary=r["change_summary"] or "",
            is_approved=bool(r["is_approved"]),
            created_at=r["created_at"]
        )

def get_latest_revision(submission_id: str) -> Optional[ContentRevision]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM content_revisions WHERE submission_id = ? ORDER BY version_number DESC LIMIT 1", (submission_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return ContentRevision(
            id=r["id"],
            submission_id=r["submission_id"],
            version_number=r["version_number"],
            content_text=r["content_text"],
            supporting_evidence=r["supporting_evidence"] or "",
            change_summary=r["change_summary"] or "",
            is_approved=bool(r["is_approved"]),
            created_at=r["created_at"]
        )

# -------------------------------------------------------------
# Review Runs & Findings
# -------------------------------------------------------------

def save_review_run(
    submission_id: str,
    revision_id: str,
    guideline_version_id: str,
    overall_recommendation: str,
    deterministic_passed: bool,
    ai_review_performed: bool,
    ai_provider_mode: str,
    summary: str,
    suggested_revised_copy: str,
    findings: List[Finding]
) -> ReviewRun:
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    crit_count = sum(1 for f in findings if f.severity == "CRITICAL")
    high_count = sum(1 for f in findings if f.severity == "HIGH")
    med_count = sum(1 for f in findings if f.severity == "MEDIUM")
    low_count = sum(1 for f in findings if f.severity == "LOW")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO review_runs (
                id, submission_id, revision_id, guideline_version_id, overall_recommendation,
                deterministic_passed, ai_review_performed, ai_provider_mode, summary,
                critical_count, high_count, medium_count, low_count, suggested_revised_copy, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id, submission_id, revision_id, guideline_version_id, overall_recommendation,
            1 if deterministic_passed else 0,
            1 if ai_review_performed else 0,
            ai_provider_mode,
            summary,
            crit_count, high_count, med_count, low_count, suggested_revised_copy, now
        ))

        # Insert findings
        for f in findings:
            find_id = f.id or f"find_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT INTO findings (
                    id, review_run_id, source, rule_id, rule_title, category,
                    severity, disposition_impact, matched_text, explanation,
                    expected_condition, supporting_evidence_reference,
                    recommended_correction, verification_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                find_id,
                run_id,
                f.source,
                f.rule_id,
                f.rule_title,
                f.category,
                f.severity,
                f.disposition_impact,
                f.matched_text,
                f.explanation,
                f.expected_condition,
                f.supporting_evidence_reference,
                f.recommended_correction,
                f.verification_state
            ))

        # Update submission status to 'IN_REVIEW'
        cursor.execute("UPDATE submissions SET current_status = 'IN_REVIEW', updated_at = ? WHERE id = ?", (now, submission_id))

        # Audit event
        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            submission_id,
            "REVIEW_RUN",
            f"Review run executed. Recommendation: {overall_recommendation} ({crit_count} Crit, {high_count} High, {med_count} Med)",
            f"Decision Engine ({ai_provider_mode})",
            json.dumps({"review_run_id": run_id, "recommendation": overall_recommendation}),
            now
        ))

    return get_review_run_by_id(run_id)

def get_review_run_by_id(run_id: str) -> Optional[ReviewRun]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM review_runs WHERE id = ?", (run_id,))
        r = cursor.fetchone()
        if not r:
            return None

        cursor.execute("SELECT * FROM findings WHERE review_run_id = ? ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 ELSE 4 END", (run_id,))
        f_rows = cursor.fetchall()
        findings = [
            Finding(
                id=fr["id"],
                review_run_id=fr["review_run_id"],
                source=fr["source"],
                rule_id=fr["rule_id"],
                rule_title=fr["rule_title"],
                category=fr["category"],
                severity=fr["severity"],
                disposition_impact=fr["disposition_impact"],
                matched_text=fr["matched_text"],
                explanation=fr["explanation"],
                expected_condition=fr["expected_condition"],
                supporting_evidence_reference=fr["supporting_evidence_reference"] or "",
                recommended_correction=fr["recommended_correction"] or "",
                verification_state=fr["verification_state"]
            )
            for fr in f_rows
        ]

        return ReviewRun(
            id=r["id"],
            submission_id=r["submission_id"],
            revision_id=r["revision_id"],
            guideline_version_id=r["guideline_version_id"],
            overall_recommendation=r["overall_recommendation"],
            deterministic_passed=bool(r["deterministic_passed"]),
            ai_review_performed=bool(r["ai_review_performed"]),
            ai_provider_mode=r["ai_provider_mode"],
            summary=r["summary"],
            critical_count=r["critical_count"],
            high_count=r["high_count"],
            medium_count=r["medium_count"],
            low_count=r["low_count"],
            suggested_revised_copy=r["suggested_revised_copy"] or "",
            findings=findings,
            created_at=r["created_at"]
        )

def get_latest_review_run_for_submission(submission_id: str) -> Optional[ReviewRun]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM review_runs WHERE submission_id = ? ORDER BY created_at DESC LIMIT 1", (submission_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return get_review_run_by_id(r["id"])

def get_review_runs_for_submission(submission_id: str) -> List[ReviewRun]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM review_runs WHERE submission_id = ? ORDER BY created_at DESC", (submission_id,))
        rows = cursor.fetchall()
        return [get_review_run_by_id(r["id"]) for r in rows if r]

# -------------------------------------------------------------
# Approval Decisions
# -------------------------------------------------------------

def record_approval_decision(
    submission_id: str,
    revision_id: str,
    review_run_id: str,
    decision: str, # 'APPROVED', 'CHANGES_REQUESTED', 'REJECTED'
    reviewer_name: str,
    reviewer_role: str,
    reviewer_comments: str
) -> ApprovalDecision:
    dec_id = f"dec_{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    status_map = {
        "APPROVED": "APPROVED",
        "CHANGES_REQUESTED": "CHANGES_REQUESTED",
        "REJECTED": "REJECTED"
    }
    new_status = status_map.get(decision, "IN_REVIEW")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Invalidate previous approvals for this submission if changing decision
        if decision == "APPROVED":
            cursor.execute("UPDATE approval_decisions SET is_currently_valid = 0 WHERE submission_id = ?", (submission_id,))
            cursor.execute("UPDATE content_revisions SET is_approved = 1 WHERE id = ?", (revision_id,))
        else:
            cursor.execute("UPDATE content_revisions SET is_approved = 0 WHERE id = ?", (revision_id,))

        cursor.execute("""
            INSERT INTO approval_decisions (
                id, submission_id, revision_id, review_run_id, decision,
                reviewer_name, reviewer_role, reviewer_comments, is_currently_valid, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (
            dec_id, submission_id, revision_id, review_run_id, decision,
            reviewer_name, reviewer_role, reviewer_comments, now
        ))

        # Update submission status
        cursor.execute("UPDATE submissions SET current_status = ?, updated_at = ? WHERE id = ?", (new_status, now, submission_id))

        # Audit event
        cursor.execute("""
            INSERT INTO audit_events (id, submission_id, event_type, description, actor, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            submission_id,
            "DECISION_MADE",
            f"Human decision recorded: {decision} by {reviewer_name} ({reviewer_role}). Comments: {reviewer_comments[:80]}",
            reviewer_name,
            json.dumps({"decision": decision, "revision_id": revision_id, "decision_id": dec_id}),
            now
        ))

    return ApprovalDecision(
        id=dec_id,
        submission_id=submission_id,
        revision_id=revision_id,
        review_run_id=review_run_id,
        decision=decision,
        reviewer_name=reviewer_name,
        reviewer_role=reviewer_role,
        reviewer_comments=reviewer_comments,
        is_currently_valid=True,
        created_at=now
    )

def get_decisions_for_submission(submission_id: str) -> List[ApprovalDecision]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM approval_decisions WHERE submission_id = ? ORDER BY created_at DESC", (submission_id,))
        rows = cursor.fetchall()
        return [
            ApprovalDecision(
                id=r["id"],
                submission_id=r["submission_id"],
                revision_id=r["revision_id"],
                review_run_id=r["review_run_id"],
                decision=r["decision"],
                reviewer_name=r["reviewer_name"],
                reviewer_role=r["reviewer_role"],
                reviewer_comments=r["reviewer_comments"] or "",
                is_currently_valid=bool(r["is_currently_valid"]),
                created_at=r["created_at"]
            )
            for r in rows
        ]

# -------------------------------------------------------------
# Audit Logs
# -------------------------------------------------------------

def get_audit_trail(submission_id: Optional[str] = None, limit: int = 50) -> List[AuditEvent]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if submission_id:
            cursor.execute("SELECT * FROM audit_events WHERE submission_id = ? ORDER BY created_at DESC LIMIT ?", (submission_id, limit))
        else:
            cursor.execute("SELECT * FROM audit_events ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [
            AuditEvent(
                id=r["id"],
                submission_id=r["submission_id"],
                event_type=r["event_type"],
                description=r["description"],
                actor=r["actor"],
                metadata_json=r["metadata_json"] or "{}",
                created_at=r["created_at"]
            )
            for r in rows
        ]

# -------------------------------------------------------------
# Governance Insights & Metrics Queries
# -------------------------------------------------------------

def get_governance_insights() -> Dict[str, Any]:
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Submission counts (distinct submissions)
        cursor.execute("SELECT COUNT(DISTINCT id) as total FROM submissions")
        total_submissions = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(DISTINCT id) as pending FROM submissions WHERE current_status IN ('SUBMITTED', 'IN_REVIEW')")
        pending_reviews = cursor.fetchone()["pending"]

        cursor.execute("SELECT COUNT(DISTINCT id) as approved FROM submissions WHERE current_status = 'APPROVED'")
        approved_count = cursor.fetchone()["approved"]

        cursor.execute("SELECT current_status, COUNT(DISTINCT id) as cnt FROM submissions GROUP BY current_status")
        status_counts = {r["current_status"]: r["cnt"] for r in cursor.fetchall()}

        # 2. System Recommendations from LATEST review run per submission (distinct per asset)
        cursor.execute("""
            SELECT rr.overall_recommendation, COUNT(DISTINCT rr.submission_id) as cnt
            FROM review_runs rr
            INNER JOIN (
                SELECT submission_id, MAX(created_at) as max_created
                FROM review_runs
                GROUP BY submission_id
            ) latest ON rr.submission_id = latest.submission_id AND rr.created_at = latest.max_created
            GROUP BY rr.overall_recommendation
        """)
        rec_counts = {r["overall_recommendation"]: r["cnt"] for r in cursor.fetchall()}

        # Calculate items requiring attention (HOLD + REVIEW)
        hold_count = rec_counts.get("HOLD", 0)
        review_count = rec_counts.get("REVIEW", 0)
        pass_count = rec_counts.get("PASS", 0)
        issues_requiring_attention = hold_count + review_count

        # 3. Valid Human Approval Status
        cursor.execute("""
            SELECT decision, COUNT(DISTINCT submission_id) as cnt
            FROM approval_decisions
            WHERE is_currently_valid = 1
            GROUP BY decision
        """)
        human_decisions = {r["decision"]: r["cnt"] for r in cursor.fetchall()}

        # 4. Most frequently triggered rules
        cursor.execute("""
            SELECT rule_title, category, severity, COUNT(*) as trigger_count
            FROM findings
            WHERE rule_title IS NOT NULL AND rule_title != ''
            GROUP BY rule_title, category, severity
            ORDER BY trigger_count DESC
            LIMIT 5
        """)
        top_rules = [
            {
                "rule_title": r["rule_title"],
                "category": r["category"],
                "severity": r["severity"],
                "trigger_count": r["trigger_count"]
            }
            for r in cursor.fetchall()
        ]

        # 5. Repeated unsupported claim patterns
        cursor.execute("""
            SELECT matched_text, category, COUNT(*) as pattern_count
            FROM findings
            WHERE disposition_impact IN ('HOLD', 'REVIEW')
            GROUP BY matched_text
            ORDER BY pattern_count DESC
            LIMIT 5
        """)
        unsupported_patterns = [
            {"matched_text": r["matched_text"], "category": r["category"], "count": r["pattern_count"]}
            for r in cursor.fetchall()
        ]

        # 6. Common tone/terminology issues
        cursor.execute("""
            SELECT category, COUNT(*) as cnt
            FROM findings
            GROUP BY category
            ORDER BY cnt DESC
        """)
        category_breakdown = {r["category"]: r["cnt"] for r in cursor.fetchall()}

        # 7. Recent distinct reviews
        cursor.execute("""
            SELECT rr.id, rr.overall_recommendation, rr.created_at, s.title, s.content_type, s.channel
            FROM review_runs rr
            JOIN submissions s ON s.id = rr.submission_id
            ORDER BY rr.created_at DESC
            LIMIT 6
        """)
        recent_activity = [
            {
                "run_id": r["id"],
                "recommendation": r["overall_recommendation"],
                "created_at": r["created_at"],
                "title": r["title"],
                "content_type": r["content_type"],
                "channel": r["channel"]
            }
            for r in cursor.fetchall()
        ]

        return {
            "total_submissions": total_submissions,
            "pending_reviews": pending_reviews,
            "approved_count": approved_count,
            "issues_requiring_attention": issues_requiring_attention,
            "hold_count": hold_count,
            "review_count": review_count,
            "pass_count": pass_count,
            "status_counts": status_counts,
            "recommendations": rec_counts,
            "human_decisions": human_decisions,
            "top_rules": top_rules,
            "unsupported_patterns": unsupported_patterns,
            "category_breakdown": category_breakdown,
            "recent_activity": recent_activity
        }
