"""Data models for Brand and Guideline management."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

@dataclass
class Rule:
    id: str
    guideline_version_id: str
    rule_type: str  # 'prohibited_phrase', 'approved_terminology', 'price_check', 'disclaimer_check', 'evidence_requirement', 'messaging_restriction'
    category: str   # 'Voice & Tone', 'Pricing & Offers', 'Legal & Compliance', 'Claims & Evidence', 'Terminology'
    severity: str   # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    pattern: str    # Search term, regex, or value
    title: str
    description: str
    suggested_fix: str
    blocks_approval: bool = True
    is_mandatory: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class GuidelineVersion:
    id: str
    brand_id: str
    version_number: int
    version_label: str
    tone_of_voice: str
    target_audience: str
    approved_prices: List[Dict[str, Any]] = field(default_factory=list)
    conditional_promotions: List[Dict[str, Any]] = field(default_factory=list)
    required_disclaimers: List[Dict[str, Any]] = field(default_factory=list)
    evidence_requirements: List[Dict[str, Any]] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    is_active: bool = True
    changelog: str = "Initial baseline guideline"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class Brand:
    id: str
    name: str
    tagline: str
    description: str
    industry: str
    is_demo: bool = False
    active_guideline_version_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
