# ui/sidebar.py
# ─────────────────────────────────────────────────────────────────────────
# ONE unified sidebar, used by every page — Friend's visual design (gradient
# background, page-link navigation grouped by role, colored top badge).
# Per the merge spec: "Use Friend's Sidebar everywhere. No mixing. No
# duplicate navigation. One unified sidebar."
#
# No Provider/Model/API Key fields are shown here at all — the key is
# expected to come from Streamlit Cloud's Secrets panel (or a local
# .streamlit/secrets.toml, an environment variable, or config/app_config.json
# for a hardcoded value). Whichever of those has a key, the provider and
# best available model are auto-detected from the key's format via
# utils/helpers.resolve_model() — nothing to pick manually.
# ─────────────────────────────────────────────────────────────────────────

import streamlit as st

from utils.helpers import get_api_key, resolve_model, get_configured_provider_model

PAGE_BADGES = {
    "m0": ("📘", "Instructions"),
    "m1": ("📄", "Problem Definition"),
    "m2": ("📊", "Feasibility Assessment"),
    "m3": ("⚖️", "Gain-Pain Analysis"),
    "m4": ("🏛️", "Governance Review"),
    "m5": ("📊", "Analytics Dashboard"),
    "m6": ("🧑‍⚖️", "Expert Advice"),
}


def _init_llm_defaults():
    """Resolve provider + model automatically from whichever API key is
    available (Streamlit secrets > env vars > config/app_config.json),
    with zero UI. Runs once per session — call_ai() reads the results
    from st.session_state.

    If config/app_config.json explicitly sets "provider" and "model"
    (e.g. "groq" / "llama-3.3-70b-versatile"), that pair is used directly —
    no format-based auto-detection needed. Otherwise the provider is
    guessed from the API key's prefix (AIza.../sk-.../sk-ant-.../gsk_...)
    and the best available model for that provider is selected."""
    if "llm_provider" in st.session_state and "llm_model" in st.session_state:
        return

    api_key = get_api_key()

    # Config file can set provider/model even without an api_key present
    # here (e.g. key only added later in app_config.json) — but we still
    # need a key to actually call the provider, so bail out if there's none.
    if not api_key:
        return

    provider, model = resolve_model(api_key)
    st.session_state["api_key_input"] = api_key
    st.session_state["llm_provider"] = provider
    st.session_state["llm_model"] = model


def render_sidebar(active: str = "m1"):
    """Render the unified sidebar. `active` is one of PAGE_BADGES' keys."""
    _init_llm_defaults()

    icon, label = PAGE_BADGES.get(active, ("📄", "AI Governance"))
    st.sidebar.markdown(f"""
    <div style="background:#6D5DF6;padding:12px;border-radius:12px;
                margin-bottom:10px;font-weight:bold;">
    {icon} {label}
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("# 🤖 AI Governance")
        st.caption("Governance Platform")
        st.divider()

        st.subheader("Getting Started")
        st.page_link("pages/0_Instructions.py", label="📘 Instructions")

        st.subheader("Idea Submitter")
        st.page_link("app.py", label="📄 Problem Definition")

        st.subheader("Assessment Team")
        st.page_link("pages/2_Feasibility_Assessment.py", label="📊 Feasibility Assessment")
        st.page_link("pages/3_Gain_Pain_Analysis.py", label="⚖️ Gain Pain Analysis")

        st.subheader("Governance Board")
        st.page_link("pages/4_Governance_Review.py", label="🏛️ Governance Review")
        st.page_link("pages/5_Analytics_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/6_Expert_Advice.py", label="🧑‍⚖️ Expert Advice")
