import streamlit as st

st.set_page_config(
    page_title="UPI Narrator",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Dark theme CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global dark background */
    .stApp { background-color: #0F1117; color: #e2e8f0; }
    section[data-testid="stSidebar"] { display: none; }

    /* Remove default padding */
    .block-container { padding: 2rem 2rem 2rem; max-width: 1100px; }

    /* Nav bar */
    .nav-bar {
        background: #161822;
        border-bottom: 0.5px solid #2a2d3e;
        padding: 14px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        margin-bottom: 28px;
    }
    .nav-logo { font-size: 18px; font-weight: 600; color: #a78bfa; }
    .nav-logo span { color: #e2e8f0; }

    /* Metric cards */
    .metric-card {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        border-radius: 10px;
        padding: 16px;
        text-align: left;
    }
    .metric-label { font-size: 11px; color: #64748b; margin-bottom: 6px; }
    .metric-val { font-size: 22px; font-weight: 600; color: #e2e8f0; }
    .metric-sub { font-size: 11px; margin-top: 4px; }
    .up { color: #4ade80; }
    .down { color: #f87171; }
    .accent { color: #a78bfa; }

    /* Upload zone */
    .upload-zone {
        border: 1.5px dashed #2a2d3e;
        border-radius: 12px;
        padding: 48px 24px;
        text-align: center;
        background: #161822;
        margin-bottom: 20px;
    }
    .upload-title { font-size: 16px; font-weight: 500; color: #e2e8f0; margin-bottom: 8px; }
    .upload-sub { font-size: 13px; color: #64748b; line-height: 1.7; }

    /* Narrative box */
    .narr-box {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .narr-title { font-size: 14px; font-weight: 500; color: #e2e8f0; margin-bottom: 12px; }
    .narr-body {
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.85;
        border-left: 2px solid #a78bfa;
        padding-left: 14px;
    }

    /* Insight card */
    .insight-card {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .insight-tag {
        font-size: 10px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .tag-amber { background: #2d1f00; color: #fbbf24; }
    .tag-blue  { background: #0f1f3d; color: #60a5fa; }
    .tag-green { background: #0f2d1a; color: #4ade80; }
    .tag-purple{ background: #1e1040; color: #c084fc; }
    .insight-body { font-size: 13px; color: #94a3b8; line-height: 1.65; }

    /* Section heading */
    .sec-head {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.07em;
        color: #64748b;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    /* Step cards */
    .step-card {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        border-radius: 10px;
        padding: 16px;
    }
    .step-num  { font-size: 11px; font-weight: 600; color: #a78bfa; margin-bottom: 6px; }
    .step-title{ font-size: 13px; font-weight: 500; color: #e2e8f0; margin-bottom: 4px; }
    .step-desc { font-size: 12px; color: #64748b; line-height: 1.5; }

    /* Streamlit button override */
    .stButton > button {
        background: #a78bfa;
        color: #1e1040;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton > button:hover { background: #9061f9; color: #1e1040; }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #161822;
        border: 1.5px dashed #2a2d3e;
        border-radius: 12px;
        padding: 12px;
    }

    /* Tab bar */
    .stTabs [data-baseweb="tab-list"] {
        background: #161822;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border: 0.5px solid #2a2d3e;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        border-radius: 7px;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background: #1e2130 !important;
        color: #e2e8f0 !important;
    }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Plotly chart backgrounds */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* Input box */
    .stTextInput > div > div > input {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        color: #e2e8f0;
        border-radius: 8px;
    }
    div[data-testid="stSelectbox"] > div {
        background: #161822;
        border: 0.5px solid #2a2d3e;
        border-radius: 8px;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ── Nav ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">UPI<span>Narrator</span></div>
    <div style="font-size:12px;color:#64748b;">Your money, finally explained</div>
</div>
""", unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["  Upload  ", "  Dashboard  ", "  My Story  ", "  Insights  "])

with tab1:
    from pages.upload import render
    render()

with tab2:
    from pages.dashboard import render
    render()

with tab3:
    from pages.narrative import render
    render()

with tab4:
    from pages.insights import render
    render()
