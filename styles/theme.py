"""Indian Heritage × Modern AI Visual Identity & Styling System for BrandNiti AI.
Refined palette:
- Deep Indigo: #1E1B4B / #312E81
- Peacock Teal: #0F766E / #14B8A6
- Warm Ivory / Cream: #FAF8F5 / #F3EDE2
- Antique Gold / Saffron Accent: #D97706 / #B45309
- High-contrast accessible status tokens for PASS, REVIEW, HOLD.
"""

CUSTOM_CSS = """
<style>
/* -------------------------------------------------------------
   Typography & Canvas Setup
   ------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cinzel:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1E1B4B;
}

.stApp {
    background-color: #FAF8F5;
}

/* Sidebar styling with subtle heritage tone */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #18153A 0%, #0F172A 100%);
    color: #F8FAFC;
    border-right: 1px solid rgba(217, 119, 6, 0.2);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
    color: #E2E8F0 !important;
}

/* -------------------------------------------------------------
   BrandNiti Brand Header & Wordmark
   ------------------------------------------------------------- */
.bn-header {
    background: linear-gradient(135deg, #1E1B4B 0%, #172554 60%, #0F766E 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    color: #FFFFFF;
    margin-bottom: 1.75rem;
    border-bottom: 3px solid #D97706;
    box-shadow: 0 4px 20px -2px rgba(30, 27, 75, 0.15);
    position: relative;
    overflow: hidden;
}

.bn-header::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 280px;
    height: 100%;
    opacity: 0.08;
    background-image: radial-gradient(#D97706 2px, transparent 2px), radial-gradient(#14B8A6 2px, transparent 2px);
    background-size: 24px 24px;
    background-position: 0 0, 12px 12px;
    pointer-events: none;
}

.bn-title {
    font-family: 'Cinzel', serif;
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #FFFFFF;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.bn-title span.saffron {
    color: #F59E0B;
}

.bn-tagline {
    font-size: 0.95rem;
    color: #99F6E4;
    font-weight: 500;
    margin-top: 4px;
    letter-spacing: 0.02em;
}

.bn-badge-team {
    display: inline-block;
    background: rgba(217, 119, 6, 0.25);
    border: 1px solid rgba(245, 158, 11, 0.5);
    color: #FDE68A;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}

/* -------------------------------------------------------------
   Geometric Motif Divider (Indian Jaali inspiration)
   ------------------------------------------------------------- */
.bn-divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin: 1.5rem 0;
    color: #D97706;
    opacity: 0.8;
}

.bn-divider::before, .bn-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #E2D9CF;
}

.bn-divider:not(:empty)::before {
    margin-right: 1em;
}

.bn-divider:not(:empty)::after {
    margin-left: 1em;
}

.bn-jaali-icon {
    font-size: 1rem;
    letter-spacing: 0.2em;
}

/* -------------------------------------------------------------
   Modern Executive Cards
   ------------------------------------------------------------- */
.bn-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #E5E7EB;
    border-left: 4px solid #0F766E;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    margin-bottom: 1.2rem;
}

.bn-card-gold {
    border-left: 4px solid #D97706;
}

.bn-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1E1B4B;
    margin-bottom: 0.35rem;
}

/* -------------------------------------------------------------
   PASS / REVIEW / HOLD Disposition Badges
   ------------------------------------------------------------- */
.badge-pass {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background-color: #ECFDF5;
    color: #065F46;
    border: 1.5px solid #10B981;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

.badge-review {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background-color: #FFFBEB;
    color: #92400E;
    border: 1.5px solid #F59E0B;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

.badge-hold {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background-color: #FEF2F2;
    color: #991B1B;
    border: 1.5px solid #EF4444;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 4px 12px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

/* -------------------------------------------------------------
   Findings Card & Severity Tokens
   ------------------------------------------------------------- */
.finding-box {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.85rem;
}

.finding-crit {
    border-left: 5px solid #DC2626;
    background-color: #FFFDFD;
}

.finding-high {
    border-left: 5px solid #EA580C;
    background-color: #FFFDF9;
}

.finding-med {
    border-left: 5px solid #F59E0B;
}

.finding-low {
    border-left: 5px solid #0F766E;
}

/* Metric Tiles */
.metric-tile {
    background: #FFFFFF;
    padding: 1rem 1.2rem;
    border-radius: 8px;
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.metric-tile .num {
    font-size: 1.85rem;
    font-weight: 800;
    color: #1E1B4B;
    line-height: 1.2;
}

.metric-tile .lbl {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 4px;
}

/* Revision Diff Container */
.diff-box {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 0.85rem;
    font-family: monospace;
    font-size: 0.88rem;
    white-space: pre-wrap;
    line-height: 1.45;
}

/* Streamlit button refinements */
button[kind="primary"] {
    background-color: #1E1B4B !important;
    border-color: #1E1B4B !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border-radius: 6px !important;
}

button[kind="primary"]:hover {
    background-color: #0F766E !important;
    border-color: #0F766E !important;
}
</style>
"""

def render_header(subtitle: str = ""):
    """Renders the top BrandNiti AI visual header with heritage wordmark."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="bn-header">
        <div class="bn-title">
            <span>BRAND<span class="saffron">NITI</span> AI</span>
            <span style="font-size: 1.2rem; opacity: 0.8; font-weight: 400;">|</span>
            <span style="font-size: 1.05rem; font-weight: 500; font-family: 'Plus Jakarta Sans', sans-serif;">Governance Studio</span>
        </div>
        <div class="bn-tagline">Every Brand Message. On Brand.</div>
        <div class="bn-badge-team">Team TWIN SOCH — Two Minds. One Vision.</div>
    </div>
    """, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div style='font-size: 1.25rem; font-weight: 700; color: #1E1B4B; margin-bottom: 1rem;'>{subtitle}</div>", unsafe_allow_html=True)

def render_disposition_badge(disposition: str) -> str:
    """Returns HTML for PASS, REVIEW, or HOLD badge."""
    d = (disposition or "REVIEW").upper()
    if d == "PASS":
        return '<span class="badge-pass">✔ PASS — Clear to Proceed</span>'
    elif d == "HOLD":
        return '<span class="badge-hold">✖ HOLD — Blocked Pending Fix</span>'
    else:
        return '<span class="badge-review">⚠ REVIEW — Needs Verification</span>'

def render_divider(text: str = "◆"):
    """Renders an understated Indian-motif divider."""
    import streamlit as st
    st.markdown(f'<div class="bn-divider"><span class="bn-jaali-icon">{text}</span></div>', unsafe_allow_html=True)
