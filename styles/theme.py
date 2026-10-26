"""Indian Heritage × Modern AI Visual Identity & Styling System for BrandNiti AI.
Enterprise SaaS styling:
- Deep Indigo (#1E1B4B, #17143A) for primary navigation and visual anchors
- Peacock Teal (#0F766E, #0D9488) for primary CTAs and active states
- Warm Ivory / Soft Off-White (#FAF8F5) for comfortable canvas background
- Antique Gold / Muted Saffron (#D97706, #B45309) for restrained highlights
- High contrast, dark readable typography across all elements (no white-on-light bugs)
- Compact, professional enterprise header with horizontal navigation
- Visible 4-step workflow stepper (Content -> Analysis -> Corrections -> Human Decision)
"""
import textwrap

CUSTOM_CSS = textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap');

/* Canvas & Global Reset */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #FAF8F5 !important;
    color: #1E293B !important;
    font-size: 15px;
    line-height: 1.6;
}

/* Explicit high-contrast typography: Dark text on Ivory background */
h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
    color: #1E1B4B !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
}

h1 { font-size: 1.85rem !important; }
h2 { font-size: 1.45rem !important; margin-top: 1rem !important; }
h3 { font-size: 1.2rem !important; }
h4 { font-size: 1.05rem !important; }

p, span, div, li, [data-testid="stMarkdownContainer"] p {
    color: #1E293B !important;
}

/* Widget Labels: Dark Indigo, bold, perfectly visible */
[data-testid="stWidgetLabel"] p, label, [data-testid="stWidgetLabel"] label {
    color: #1E1B4B !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    margin-bottom: 3px !important;
}

/* Form Inputs & Textareas */
input, textarea, select, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 6px !important;
    font-size: 0.95rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #0F766E !important;
    box-shadow: 0 0 0 2px rgba(15, 118, 110, 0.2) !important;
}

/* Metric Display Values */
[data-testid="stMetricValue"] {
    color: #1E1B4B !important;
    font-weight: 800 !important;
    font-size: 1.85rem !important;
}

[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Container & Bordered Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border-color: #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.03) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    margin-bottom: 0.85rem !important;
}

[data-testid="stExpander"] details summary span p {
    color: #1E1B4B !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Streamlit main block container spacing */
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px;
}

/* -------------------------------------------------------------
   Compact Enterprise Top Brand Bar
   ------------------------------------------------------------- */
.bn-top-bar {
    background: linear-gradient(90deg, #1E1B4B 0%, #1E2248 55%, #0F766E 100%);
    padding: 0.8rem 1.4rem;
    border-radius: 8px;
    color: #FFFFFF;
    margin-bottom: 0.85rem;
    border-bottom: 2.5px solid #D97706;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(30, 27, 75, 0.08);
}

.bn-brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.bn-brand-title {
    font-family: 'Cinzel', serif;
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #FFFFFF !important;
    line-height: 1.2;
}

.bn-brand-title span.saffron {
    color: #F59E0B !important;
}

.bn-brand-tagline {
    font-size: 0.82rem;
    color: #99F6E4 !important;
    font-weight: 500;
}

.bn-badge-status {
    background: rgba(15, 118, 110, 0.35);
    border: 1px solid #14B8A6;
    color: #99F6E4 !important;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.03em;
}

/* -------------------------------------------------------------
   Horizontal Navigation Bar
   ------------------------------------------------------------- */
.nav-tab-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #FFFFFF;
    padding: 6px;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.03);
    overflow-x: auto;
}

/* Streamlit Button Overrides for Navigation */
button[kind="primary"] {
    background-color: #0F766E !important;
    border: none !important;
    border-bottom: 3px solid #D97706 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    box-shadow: 0 1px 2px rgba(15, 118, 110, 0.15) !important;
    transition: all 0.15s ease !important;
}

button[kind="primary"]:hover {
    background-color: #0D9488 !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.15s ease !important;
}

button[kind="secondary"]:hover {
    background-color: #F8FAFC !important;
    color: #0F766E !important;
    border-color: #CBD5E1 !important;
}

/* -------------------------------------------------------------
   4-Step Workflow Stepper
   ------------------------------------------------------------- */
.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2D9CF;
    border-radius: 8px;
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.35rem;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.04);
}

.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    font-weight: 600;
}

.step-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    transition: all 0.2s ease;
}

/* Active Step: Peacock Teal with Antique Gold halo & Deep Indigo label */
.step-active .step-circle {
    background-color: #0F766E;
    color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.45);
    border: 2px solid #FAF8F5;
}

.step-active .step-label {
    color: #1E1B4B !important;
    font-weight: 700;
    font-size: 0.92rem;
}

/* Completed Step: Peacock/Emerald fill with checkmark */
.step-complete .step-circle {
    background-color: #0D9488;
    color: #FFFFFF !important;
}

.step-complete .step-label {
    color: #0F766E !important;
    font-weight: 600;
}

/* Pending Step: Muted Slate on Soft Ivory */
.step-pending .step-circle {
    background-color: #F1F5F9;
    color: #64748B !important;
    border: 1.5px solid #CBD5E1;
}

.step-pending .step-label {
    color: #64748B !important;
}

/* Styled Connecting Lines with Progress Fill */
.step-divider-line {
    flex: 1;
    min-width: 20px;
    height: 3px;
    background: #E2E8F0;
    margin: 0 14px;
    border-radius: 2px;
    transition: background 0.25s ease;
}

.step-divider-line.step-divider-complete {
    background: linear-gradient(90deg, #0D9488, #0F766E);
}

@media (max-width: 768px) {
    .stepper-container {
        flex-wrap: wrap;
        gap: 10px;
        padding: 0.75rem;
    }
    .step-divider-line {
        display: none;
    }
    .step-item {
        font-size: 0.82rem;
    }
}

/* -------------------------------------------------------------
   PASS / REVIEW / HOLD Disposition Badges
   ------------------------------------------------------------- */
.bn-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 700;
    font-size: 0.88rem;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 0.02em;
}

.bn-badge-pass {
    background-color: #ECFDF5;
    color: #065F46 !important;
    border: 1.5px solid #10B981;
}

.bn-badge-review {
    background-color: #FFFBEB;
    color: #92400E !important;
    border: 1.5px solid #F59E0B;
}

.bn-badge-hold {
    background-color: #FEF2F2;
    color: #991B1B !important;
    border: 1.5px solid #EF4444;
}

/* -------------------------------------------------------------
   Findings Box & Severity Border Indicators
   ------------------------------------------------------------- */
.finding-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 1.1rem 1.35rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 1px 2px rgba(30, 27, 75, 0.02);
}

.finding-crit {
    border-left: 5px solid #DC2626;
    background-color: #FFFDFD;
}

.finding-high {
    border-left: 5px solid #EA580C;
    background-color: #FFFDFB;
}

.finding-med {
    border-left: 5px solid #D97706;
}

.finding-low {
    border-left: 5px solid #0F766E;
}

/* Code Diff Box */
.diff-box {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 0.85rem 1.1rem;
    font-family: 'Plus Jakarta Sans', monospace;
    font-size: 0.92rem;
    white-space: pre-wrap;
    line-height: 1.55;
    color: #1E293B !important;
}

/* Understated Indian Geometric Divider */
.bn-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.35rem 0;
    color: #D97706 !important;
    opacity: 0.75;
}

.bn-divider::before, .bn-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E2D9CF;
}

.bn-divider:not(:empty)::before {
    margin-right: 1rem;
}

.bn-divider:not(:empty)::after {
    margin-left: 1rem;
}

.bn-jaali-icon {
    font-size: 0.95rem;
    letter-spacing: 0.2em;
    color: #D97706 !important;
}
</style>
""").strip()

def render_header(ai_connected: bool = False):
    """Renders the sleek, compact enterprise top bar with BrandNiti AI wordmark and status."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    status_text = "🟢 Gemini AI Connected" if ai_connected else "🟡 Deterministic Engine Active"
    top_bar_html = textwrap.dedent(f"""
<div class="bn-top-bar">
    <div class="bn-brand-group">
        <div class="bn-brand-title">BRAND<span class="saffron">NITI</span> AI</div>
        <div class="bn-brand-tagline">Every Brand Message. On Brand. &bull; Enterprise Governance</div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="bn-badge-status">{status_text}</span>
    </div>
</div>
""").strip()
    st.markdown(top_bar_html, unsafe_allow_html=True)

def render_stepper(current_step: int):
    """Renders the 4-step workflow stepper: Content Draft -> Policy Analysis -> Corrections -> Human Decision."""
    import streamlit as st
    steps = [
        (1, "Content Draft"),
        (2, "Policy Analysis"),
        (3, "Corrections"),
        (4, "Human Decision")
    ]
    parts = []
    for step_num, label in steps:
        if step_num < current_step:
            cls = "step-item step-complete"
            circle = "✔"
        elif step_num == current_step:
            cls = "step-item step-active"
            circle = str(step_num)
        else:
            cls = "step-item step-pending"
            circle = str(step_num)

        parts.append(
            f'<div class="{cls}"><div class="step-circle">{circle}</div><div class="step-label">{label}</div></div>'
        )

    # Connecting progress lines between each step
    dividers = []
    for idx in range(1, 4):
        div_cls = "step-divider-line step-divider-complete" if current_step > idx else "step-divider-line"
        dividers.append(f'<div class="{div_cls}"></div>')

    stepper_html = (
        f'<div class="stepper-container">'
        f'{parts[0]}{dividers[0]}'
        f'{parts[1]}{dividers[1]}'
        f'{parts[2]}{dividers[2]}'
        f'{parts[3]}'
        f'</div>'
    )
    st.markdown(stepper_html, unsafe_allow_html=True)

def render_disposition_badge(disposition: str) -> str:
    """Returns clean HTML for PASS, REVIEW, or HOLD badge without any leading indentation."""
    d = (disposition or "REVIEW").upper()
    if d == "PASS":
        return '<span class="bn-badge bn-badge-pass">✔ PASS — Compliant</span>'
    elif d == "HOLD":
        return '<span class="bn-badge bn-badge-hold">✖ HOLD — Policy Blocked</span>'
    else:
        return '<span class="bn-badge bn-badge-review">⚠ REVIEW — Verification Required</span>'

def render_divider(text: str = "◆"):
    """Renders an understated Indian-motif divider without leading indentation."""
    import streamlit as st
    divider_html = f'<div class="bn-divider"><span class="bn-jaali-icon">{text}</span></div>'
    st.markdown(divider_html, unsafe_allow_html=True)
