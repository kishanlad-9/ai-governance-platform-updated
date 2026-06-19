# pages/2_Feasibility_Assessment.py
#
# MODULE 2 — Feasibility Assessment.
#   Part 1 (problem selection: dropdown, cards, header, layout) — Friend's
#           Project, unchanged.
#   Part 2 (AI feasibility logic, scoring, verdict, ISO/NIST mappings,
#           recommendations) — My Project, unchanged formulas/prompts.
#
# New flow per merge spec: everything happens on ONE scrollable page, in
# this order — Problem Selection -> Assessment Running -> Dimension Scores
# -> Reasoning -> Verdict -> Recommendations. No extra buttons, no second
# page: selecting a problem from the dropdown is the only action needed:
# the AI assessment runs automatically and the rest of the page renders
# sequentially below it.

import streamlit as st
import pandas as pd
from datetime import datetime

from database.problem_repository import get_problems
from database.db import db_get_problem, db_save_assessment, db_update_status, db_load_assessments
from config.constants import ASSESSMENT_DIMENSIONS, VERDICT_CONFIG
from utils.helpers import get_completeness_color, call_m2_assessment

from ui.theme import apply_theme
from ui.sidebar import render_sidebar

st.set_page_config(page_title="AI Governance Platform", page_icon="🤖",
                    layout="wide", initial_sidebar_state="expanded")

apply_theme()
render_sidebar("m2")

# ==========================
# PAGE TITLE  (Friend's — Part 1)
# ==========================

st.title("AI Feasibility Assessment")
st.caption("Evaluate AI readiness and feasibility of submitted business problems.")

# ==========================================
# PROBLEM SELECTION  (Friend's — Part 1)
# ==========================================

problems = get_problems()

if not problems:
    st.warning("No problems found. Please submit a problem in Module 1 first.")
    st.stop()

problem_dict = {row[1]: row[0] for row in problems}
problem_options = ["-- Select a Problem --"] + list(problem_dict.keys())

selected_problem = st.selectbox("Select AI Opportunity", problem_options)

if selected_problem == "-- Select a Problem --":
    st.info("Please select a problem to begin analysis.")
    st.stop()

problem_id = problem_dict[selected_problem]
problem = db_get_problem(problem_id)

with st.container(border=True):
    st.markdown('<span class="card-title"></span>', unsafe_allow_html=True)
    st.subheader("Problem Summary")
    st.info(problem.get("problem_statement", ""))
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Business Objective**")
        st.write(problem.get("business_objective", "") or "—")
        st.write("**Proposed Solution**")
        st.write(problem.get("solution_approach", "") or "—")
    with c2:
        st.write("**Timeline**")
        st.write(problem.get("timeline", "") or "—")
        st.write("**Owner**")
        st.write(problem.get("action_owner", "") or "—")

st.divider()

# ==========================================
# PART 2 — AI FEASIBILITY LOGIC (My Project)
# ==========================================

st.markdown("### 🤖 AI Analysis")
st.caption("AI is evaluating feasibility across 6 dimensions — "
           "AI Suitability, Economic Viability, Data & Technology Readiness, "
           "Workflow Maturity, Change Management, Risk & Compliance.")

if "m2_result_cache" not in st.session_state:
    st.session_state["m2_result_cache"] = {}

cache = st.session_state["m2_result_cache"]

if problem_id not in cache:
    with st.spinner("AI is evaluating feasibility…"):
        result = call_m2_assessment(problem)
    if not result:
        st.error("Assessment failed. Please check your AI Settings (provider, model, API key) in the sidebar and try again.")
        st.stop()
    cache[problem_id] = result

    # Persist — same scoring/verdict/hard-gate logic as My Project's Module 2
    scores = result.get("scores", {})
    overall = result.get("overall", 0.0)
    verdict = result.get("verdict", "Conditional")

    strengths = "\n".join(f"- {s}" for s in result.get("strengths", []))
    risks = "\n".join(f"- {r}" for r in result.get("risks", []))
    recommendations = "\n".join(f"- {r}" for r in result.get("recommendations", []))
    dim_reasoning = result.get("dimension_reasoning", {})
    reasoning_md = "\n".join(
        f"**{dim['label']}** ({scores.get(dim['id'], 0):.1f}/5): {dim_reasoning.get(dim['id'], '')}"
        for dim in ASSESSMENT_DIMENSIONS
    )
    ai_report = (f"## Overall Assessment\n{result.get('overall_summary', '')}\n\n"
                 f"## Dimension Breakdown\n{reasoning_md}\n\n"
                 f"## Strengths\n{strengths}\n\n## Risks & Gaps\n{risks}\n\n"
                 f"## Recommendations\n{recommendations}")

    rec_id = f"FA-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    db_save_assessment({
        "id": rec_id, "problem_id": problem_id,
        "assessed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assessor_name": "AI Assessment",
        "ai_suitability_score": scores.get("ai_suitability", 0),
        "economic_viability_score": scores.get("economic_viability", 0),
        "data_readiness_score": scores.get("data_readiness", 0),
        "workflow_maturity_score": scores.get("workflow_maturity", 0),
        "change_management_score": scores.get("change_management", 0),
        "risk_compliance_score": scores.get("risk_compliance", 0),
        "hard_gate_triggered": 1 if result.get("hard_gate_triggered") else 0,
        "hard_gate_reason": result.get("hard_gate_reason", ""),
        "overall_score": overall, "verdict": verdict,
        "ai_recommendation": ai_report,
        "responses": str(scores),
    })
    new_status = {"Feasible": "Under Review", "Conditional": "Deferred",
                  "Not Feasible": "Rejected"}.get(verdict, "Under Review")
    db_update_status(problem_id, new_status)

result = cache[problem_id]
scores = result.get("scores", {})
dim_reasoning = result.get("dimension_reasoning", {})
overall = result.get("overall", 0.0)
verdict = result.get("verdict", "Conditional")
vc = VERDICT_CONFIG.get(verdict, VERDICT_CONFIG["Conditional"])
hard_gate = result.get("hard_gate_triggered")
hard_gate_reason = result.get("hard_gate_reason", "")

st.success("Assessment complete.")

# ── Dimension Scores ─────────────────────────────────────────────────────
st.markdown("### 📊 Dimension Scores")
for dim in ASSESSMENT_DIMENSIONS:
    s = scores.get(dim["id"], 0)
    pct = int(s / 5 * 100)
    col = get_completeness_color(pct)
    st.markdown(f"""
    <div class="card" style="padding:0.9rem 1.2rem;margin-bottom:0.6rem;min-height:0;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>{dim['icon']} <b>{dim['label']}</b> <span style="color:#888;font-size:0.75rem;">({dim['role']})</span></span>
        <span style="font-weight:700;color:{col};">{s:.1f}/5</span>
      </div>
      <div style="background:#eee;border-radius:8px;height:8px;margin-top:6px;">
        <div style="background:{col};width:{pct}%;height:8px;border-radius:8px;"></div>
      </div>
    </div>""", unsafe_allow_html=True)

# ── Reasoning ────────────────────────────────────────────────────────────
st.markdown("### 🧠 Reasoning")
if result.get("overall_summary"):
    st.markdown(f'<div class="review-box">{result["overall_summary"]}</div>', unsafe_allow_html=True)
st.write("")
for dim in ASSESSMENT_DIMENSIONS:
    rsn = dim_reasoning.get(dim["id"], "")
    if rsn:
        st.markdown(f"**{dim['icon']} {dim['label']}:** {rsn}")

# ── Verdict ──────────────────────────────────────────────────────────────
st.markdown("### ✅ Verdict")
if hard_gate:
    st.error(f"🚫 Hard Gate Triggered: {hard_gate_reason}")

st.markdown(f"""
<div style="background:{vc['bg']};border:1.5px solid {vc['color']};border-radius:14px;
            padding:1.2rem 1.6rem;margin-bottom:1rem;
            display:flex;justify-content:space-between;align-items:center;">
  <div>
    <div style="font-size:0.7rem;color:{vc['color']};font-weight:700;letter-spacing:0.08em;">OVERALL VERDICT</div>
    <div style="font-size:1.9rem;font-weight:800;color:{vc['color']};margin-top:2px;">
      {overall:.2f}<span style="font-size:1rem;opacity:0.6;"> / 5</span>
    </div>
  </div>
  <div style="font-size:1rem;font-weight:700;color:{vc['color']};">{vc['icon']} {verdict}</div>
</div>""", unsafe_allow_html=True)

# ── Recommendations ──────────────────────────────────────────────────────
st.markdown("### 💡 Recommendations")
rec_col, risk_col = st.columns(2)
with rec_col:
    if result.get("strengths"):
        st.markdown("**✅ Strengths**")
        for s in result["strengths"]:
            st.markdown(f"- {s}")
    if result.get("recommendations"):
        st.markdown("**💡 Recommendations**")
        for r in result["recommendations"]:
            st.markdown(f"- {r}")
with risk_col:
    if result.get("risks"):
        st.markdown("**⚠️ Risks & Gaps**")
        for r in result["risks"]:
            st.markdown(f"- {r}")

assessments = db_load_assessments(problem_id)
if assessments:
    latest = assessments[0]
    with st.expander("Full AI Report", expanded=False):
        st.markdown(latest.get("ai_recommendation", ""))

    df = pd.DataFrame([{
        "Assessment ID": latest["id"], "Problem ID": problem_id,
        "Assessed at": latest["assessed_at"], "Overall Score": latest["overall_score"],
        "Verdict": latest["verdict"],
        **{d["label"]: scores.get(d["id"]) for d in ASSESSMENT_DIMENSIONS},
    }])
    st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode(),
                        f"assessment_{latest['id']}.csv", "text/csv")

st.info("Proceed to **⚖️ Gain Pain Analysis** in the sidebar to continue.")
