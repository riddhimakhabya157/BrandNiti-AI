# BrandNiti AI — Every Brand Message. On Brand.

**Hackathon Round 2 Prototype**  
**Team:** TWIN SOCH — Two Minds. One Vision.  
**Core Promise:** AI-Powered Brand Governance: Create Faster, Verify Smarter, Publish Confidently.

---

## 🏛️ Visual Identity & Design Philosophy: Indian Heritage × Modern AI

BrandNiti AI blends an Indian-rooted design philosophy with a modern AI SaaS product aesthetic:
- **Palette:** Deep Indigo (`#1E1B4B`) contrast, Peacock Teal (`#0F766E`) precision indicators, Warm Ivory (`#FAF8F5`) canvas, and restrained Antique Gold / Saffron (`#D97706`) accents.
- **Architectural Motif:** Subtle Indian geometric jaali / rangoli-inspired dividers and structure.
- **Explainable Status System:** Accessible, color-coded, distinct badges for **PASS** (Emerald Green), **REVIEW** (Amber/Gold), and **HOLD** (Ruby Red).
- **Enterprise-Ready UI:** High-density, professional typography (Plus Jakarta Sans & Cinzel wordmark), zero decorative clutter, responsive data tables, side-by-side diff comparisons, and clear executive KPI cards.

---

## 🚀 Key Problems Solved (Round 1 Vision Realized)

1. **Inconsistent Brand Voice & Terminology:** Automates tone of voice checks and brand naming rules across channels.
2. **Risky Promotional Pricing Claims:** Enforces strict conditional checks (e.g. ₹799 promotional price requires active authorized campaign documentation; system never assumes promotion is active).
3. **Unsubstantiated Efficacy Guarantees:** Detects and blocks absolute guarantees (e.g. "Guaranteed results in 24 hours") under mandatory deterministic policies.
4. **Missing Disclaimers & Required Evidence:** Automatically flags missing results disclaimers and mandates clinical/empirical citations for turnaround speed assertions.
5. **Approval Tampering & Drift:** If an approved piece of content is subsequently edited, **BrandNiti AI automatically invalidates the prior approval** for the new revision and enforces revalidation.
6. **Fragmented Audit Trail:** Durable SQLite event stream recording every draft version, automated audit run, human decision, and invalidation timestamp.

---

## 📦 Technology Stack

- **Language:** Python 3.14 / 3.10+
- **Frontend Framework:** Streamlit (single-application architecture with injected Indian Heritage CSS design system)
- **Deterministic Rule Engine:** Custom Python regex and token-level policy verification
- **AI-Assisted Contextual Review:** Google Gemini 2.5 Flash integration with prompt injection defense, zero-hallucination guardrails, and a transparent sample mode fallback when API credentials are unset
- **Persistence Layer:** SQLite with Write-Ahead Logging (`PRAGMA journal_mode = WAL;`) and enforced foreign keys (`PRAGMA foreign_keys = ON;`)
- **Testing:** Pytest automated test suite covering deterministic rules, decision engine precedence, approval invalidation, and metrics calculation

---

## 📐 Product Architecture & Core Modules

```
BrandNiti_AI/
├── app.py                      # Main Streamlit application and view router
├── models/
│   ├── brand.py                # Brand, GuidelineVersion, and Rule data models
│   └── submission.py           # Submission, ContentRevision, ReviewRun, Finding, Decision models
├── services/
│   ├── rule_engine.py          # Deterministic brand-rule validation (Zero Hallucination)
│   ├── ai_review.py            # Gemini API contextual review + transparent sample mode fallback
│   ├── decision_engine.py      # HOLD > REVIEW > PASS disposition hierarchy & explanation aggregator
│   └── review_workflow.py      # State machine orchestrator & human approval invalidation logic
├── database/
│   ├── connection.py           # Thread-safe SQLite connection manager with WAL mode
│   ├── schema.py               # Complete SQL schema & indices definition
│   ├── seed_data.py            # Seed fixtures for fictional demo brand 'Nivara Pro'
│   └── queries.py              # Parameterized SQL queries for brands, submissions, and metrics
├── styles/
│   └── theme.py                # Indian Heritage × Modern AI CSS theme, headers, and badges
├── tests/
│   └── test_brandniti.py       # Comprehensive pytest suite (9 automated tests)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # Complete system documentation
```

---

## ⚖️ Deterministic Rules vs AI Contextual Review

| Dimension | Deterministic Rule Engine | AI-Assisted Review (Gemini) |
| :--- | :--- | :--- |
| **Authority** | **Mandatory & Non-negotiable** | **Advisory & Explanatory** |
| **Can Overrule?** | Cannot be bypassed by AI | Cannot bypass deterministic policies |
| **Scope** | Prohibited phrases, exact pricing, conditional promo rules, required disclaimers, explicit evidence triggers | Tone mismatch, nuanced context, misleading implications, copywriting suggestions |
| **Evidence Integrity** | Strict factual matching against submitted metadata | **Zero Hallucination Guarantee:** Never invents URLs, citations, or verification results |
| **Availability** | Always 100% available offline | Live when `GEMINI_API_KEY` is present; transparently falls back to labeled sample review |

---

## 🚦 Decision Engine Precedence Model

The application strictly implements the Round 1 disposition model:

- 🛑 **HOLD — Blocked Pending Fix**  
  *Triggers:* Any mandatory prohibited phrase (e.g. "guaranteed results", "100% cure") or blocking policy violation.  
  *Precedence:* **HOLD takes precedence over all other outcomes.** If both HOLD and REVIEW conditions exist, the recommendation is HOLD.
- ⚠️ **REVIEW — Needs Verification**  
  *Triggers:* Unverified promotional pricing (e.g. ₹799 without campaign documentation), unverified speed claims ("in 24 hours" without lab citations), missing disclaimers, or tone inconsistencies.
- ✅ **PASS — Clear to Proceed**  
  *Triggers:* All mandatory deterministic rules pass, all required evidence is documented, and no high-risk contextual issues remain.  
  *Crucial Rule:* **PASS is an advisory system recommendation, not an approval.** Even a PASS requires human review and sign-off before publication.

---

## 🧪 Automated Testing & Verification

The test suite thoroughly validates core requirements:
- **Presentation Content Benchmark:** Verifies that `"Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"` flags ₹799 promotional price condition, flags "Guaranteed results" as CRITICAL HOLD, flags "in 24 hours" as requiring empirical evidence, and flags missing disclaimer.
- **Evidence Verification:** Confirms ₹799 with valid promotional documentation passes conditionally.
- **Decision Precedence:** Confirms HOLD overrides REVIEW and PASS.
- **Approval Invalidation:** Creates an approved draft, edits it, and verifies that the previous approval is automatically marked `is_currently_valid = False` with submission status reverted to `SUBMITTED`.
- **Database Durability:** Verifies SQLite transactions survive connection restarts.
- **Guideline Versioning:** Verifies version bumping to v2.0 upon publishing rule edits.
- **Governance Insights:** Computes real SQL aggregates without hardcoded numbers.

Run the tests locally:
```bash
python -m pytest tests/test_brandniti.py -v
```
*Current test status: 9 passed in 3.89s (100% pass rate).*

---

## 🏃 Quickstart: Running BrandNiti AI Locally

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14.2)
- Git

### 2. Clone and Setup
```bash
git clone https://github.com/twin-soch/brandniti-ai.git
cd brandniti-ai

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Credentials (Optional)
```bash
cp .env.example .env
# Edit .env and paste your Gemini API key:
# GEMINI_API_KEY=your_key_here
```
*(If no key is configured, BrandNiti AI automatically and transparently operates in deterministic review mode with illustrative sample fallback).*

### 4. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔍 Judge's Evaluation Journey (Step-by-Step)

1. **Open the Overview Screen:** Inspect the real-time governance metrics and click **"Audit Round 1 Risky Ad Sample"**.
2. **Review the Risky Ad:** Notice the pre-loaded copy `"Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"`.
3. **Execute the Audit:** Click **"Run Full Governance Audit"**.
4. **Inspect Explainable Findings:**
   - Observe the **HOLD** recommendation badge.
   - See the 4 itemized findings: Prohibited phrasing ("Guaranteed results"), Conditional promo price (₹799 without evidence), Unverified timeframe claim ("in 24 hours"), and Missing disclaimer.
5. **Inspect Suggested Copy:** View the side-by-side comparison box showing how BrandNiti AI safely rewrites the copy to standard price ₹999 with sustainable wellness phrasing and variation disclaimer.
6. **Accept & Resubmit Revision:** Expand "Edit and Submit Revised Version", review the compliant copy, and submit as version **v2**. Notice the new audit run upgrades to **PASS**!
7. **Navigate to Review Queue:** Open **"3. Review Queue"**, locate the submission, and record a human **APPROVED** decision by demo reviewer *Priya Sharma*.
8. **Test Approval Invalidation:** In the Review Queue, edit the approved submission to reintroduce a risky phrase. Check the audit history: notice that the previous approval is immediately revoked (`is_currently_valid = 0`), the status returns to `SUBMITTED`, and revalidation is enforced!
9. **Inspect Insights & History:** Visit **"5. Insights"** and **"6. Review History"** to inspect SQL-computed rule trigger frequencies and immutable audit logs.

---

## 🔮 Three Major Round 3 Improvements (Planned Roadmap)

The following three architectural upgrades are reserved for Round 3:

### Improvement 1 — Brand Guideline and Document Ingestion
- **Problem:** Brand guidelines are often published as 50+ page corporate brand books (PDFs, PPTXs, Notion documents), making manual rule transcription tedious and prone to human omission.
- **Technical Approach:** Implement an asynchronous document parsing pipeline utilizing multimodal Gemini Document Understanding and PyMuPDF. Extracts color schemes, tone personas, disallowed terminology tables, pricing policies, and evidence thresholds into structured JSON drafts. Includes an interactive human-in-the-loop review stage for brand managers to review and confirm extracted rules before publishing a new guideline version.
- **Expected User Benefit:** Onboarding a new enterprise brand profile reduced from 4 hours of manual transcription to under 3 minutes with verified human confirmation.
- **Measurable Success Criterion:** $\ge 92\%$ accuracy on structured rule extraction across 15 standard corporate brand guideline PDFs.
- **Dependencies & Limitations:** Requires multimodal document parsing libraries and OCR support for scanned image-heavy PDFs.

### Improvement 2 — Multilingual Brand Governance (Indic Languages)
- **Problem:** Global and Indian brands run hyper-local campaigns in Hindi, Tamil, Telugu, Bengali, Marathi, and regional dialects where translated idioms frequently distort approved brand tone or violate local statutory advertising regulations (ASCI guidelines).
- **Technical Approach:** Implement language identification and specialized cross-lingual embedding evaluation against multilingual terminology dictionaries. Integrates regional Indian advertising statutory disclaimer libraries (e.g., Food Safety & Standards Act, Drugs and Magic Remedies Act disclaimers in regional scripts).
- **Expected User Benefit:** Single unified governance workflow for multi-region, pan-Indian campaigns with zero cross-lingual tone degradation.
- **Measurable Success Criterion:** 100% detection rate for statutory disclaimer omissions and prohibited health claims across 8 scheduled Indian languages.
- **Dependencies & Limitations:** High-quality Indic translation models and labeled regional benchmark datasets.

### Improvement 3 — Enterprise Approval & Marketing Integrations
- **Problem:** Copy approval bottlenecks occur because content creators work in tools like Figma, HubSpot, WordPress, and Hootsuite, while compliance reviews happen manually in email or Slack threads.
- **Technical Approach:** Build bi-directional webhook and REST API connectors for HubSpot, Figma, Contentful, and Slack. Introduces multi-tier role-based approval routing (e.g., Copywriter $\rightarrow$ Agency Lead $\rightarrow$ Legal Counsel $\rightarrow$ Brand Director) with cryptographic signatures for finalized publication payloads.
- **Expected User Benefit:** Content creators receive real-time inline BrandNiti governance scores directly within their authoring environment without context-switching.
- **Measurable Success Criterion:** Sub-second API response time ($\le 850\text{ms}$) for deterministic webhook audits and automated generation of tamper-evident approval certificates.
- **Dependencies & Limitations:** Third-party OAuth2 app verifications and enterprise enterprise SSO integrations (SAML/Okta).

---

## 👥 Team Identity

**TWIN SOCH**  
*Two Minds. One Vision.*  
Hackathon Round 2 Prototype — 28 October 2026.
