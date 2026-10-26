"""Indian Heritage × Modern AI Visual Identity & Styling System for BrandNiti AI.
Enterprise SaaS design system featuring:
- Deep Indigo (#1E1B4B, #161338) for structural navigation and visual anchors
- Peacock Teal (#0F766E, #0D9488) for primary CTAs and active states
- Warm Ivory / Soft Off-White (#FAF8F5, #F5F2EC) for comfortable canvas background
- Antique Gold / Muted Saffron (#D97706, #B45309) for restrained highlights
- Accessible, high-contrast typography and clear disposition tokens (PASS, REVIEW, HOLD)
"""

CUSTOM_CSS = """
<style>
/* -------------------------------------------------------------
   Typography & Canvas Setup
   ------------------------------------------------------------- */
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

/* Sidebar styling with subtle indigo heritage tone */
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
    padding-top: 1.75rem;
    padding-bottom: 3.5rem;
    max-width: 1280px;
}

/* -------------------------------------------------------------
   BrandNiti Enterprise Header & Wordmark
   ------------------------------------------------------------- */
.bn-header {
    background: linear-gradient(135deg, #1E1B4B 0%, #192147 60%, #0F766E 100%);
    padding: 1.75rem 2.25rem;
    border-radius: 12px;
    color: #FFFFFF;
    margin-bottom: 1.75rem;
    border-bottom: 3px solid #D97706;
    box-shadow: 0 4px 20px -2px rgba(30, 27, 75, 0.12);
    position: relative;
    overflow: hidden;
}

.bn-header::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 320px;
    height: 100%;
    opacity: 0.07;
    background-image: radial-gradient(#D97706 2px, transparent 2px), radial-gradient(#14B8A6 2px, transparent 2px);
    background-size: 24px 24px;
    background-position: 0 0, 12px 12px;
    pointer-events: none;
}

.bn-brand-container {
    display: flex;
    align-items: center;
    gap: 16px;
}

.bn-logo-svg {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
}

.bn-title {
    font-family: 'Cinzel', serif;
    font-size: 1.95rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.2;
}

.bn-title span.saffron {
    color: #F59E0B;
}

.bn-tagline {
    font-size: 1.02rem;
    color: #99F6E4;
    font-weight: 500;
    margin-top: 4px;
    letter-spacing: 0.015em;
}

.bn-subphrase {
    font-size: 0.82rem;
    color: #E2E8F0;
    opacity: 0.9;
    margin-top: 6px;
    letter-spacing: 0.02em;
}

/* -------------------------------------------------------------
   Geometric Motif Divider (Understated Indian symmetry)
   ------------------------------------------------------------- */
.bn-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.75rem 0;
    color: #D97706;
    opacity: 0.75;
}

.bn-divider::before, .bn-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E2D9CF;
}

.bn-divider:not(:empty)::before {
    margin-right: 1.2em;
}

.bn-divider:not(:empty)::after {
    margin-left: 1.2em;
}

.bn-jaali-icon {
    font-size: 1.1rem;
    letter-spacing: 0.25em;
}

/* -------------------------------------------------------------
   Enterprise Cards & Surfaces
   ------------------------------------------------------------- */
.bn-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #0F766E;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.04);
    margin-bottom: 1.25rem;
}

.bn-card-gold {
    border-left: 4px solid #D97706;
}

.bn-card-indigo {
    border-left: 4px solid #1E1B4B;
}

.bn-card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1E1B4B;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.bn-card-desc {
    color: #475569;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* -------------------------------------------------------------
   PASS / REVIEW / HOLD Disposition Badges
   ------------------------------------------------------------- */
.badge-pass {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background-color: #ECFDF5;
    color: #065F46;
    border: 1.5px solid #10B981;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 5px 14px;
    border-radius: 6px;
    letter-spacing: 0.03em;
}

.badge-review {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background-color: #FFFBEB;
    color: #92400E;
    border: 1.5px solid #F59E0B;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 5px 14px;
    border-radius: 6px;
    letter-spacing: 0.03em;
}

.badge-hold {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background-color: #FEF2F2;
    color: #991B1B;
    border: 1.5px solid #EF4444;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 5px 14px;
    border-radius: 6px;
    letter-spacing: 0.03em;
}

/* -------------------------------------------------------------
   Findings Card & Severity Tokens
   ------------------------------------------------------------- */
.finding-box {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
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
    background-color: #FFFFFD;
}

.finding-low {
    border-left: 5px solid #0F766E;
}

/* Metric Tiles */
.metric-tile {
    background: #FFFFFF;
    padding: 1.25rem 1.4rem;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 1px 3px rgba(30, 27, 75, 0.04);
}

.metric-tile .num {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1E1B4B;
    line-height: 1.15;
}

.metric-tile .lbl {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 6px;
}

/* Revision Diff Container */
.diff-box {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: 'Plus Jakarta Sans', monospace;
    font-size: 0.95rem;
    white-space: pre-wrap;
    line-height: 1.6;
    color: #1E293B;
}

/* Streamlit button refinements: Peacock Teal primary */
button[kind="primary"] {
    background-color: #0F766E !important;
    border-color: #0F766E !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 1.25rem !important;
    letter-spacing: 0.02em !important;
    border-radius: 6px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.15s ease-in-out !important;
}

button[kind="primary"]:hover {
    background-color: #0D9488 !important;
    border-color: #0D9488 !important;
    box-shadow: 0 3px 6px rgba(15, 118, 110, 0.25) !important;
}

button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border-color: #CBD5E1 !important;
    color: #1E1B4B !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    border-radius: 6px !important;
}

button[kind="secondary"]:hover {
    background-color: #F1F5F9 !important;
    border-color: #94A3B8 !important;
}

/* Form input refinement */
input, textarea, select {
    font-size: 0.95rem !important;
}

/* Clean expander headers */
.streamlit-expanderHeader {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #1E1B4B !important;
}
</style>
"""

BRAND_SVG_EMBLEM = """
<svg class="bn-logo-svg" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,4 96,50 50,96 4,50" stroke="#D97706" stroke-width="2.5" fill="rgba(217, 119, 6, 0.08)"/>
  <rect x="22" y="22" width="56" height="56" rx="6" stroke="#14B8A6" stroke-width="2.2" fill="none"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#FDE68A" stroke-width="2.2" stroke-linecap="round"/>
  <line x1="28" y1="40" x2="72" y2="40" stroke="#FDE68A" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M28 40 L24 58 C24 62 32 62 32 58 Z" fill="#14B8A6" stroke="#99F6E4" stroke-width="1.5"/>
  <path d="M72 40 L68 58 C68 62 76 62 76 58 Z" fill="#14B8A6" stroke="#99F6E4" stroke-width="1.5"/>
  <polygon points="50,33 55,40 50,47 45,40" fill="#F59E0B"/>
  <circle cx="50" cy="50" r="3" fill="#FFFFFF"/>
</svg>
"""

def render_header(subtitle: str = ""):
    """Renders the top BrandNiti AI visual header with refined SVG emblem and enterprise identity."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="bn-header">
        <div class="bn-brand-container">
            {BRAND_SVG_EMBLEM}
            <div>
                <div class="bn-title">
                    BRAND<span class="saffron">NITI</span> AI
                    <span style="font-size: 1.15rem; opacity: 0.6; font-weight: 300; margin: 0 8px;">|</span>
                    <span style="font-size: 1.05rem; font-weight: 500; font-family: 'Plus Jakarta Sans', sans-serif;">Enterprise Governance Studio</span>
                </div>
                <div class="bn-tagline">Every Brand Message. On Brand.</div>
                <div class="bn-subphrase">AI-powered brand governance. Create confidently. Review intelligently. Publish responsibly.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div style='font-size: 1.35rem; font-weight: 700; color: #1E1B4B; margin-bottom: 1.25rem;'>{subtitle}</div>", unsafe_allow_html=True)

def render_disposition_badge(disposition: str) -> str:
    """Returns HTML for PASS, REVIEW, or HOLD badge with accessible icons."""
    d = (disposition or "REVIEW").upper()
    if d == "PASS":
        return '<span class="badge-pass">✔ PASS — Compliant</span>'
    elif d == "HOLD":
        return '<span class="badge-hold">✖ HOLD — Policy Blocked</span>'
    else:
        return '<span class="badge-review">⚠ REVIEW — Verification Required</span>'

def render_divider(text: str = "◆"):
    """Renders an understated Indian-motif divider."""
    import streamlit as st
    st.markdown(f'<div class="bn-divider"><span class="bn-jaali-icon">{text}</span></div>', unsafe_allow_html=True)
