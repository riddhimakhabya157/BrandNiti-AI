"""Data models for Submissions, Revisions, Review Runs, Findings, and Human Approvals."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

@dataclass
class Finding:
    id: str
    review_run_id: str
    source: str                 # 'DETERMINISTIC' or 'AI_ASSISTED'
    rule_id: Optional[str]
    rule_title: str
    category: str               # 'Voice & Tone', 'Pricing & Offers', 'Legal & Compliance', 'Claims & Evidence', 'Terminology', 'Accessibility'
    severity: str               # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    disposition_impact: str     # 'HOLD', 'REVIEW', 'PASS'
    matched_text: str
    explanation: str
    expected_condition: str
    supporting_evidence_reference: str = ""
    recommended_correction: str = ""
    verification_state: str = "VIOLATION_CONFIRMED" # 'VIOLATION_CONFIRMED', 'REQUIRES_DOCUMENTED_EVIDENCE', 'ADVISORY_SUGGESTION', 'VERIFIED_COMPLIANT'

@dataclass
class ReviewRun:
    id: str
    submission_id: str
    revision_id: str
    guideline_version_id: str
    overall_recommendation: str # 'PASS', 'REVIEW', 'HOLD'
    deterministic_passed: bool
    ai_review_performed: bool
    ai_provider_mode: str       # 'LIVE_GEMINI', 'SAMPLE_MOCK_FALLBACK', 'DETERMINISTIC_ONLY'
    summary: str
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    suggested_revised_copy: str
    findings: List[Finding] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ContentRevision:
    id: str
    submission_id: str
    version_number: int
    content_text: str
    supporting_evidence: str    # Documented promos, clinical trials, URL evidence, etc.
    change_summary: str
    is_approved: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ApprovalDecision:
    id: str
    submission_id: str
    revision_id: str
    review_run_id: str
    decision: str               # 'APPROVED', 'CHANGES_REQUESTED', 'REJECTED'
    reviewer_name: str
    reviewer_role: str
    reviewer_comments: str
    is_currently_valid: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Submission:
    id: str
    title: str
    content_type: str           # 'social_post', 'advertisement', 'email', 'blog_article', 'product_copy'
    channel: str                # 'Instagram', 'LinkedIn', 'Google Ads', 'Email', 'Website', 'Print'
    campaign_name: str
    brand_id: str
    current_version_number: int = 1
    current_status: str = "DRAFT" # 'DRAFT', 'SUBMITTED', 'IN_REVIEW', 'CHANGES_REQUESTED', 'APPROVED', 'REJECTED'
    revisions: List[ContentRevision] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class AuditEvent:
    id: str
    submission_id: Optional[str]
    event_type: str
    description: str
    actor: str
    metadata_json: str = "{}"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
