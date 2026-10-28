"""BrandNiti AI — Modern Enterprise Brand-Governance Theme & Styling System.
Visual Identity: White + Deep Green + Red Premium Enterprise Identity.
- Main background: #F8FAFC
- Cards and panels: #FFFFFF
- Primary green: #166534
- Dark green headings: #14532D
- Light green surfaces: #DCFCE7
- Primary text: #0F172A
- Secondary text: #64748B
- Borders: #E2E8F0
- Critical/HOLD red: #DC2626
- Light red warning surface: #FEE2E2
- REVIEW amber: #A16207
- Light amber warning surface: #FEF3C7
"""
import textwrap

CUSTOM_CSS = textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Canvas & Global Reset */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
    font-size: 15px;
    line-height: 1.6;
}

/* Typography Hierarchy */
h1, h2, h3, h4, h5, h6, [data-testid="stHeader"] {
    color: #14532D !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.015em;
}

h1 { font-size: 1.85rem !important; margin-bottom: 0.5rem !important; }
h2 { font-size: 1.35rem !important; margin-top: 0.85rem !important; margin-bottom: 0.4rem !important; }
h3 { font-size: 1.15rem !important; margin-top: 0.75rem !important; }
h4 { font-size: 1.0rem !important; }

p, span, div, li, [data-testid="stMarkdownContainer"] p {
    color: #0F172A;
}

/* Secondary muted text */
.text-secondary {
    color: #64748B !important;
    font-size: 0.875rem;
}

/* Form Widget Labels */
[data-testid="stWidgetLabel"] p, label, [data-testid="stWidgetLabel"] label {
    color: #14532D !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-bottom: 4px !important;
}

/* Form Inputs, Textareas, and Selectboxes */
input, textarea, select, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea, [data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 6px !important;
    font-size: 0.92rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

input:focus, textarea:focus, select:focus, [data-baseweb="input"] input:focus, [data-baseweb="textarea"] textarea:focus {
    border-color: #166534 !important;
    box-shadow: 0 0 0 3px rgba(22, 101, 52, 0.15) !important;
    outline: none !important;
}

/* Streamlit Native Metric Value and Label */
[data-testid="stMetricValue"] {
    color: #14532D !important;
    font-weight: 800 !important;
    font-size: 1.75rem !important;
    letter-spacing: -0.02em;
}

[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* Container & Bordered Panels */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
}

/* Streamlit Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
}

[data-testid="stExpander"] details summary span p {
    color: #0F172A !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Streamlit Layout Block Spacing */
.main .block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px;
}

/* -------------------------------------------------------------
   BrandNiti AI Enterprise Header Bar
   ------------------------------------------------------------- */
.bn-top-bar {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 3.5px solid #166534;
    padding: 0.9rem 1.4rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
}

.bn-brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
}

.bn-brand-shield {
    background: #DCFCE7;
    color: #166534;
    width: 38px;
    height: 38px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    border: 1px solid #86EFAC;
}

.bn-brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #14532D !important;
    line-height: 1.15;
}

.bn-brand-title span.accent {
    color: #166534 !important;
}

.bn-brand-tagline {
    font-size: 0.8rem;
    color: #64748B !important;
    font-weight: 500;
    margin-top: 2px;
}

.bn-badge-status {
    background: #DCFCE7;
    border: 1px solid #86EFAC;
    color: #14532D !important;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.bn-badge-status-neutral {
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    color: #334155 !important;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

/* -------------------------------------------------------------
   Buttons: Primary (Green) & Secondary (White / Slate)
   ------------------------------------------------------------- */
button[kind="primary"] {
    background-color: #166534 !important;
    border: 1px solid #14532D !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    box-shadow: 0 1px 2px rgba(22, 101, 52, 0.12) !important;
    transition: all 0.15s ease !important;
}

button[kind="primary"]:hover {
    background-color: #14532D !important;
    border-color: #052E16 !important;
    box-shadow: 0 2px 4px rgba(20, 83, 45, 0.2) !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #0F172A !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.15s ease !important;
}

button[kind="secondary"]:hover {
    background-color: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #166534 !important;
}

/* -------------------------------------------------------------
   4-Step Workflow Stepper
   ------------------------------------------------------------- */
.stepper-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.35rem;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
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

/* Active Step: Deep Green with subtle ring */
.step-active .step-circle {
    background-color: #166534;
    color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(22, 101, 52, 0.22);
    border: 2px solid #FFFFFF;
}

.step-active .step-label {
    color: #14532D !important;
    font-weight: 700;
    font-size: 0.92rem;
}

/* Completed Step: Primary Green fill with checkmark */
.step-complete .step-circle {
    background-color: #166534;
    color: #FFFFFF !important;
}

.step-complete .step-label {
    color: #166534 !important;
    font-weight: 600;
}

/* Pending Step: Muted Slate on Soft Canvas */
.step-pending .step-circle {
    background-color: #F1F5F9;
    color: #64748B !important;
    border: 1.5px solid #CBD5E1;
}

.step-pending .step-label {
    color: #64748B !important;
}

/* Connecting lines with progress fill */
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
    background: #166534;
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
    background-color: #DCFCE7;
    color: #14532D !important;
    border: 1.5px solid #86EFAC;
}

.bn-badge-review {
    background-color: #FEF3C7;
    color: #A16207 !important;
    border: 1.5px solid #FCD34D;
}

.bn-badge-hold {
    background-color: #FEE2E2;
    color: #DC2626 !important;
    border: 1.5px solid #FCA5A5;
}

/* Workflow Status Tags */
.bn-status-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 4px;
    letter-spacing: 0.02em;
}

.bn-status-approved {
    background-color: #DCFCE7;
    color: #14532D !important;
    border: 1px solid #86EFAC;
}

.bn-status-changes {
    background-color: #FEF3C7;
    color: #A16207 !important;
    border: 1px solid #FCD34D;
}

.bn-status-rejected {
    background-color: #FEE2E2;
    color: #DC2626 !important;
    border: 1px solid #FCA5A5;
}

.bn-status-pending {
    background-color: #F1F5F9;
    color: #334155 !important;
    border: 1px solid #CBD5E1;
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
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}

.finding-crit {
    border-left: 4px solid #DC2626;
    background-color: #FFFFFF;
}

.finding-high {
    border-left: 4px solid #EA580C;
    background-color: #FFFFFF;
}

.finding-med {
    border-left: 4px solid #A16207;
    background-color: #FFFFFF;
}

.finding-low {
    border-left: 4px solid #166534;
    background-color: #FFFFFF;
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
    color: #0F172A !important;
}

/* Clean Divider */
.bn-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.25rem 0;
    color: #94A3B8 !important;
}

.bn-divider::before, .bn-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E2E8F0;
}

.bn-divider:not(:empty)::before {
    margin-right: 1rem;
}

.bn-divider:not(:empty)::after {
    margin-left: 1rem;
}

.bn-divider-dot {
    font-size: 0.85rem;
    color: #94A3B8 !important;
}

/* Modern Empty State Container */
.bn-empty-state {
    background: #FFFFFF;
    border: 1px dashed #CBD5E1;
    border-radius: 8px;
    padding: 2.25rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.bn-empty-icon {
    font-size: 2.2rem;
    margin-bottom: 0.75rem;
    color: #64748B;
}
.bn-empty-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #14532D;
    margin-bottom: 0.4rem;
}
.bn-empty-desc {
    font-size: 0.88rem;
    color: #64748B;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.5;
}
</style>
""").strip()

def render_header(ai_connected: bool = False):
    """Renders the modern, clean enterprise header bar with BrandNiti AI shield mark and status."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    if ai_connected:
        status_html = '<span class="bn-badge-status">🟢 Gemini AI Active</span>'
    else:
        status_html = '<span class="bn-badge-status-neutral">⚪ Deterministic Engine Active</span>'

    top_bar_html = textwrap.dedent(f"""
<div class="bn-top-bar">
    <div class="bn-brand-group">
        <div class="bn-brand-shield">🛡️</div>
        <div>
            <div class="bn-brand-title">BRAND<span class="accent">NITI</span> AI</div>
            <div class="bn-brand-tagline">AI-Powered Brand Governance &bull; Enterprise Compliance Platform</div>
        </div>
    </div>
    <div>
        {status_html}
    </div>
</div>
""").strip()
    st.markdown(top_bar_html, unsafe_allow_html=True)

def render_stepper(current_step: int):
    """Renders the 4-step workflow stepper: Content Draft -> Policy Analysis -> Corrections -> Human Decision.
    Guaranteed zero 4-space indentation to avoid CommonMark code block conversion.
    """
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

def render_status_badge(status: str) -> str:
    """Returns clean HTML badge for workflow statuses."""
    s = (status or "SUBMITTED").upper()
    if s == "APPROVED":
        return '<span class="bn-status-tag bn-status-approved">✔ APPROVED</span>'
    elif s == "CHANGES_REQUESTED":
        return '<span class="bn-status-tag bn-status-changes">✎ CHANGES REQUESTED</span>'
    elif s == "REJECTED":
        return '<span class="bn-status-tag bn-status-rejected">✖ REJECTED</span>'
    elif s == "IN_REVIEW":
        return '<span class="bn-status-tag bn-status-pending">⏳ IN REVIEW</span>'
    else:
        return f'<span class="bn-status-tag bn-status-pending">📥 {s}</span>'

def render_divider(text: str = "•"):
    """Renders a clean divider without leading indentation."""
    import streamlit as st
    divider_html = f'<div class="bn-divider"><span class="bn-divider-dot">{text}</span></div>'
    st.markdown(divider_html, unsafe_allow_html=True)

def render_empty_state_html(icon: str, title: str, description: str) -> str:
    """Returns clean HTML for an empty state with zero leading indentation."""
    return (
        f'<div class="bn-empty-state">\n'
        f'<div class="bn-empty-icon">{icon}</div>\n'
        f'<div class="bn-empty-title">{title}</div>\n'
        f'<div class="bn-empty-desc">{description}</div>\n'
        f'</div>'
    )

def render_severity_badge(severity: str) -> str:
    """Returns colored HTML badge for rule severity."""
    sev = (severity or "LOW").upper()
    if sev == "CRITICAL":
        return '<span style="background: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; font-size: 0.74rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.02em;">CRITICAL BLOCKER</span>'
    elif sev == "HIGH":
        return '<span style="background: #FFF7ED; color: #EA580C; border: 1px solid #FDBA74; font-size: 0.74rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.02em;">HIGH SEVERITY</span>'
    elif sev == "MEDIUM":
        return '<span style="background: #FEF3C7; color: #A16207; border: 1px solid #FCD34D; font-size: 0.74rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.02em;">MEDIUM PRIORITY</span>'
    else:
        return '<span style="background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; font-size: 0.74rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; letter-spacing: 0.02em;">LOW / ADVISORY</span>'

def render_metric_card_html(label: str, value: str | int, hint: str = "", accent_color: str = "#166534") -> str:
    """Returns clean HTML for a styled dashboard metric card with zero leading indentation."""
    hint_html = f'<div style="font-size: 0.78rem; color: #64748B; margin-top: 5px;">{hint}</div>\n' if hint else ""
    return (
        f'<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3.5px solid {accent_color}; border-radius: 8px; padding: 1.1rem 1.25rem; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);">\n'
        f'<div style="color: #64748B; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px;">{label}</div>\n'
        f'<div style="color: #14532D; font-weight: 800; font-size: 1.85rem; line-height: 1.1; letter-spacing: -0.02em;">{value}</div>\n'
        f'{hint_html}'
        f'</div>'
    )
