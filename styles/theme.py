"""Indian Heritage × Modern AI Visual Identity & Styling System for BrandNiti AI.
Enterprise SaaS styling:
- Deep Indigo (#1E1B4B, #17143A) for primary navigation and visual anchors
- Peacock Teal (#0F766E, #0D9488) for primary CTAs and active states
- Warm Ivory / Soft Off-White (#FAF8F5) for comfortable canvas background
- Antique Gold / Muted Saffron (#D97706, #B45309) for restrained highlights
- Compact, professional enterprise header (no oversized banners)
- All HTML blocks use strict textwrap.dedent to prevent CommonMark indented-code-block leaks.
"""
import textwrap

CUSTOM_CSS = textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1E293B;
    font-size: 15px;
    line-height: 1.6;
}

.stApp {
    background-color: #FAF8F5;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17143A 0%, #0F172A 100%);
    color: #F8FAFC;
    border-right: 1px solid rgba(217, 119, 6, 0.25);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
    color: #E2E8F0 !important;
    font-size: 14px;
}

/* Streamlit main block container spacing */
.main .block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 3rem !important;
    max-width: 1260px;
}

/* -------------------------------------------------------------
   Compact Enterprise Top Brand Bar (Sleek, no oversized banner)
   ------------------------------------------------------------- */
.bn-top-bar {
    background: linear-gradient(90deg, #1E1B4B 0%, #1E2248 55%, #0F766E 100%);
    padding: 0.9rem 1.4rem;
    border-radius: 8px;
    color: #FFFFFF;
    margin-bottom: 1.25rem;
    border-bottom: 2.5px solid #D97706;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(30, 27, 75, 0.08);
}

.bn-brand-group {
    display: flex;
    flex-direction: column;
}

.bn-brand-title {
    font-family: 'Cinzel', serif;
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #FFFFFF;
    line-height: 1.2;
}

.bn-brand-title span.saffron {
    color: #F59E0B;
}

.bn-brand-tagline {
    font-size: 0.85rem;
    color: #99F6E4;
    font-weight: 500;
    margin-top: 2px;
}

.bn-badge-edition {
    background: rgba(217, 119, 6, 0.25);
    border: 1px solid #D97706;
    color: #FDE68A;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Page Section Heading */
.bn-page-heading {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1E1B4B;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* -------------------------------------------------------------
   Understated Geometric Dividers
   ------------------------------------------------------------- */
.bn-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.35rem 0;
    color: #D97706;
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
}

/* -------------------------------------------------------------
   Enterprise Cards & Metric Displays
   ------------------------------------------------------------- */
.bn-card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 1.25rem 1.4rem;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0F766E;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.03);
    margin-bottom: 1rem;
}

.bn-card-gold {
    border-left: 4px solid #D97706;
}

.bn-card-indigo {
    border-left: 4px solid #1E1B4B;
}

.bn-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1E1B4B;
    margin-bottom: 0.35rem;
}

.bn-card-desc {
    color: #475569;
    font-size: 0.92rem;
    line-height: 1.55;
}

/* Metric Display Tiles */
.metric-tile {
    background: #FFFFFF;
    padding: 1rem 1.15rem;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 1px 2px rgba(30, 27, 75, 0.03);
}

.metric-tile .num {
    font-size: 2rem;
    font-weight: 800;
    color: #1E1B4B;
    line-height: 1.15;
}

.metric-tile .lbl {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 4px;
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
    color: #065F46;
    border: 1.5px solid #10B981;
}

.bn-badge-review {
    background-color: #FFFBEB;
    color: #92400E;
    border: 1.5px solid #F59E0B;
}

.bn-badge-hold {
    background-color: #FEF2F2;
    color: #991B1B;
    border: 1.5px solid #EF4444;
}

/* -------------------------------------------------------------
   Findings Box & Severity Border Indicators
   ------------------------------------------------------------- */
.finding-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
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
    color: #1E293B;
}

/* Buttons */
button[kind="primary"] {
    background-color: #0F766E !important;
    border-color: #0F766E !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.2rem !important;
}

button[kind="primary"]:hover {
    background-color: #0D9488 !important;
    border-color: #0D9488 !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #1E1B4B !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border-radius: 6px !important;
}
</style>
""").strip()

def render_header(subtitle: str = ""):
    """Renders the sleek, compact enterprise top bar with BrandNiti AI wordmark and page title."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    top_bar_html = textwrap.dedent("""
<div class="bn-top-bar">
    <div class="bn-brand-group">
        <div class="bn-brand-title">BRAND<span class="saffron">NITI</span> AI</div>
        <div class="bn-brand-tagline">Every Brand Message. On Brand. &bull; Enterprise Governance</div>
    </div>
    <div class="bn-badge-edition">Governance Studio</div>
</div>
""").strip()
    st.markdown(top_bar_html, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="bn-page-heading">{subtitle}</div>', unsafe_allow_html=True)

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
