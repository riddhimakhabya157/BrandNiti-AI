"""SQLite schema definition for BrandNiti AI."""
import sqlite3
from database.connection import get_db_connection

SCHEMA_SQL = """
-- Brands table
CREATE TABLE IF NOT EXISTS brands (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tagline TEXT,
    description TEXT,
    industry TEXT,
    is_demo INTEGER DEFAULT 0,
    active_guideline_version_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Guideline versions table
CREATE TABLE IF NOT EXISTS guideline_versions (
    id TEXT PRIMARY KEY,
    brand_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    version_label TEXT NOT NULL,
    tone_of_voice TEXT,
    target_audience TEXT,
    approved_prices TEXT,          -- JSON string array/dict
    conditional_promotions TEXT,   -- JSON string array/dict
    required_disclaimers TEXT,     -- JSON string array/dict
    evidence_requirements TEXT,    -- JSON string array/dict
    is_active INTEGER DEFAULT 1,
    changelog TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands (id) ON DELETE CASCADE
);

-- Individual brand rules table
CREATE TABLE IF NOT EXISTS rules (
    id TEXT PRIMARY KEY,
    guideline_version_id TEXT NOT NULL,
    rule_type TEXT NOT NULL,       -- prohibited_phrase, approved_terminology, price_check, disclaimer_check, evidence_requirement, messaging_restriction
    category TEXT NOT NULL,        -- Voice & Tone, Pricing & Offers, Legal & Compliance, Claims & Evidence, Terminology
    severity TEXT NOT NULL,        -- CRITICAL, HIGH, MEDIUM, LOW
    pattern TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    suggested_fix TEXT,
    blocks_approval INTEGER DEFAULT 1,
    is_mandatory INTEGER DEFAULT 1,
    metadata_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (guideline_version_id) REFERENCES guideline_versions (id) ON DELETE CASCADE
);

-- Content submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content_type TEXT NOT NULL,    -- social_post, advertisement, email, blog_article, product_copy
    channel TEXT NOT NULL,         -- Instagram, LinkedIn, Google Ads, Email, Website, Print
    campaign_name TEXT,
    brand_id TEXT NOT NULL,
    current_version_number INTEGER DEFAULT 1,
    current_status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, SUBMITTED, IN_REVIEW, CHANGES_REQUESTED, APPROVED, REJECTED
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands (id) ON DELETE CASCADE
);

-- Content revisions table (immutable historical drafts)
CREATE TABLE IF NOT EXISTS content_revisions (
    id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    content_text TEXT NOT NULL,
    supporting_evidence TEXT DEFAULT '',
    change_summary TEXT DEFAULT '',
    is_approved INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions (id) ON DELETE CASCADE,
    UNIQUE(submission_id, version_number)
);

-- Review runs table (deterministic + AI audit log)
CREATE TABLE IF NOT EXISTS review_runs (
    id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    revision_id TEXT NOT NULL,
    guideline_version_id TEXT NOT NULL,
    overall_recommendation TEXT NOT NULL, -- PASS, REVIEW, HOLD
    deterministic_passed INTEGER NOT NULL,
    ai_review_performed INTEGER NOT NULL,
    ai_provider_mode TEXT NOT NULL,       -- LIVE_GEMINI, SAMPLE_MOCK_FALLBACK, DETERMINISTIC_ONLY
    summary TEXT NOT NULL,
    critical_count INTEGER DEFAULT 0,
    high_count INTEGER DEFAULT 0,
    medium_count INTEGER DEFAULT 0,
    low_count INTEGER DEFAULT 0,
    suggested_revised_copy TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions (id) ON DELETE CASCADE,
    FOREIGN KEY (revision_id) REFERENCES content_revisions (id) ON DELETE CASCADE,
    FOREIGN KEY (guideline_version_id) REFERENCES guideline_versions (id)
);

-- Findings table (individual issues flagged in a review run)
CREATE TABLE IF NOT EXISTS findings (
    id TEXT PRIMARY KEY,
    review_run_id TEXT NOT NULL,
    source TEXT NOT NULL,                 -- DETERMINISTIC, AI_ASSISTED
    rule_id TEXT,
    rule_title TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,               -- CRITICAL, HIGH, MEDIUM, LOW
    disposition_impact TEXT NOT NULL,     -- HOLD, REVIEW, PASS
    matched_text TEXT NOT NULL,
    explanation TEXT NOT NULL,
    expected_condition TEXT NOT NULL,
    supporting_evidence_reference TEXT DEFAULT '',
    recommended_correction TEXT DEFAULT '',
    verification_state TEXT NOT NULL DEFAULT 'VIOLATION_CONFIRMED',
    FOREIGN KEY (review_run_id) REFERENCES review_runs (id) ON DELETE CASCADE
);

-- Approval decisions table
CREATE TABLE IF NOT EXISTS approval_decisions (
    id TEXT PRIMARY KEY,
    submission_id TEXT NOT NULL,
    revision_id TEXT NOT NULL,
    review_run_id TEXT NOT NULL,
    decision TEXT NOT NULL,               -- APPROVED, CHANGES_REQUESTED, REJECTED
    reviewer_name TEXT NOT NULL,
    reviewer_role TEXT NOT NULL,
    reviewer_comments TEXT,
    is_currently_valid INTEGER DEFAULT 1, -- Becomes 0 if content is subsequently edited!
    created_at TEXT NOT NULL,
    FOREIGN KEY (submission_id) REFERENCES submissions (id) ON DELETE CASCADE,
    FOREIGN KEY (revision_id) REFERENCES content_revisions (id) ON DELETE CASCADE,
    FOREIGN KEY (review_run_id) REFERENCES review_runs (id) ON DELETE CASCADE
);

-- Audit log events table
CREATE TABLE IF NOT EXISTS audit_events (
    id TEXT PRIMARY KEY,
    submission_id TEXT,
    event_type TEXT NOT NULL,             -- SUBMISSION_CREATED, REVIEW_RUN, REVISION_CREATED, DECISION_MADE, APPROVAL_INVALIDATED, GUIDELINE_UPDATED
    description TEXT NOT NULL,
    actor TEXT NOT NULL,
    metadata_json TEXT DEFAULT '{}',
    created_at TEXT NOT NULL
);

-- Performance indices
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(current_status);
CREATE INDEX IF NOT EXISTS idx_revisions_submission ON content_revisions(submission_id);
CREATE INDEX IF NOT EXISTS idx_review_runs_submission ON review_runs(submission_id);
CREATE INDEX IF NOT EXISTS idx_findings_run ON findings(review_run_id);
CREATE INDEX IF NOT EXISTS idx_audit_events_submission ON audit_events(submission_id);
"""

def init_database():
    """Initializes tables and indexes in SQLite."""
    with get_db_connection() as conn:
        conn.executescript(SCHEMA_SQL)
