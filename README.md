# BrandNiti AI — Every Brand Message. On Brand.

**Enterprise AI-Powered Brand Governance Platform**  
*Create Confidently. Review Intelligently. Publish Responsibly.*

---

## 🛡️ Visual Identity: Premium Enterprise Compliance

BrandNiti AI uses a modern, high-contrast **White + Deep Green + Red** visual identity designed for enterprise brand governance:
- **Refined Color Palette:** Pure White (`#FFFFFF`) card surfaces on a clean canvas (`#F8FAFC`), Deep Green headings (`#14532D`), Primary Forest Green (`#166534`) for brand actions and positive states, and crisp borders (`#E2E8F0`).
- **Brand Emblem:** Minimalist shield emblem symbolizing brand defense, policy adherence, and verified compliance.
- **Accessible Disposition System:** Icon-paired status tokens strictly following color rules: **PASS** (Compliant Green `#166534`, surface `#DCFCE7`), **REVIEW** (Amber `#A16207`, surface `#FEF3C7`), and **HOLD** (Ruby Red `#DC2626`, surface `#FEE2E2`).
- **Enterprise Typography & Layout:** High-density, professional typography (`Plus Jakarta Sans`), responsive tables, side-by-side diff comparisons, and genuine database-derived KPI metrics.

---

## 🚀 Key Problems Solved

1. **Inconsistent Brand Voice & Terminology:** Automatically audits content across marketing channels (Instagram, LinkedIn, Google Ads, Email, Website, Print) against approved brand personas and terminology guidelines.
2. **Conditional Pricing Violations:** Enforces strict conditional checks (e.g. ₹799 promotional price requires active, documented marketing authorization; the system never assumes a promotion is active without verified proof).
3. **Unsubstantiated Outcomes & Timeframe Claims:** Detects and blocks absolute guarantees (e.g. "Guaranteed results in 24 hours") under mandatory deterministic policies.
4. **Mandatory Disclaimers & Empirical Evidence:** Identifies missing results disclaimers and flags unverified efficacy assertions that lack lab trials or clinical citations.
5. **Approval Tampering & Content Drift:** If an approved piece of content is subsequently edited, **BrandNiti AI automatically invalidates the prior approval** for the new revision and enforces revalidation.
6. **Durable, Traceable Audit Trail:** Tamper-resistant SQLite event stream recording every draft version, automated audit run, human decision, and invalidation timestamp.

---

## 📦 Technology Stack

- **Language:** Python 3.10+ (tested on Python 3.14.2)
- **Frontend Framework:** Streamlit with custom enterprise CSS design system
- **Deterministic Rule Engine:** Custom Python token and regex policy verification
- **AI-Assisted Contextual Review:** Google Gemini 2.5 Flash integration with prompt injection defense, zero-hallucination guardrails, and a transparent deterministic fallback when API credentials are unset
- **Persistence Layer:** SQLite with Write-Ahead Logging (`PRAGMA journal_mode = WAL;`) and enforced foreign keys (`PRAGMA foreign_keys = ON;`)
- **Testing:** Pytest automated test suite covering deterministic rules, decision engine precedence, approval invalidation, and metrics calculation

---

## 📐 Architecture & Core Modules

```
BrandNiti_AI/
├── app.py                      # Main Streamlit application and view router
├── models/
│   ├── brand.py                # Brand, GuidelineVersion, and Rule data models
│   └── submission.py           # Submission, ContentRevision, ReviewRun, Finding, Decision models
├── services/
│   ├── rule_engine.py          # Deterministic brand-rule validation (Zero Hallucination)
│   ├── ai_review.py            # Gemini API contextual review + transparent fallback
│   ├── decision_engine.py      # HOLD > REVIEW > PASS disposition hierarchy & explanation aggregator
│   └── review_workflow.py      # State machine orchestrator & human approval invalidation logic
├── database/
│   ├── connection.py           # Thread-safe SQLite connection manager with WAL mode
│   ├── schema.py               # Complete SQL schema & indices definition
│   ├── seed_data.py            # Seed fixtures for sample brand 'Nivara Pro'
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

The application strictly implements an enterprise governance disposition model:

- 🛑 **HOLD — Policy Blocked**  
  *Triggers:* Any mandatory prohibited phrase (e.g. "guaranteed results", "100% cure") or blocking policy violation.  
  *Precedence:* **HOLD takes precedence over all other outcomes.** If both HOLD and REVIEW conditions exist, the recommendation is HOLD.
- ⚠️ **REVIEW — Verification Required**  
  *Triggers:* Unverified promotional pricing (e.g. ₹799 without campaign documentation), unverified speed claims ("in 24 hours" without lab citations), missing disclaimers, or tone inconsistencies.
- ✅ **PASS — Compliant**  
  *Triggers:* All mandatory deterministic rules pass, all required evidence is documented, and no high-risk contextual issues remain.  
  *Crucial Rule:* **PASS is an advisory system recommendation, not an approval.** Even a PASS requires authorized human sign-off before publication.

---

## 🧪 Automated Testing & Verification

The test suite validates core requirements:
- **Presentation Content Benchmark:** Verifies that `"Get Nivara Pro today for ₹799. Guaranteed results in 24 hours!"` flags ₹799 promotional price condition, flags "Guaranteed results" as CRITICAL HOLD, flags "in 24 hours" as requiring empirical evidence, and flags missing disclaimer.
- **Evidence Verification:** Confirms ₹799 with valid promotional documentation passes conditionally.
- **Decision Precedence:** Confirms HOLD overrides REVIEW and PASS.
- **Approval Invalidation:** Creates an approved draft, edits it, and verifies that the previous approval is automatically marked `is_currently_valid = False` with submission status reverted to `SUBMITTED`.
- **Database Durability:** Verifies SQLite transactions survive connection restarts.
- **Guideline Versioning:** Verifies version bumping to v2.0 upon publishing rule edits.
- **Governance Insights:** Computes real SQL aggregates without hardcoded numbers.

Run tests:
```bash
python -m pytest tests/test_brandniti.py -v
```

---

## 🏃 Quickstart: Running BrandNiti AI Locally

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14.2)
- Git

### 2. Setup
```bash
git clone https://github.com/twin-soch/brandniti-ai.git
cd brandniti-ai

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Credentials (Optional)
```bash
cp .env.example .env
# Edit .env and paste your Gemini API key:
# GEMINI_API_KEY=your_key_here
```
*(If no key is configured, BrandNiti AI operates in deterministic review mode with illustrative fallback).*

### 4. Launch the Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 👥 Product Credits

**BrandNiti AI Enterprise Edition**  
*Powered by Team TWIN SOCH — Two Minds. One Vision.*
