# ui/theme.py
# ─────────────────────────────────────────────────────────────────────────
# All visual styling is taken from Friend's Project, verbatim, exactly as
# implemented (colors, gradients, card/stepper/button styles, background
# watermark). The only change here is mechanical: instead of pasting the
# same ~150 lines of <style> blocks into six separate page files (which is
# how Friend's original project was wired), it now lives in one function so
# every page is guaranteed to look identical — "one seamless application,
# not two projects stitched together" per the merge brief, and the
# explicit instruction that there be "One unified sidebar. No mixing."
# ─────────────────────────────────────────────────────────────────────────

import base64
import streamlit as st

LOGO_PATH = "assets/logo.png"


def _get_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def apply_global_styles():
    """Inject Friend's global CSS — sidebar gradient, cards, buttons, etc."""

    # Hide default Streamlit multipage nav + sidebar gradient + sidebar text
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display:none; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071126, #0B1734, #071126);
    }
    section[data-testid="stSidebar"] * { color:white; }
    </style>
    """, unsafe_allow_html=True)

    # Card-title containers + score number/label (used on Feasibility /
    # Governance Review / Analytics pages)
    st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:has(.card-title) {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    .score-number { text-align:center; font-size:72px; font-weight:700; }
    .score-label  { text-align:center; font-size:24px; font-weight:600; color:#22c55e; }
    </style>
    """, unsafe_allow_html=True)

    # Select-box accent
    st.markdown("""
    <style>
    div[data-baseweb="select"] > div{
        background: linear-gradient(135deg, #6C63FF, #5A54E8) !important;
        color:white !important;
        border:none !important;
        border-radius:14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main layout / card / stepper / button / review-box styling
    st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .block-container { padding-top: 1.5rem; max-width: 1400px; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a, #111827); }
    [data-testid="stSidebar"] * { color: white; }
    .card {
        background: white; border: 1px solid #e5e7eb; border-radius: 16px;
        padding: 24px; min-height: 320px; box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }
    .stepper {
        background: white; border: 1px solid #e5e7eb; border-radius: 12px;
        padding: 18px; margin-bottom: 20px;
    }
    .stButton > button {
        background-color: #6D5DFC; color: white; border: none;
        border-radius: 8px; font-weight: 600;
    }
    .stButton > button:hover { background-color: #5848f5; color: white; }
    .review-box {
        border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; background: white;
    }
    .review-label { font-weight: 600; color: #4b5563; margin-top: 12px; }
    </style>
    """, unsafe_allow_html=True)


    # Status badges (Module 5 dashboard / status displays) — colors carried
    # over unchanged from My Project's STATUS_BADGE mapping in config/constants.py
    st.markdown("""
    <style>
    .badge { display:inline-block; padding:3px 11px; border-radius:20px; font-size:0.73rem; font-weight:700; }
    .b-submitted { background:#EDE9FF; color:#4A42CC; }
    .b-review    { background:#FFF3CD; color:#856404; }
    .b-approved  { background:#D1F5EA; color:#0f6e56; }
    .b-rejected  { background:#FDE8E8; color:#c0392b; }
    .b-deferred  { background:#F0F0F0; color:#555; }
    </style>
    """, unsafe_allow_html=True)


def apply_background_logo():
    """Faint centered logo watermark behind page content — Friend's design."""
    try:
        logo_base64 = _get_base64(LOGO_PATH)
    except Exception:
        return
    st.markdown(f"""
    <style>
    .stApp::before {{
        content: "";
        position: fixed;
        top: 50%; left: 50%;
        width: 700px; height: 700px;
        transform: translate(-50%, -50%);
        background-image: url("data:image/png;base64,{logo_base64}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.08;
        z-index: 1;
        pointer-events: none;
    }}
    </style>
    """, unsafe_allow_html=True)


def apply_theme():
    """Call once near the top of every page."""
    apply_global_styles()
    apply_background_logo()
