# pages/0_Instructions.py
# ─────────────────────────────────────────────────────────────────────────
# User guide for the unified AI Governance Platform. Same shared theme and
# sidebar as every other page (ui/theme.apply_theme, ui/sidebar.render_sidebar)
# — no new CSS, nothing page-specific. Content is rewritten to describe this
# app's actual modules (Problem Definition -> Feasibility Assessment ->
# Gain-Pain Analysis -> Expert Advice -> Governance Review -> Analytics
# Dashboard) instead of the generic placeholder copy.
# ─────────────────────────────────────────────────────────────────────────

import streamlit as st

from ui.theme import apply_theme
from ui.sidebar import render_sidebar

st.set_page_config(
    page_title="AI Governance Platform - Instructions",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
render_sidebar("m0")

# ==========================
# TITLE
# ==========================

st.title("📘 AI Governance Platform User Guide")

st.info(
    """
    This platform helps organizations identify, evaluate, prioritize, and
    govern AI opportunities through a structured, end-to-end workflow —
    from initial idea capture through expert review and final governance
    sign-off.
    """
)

# ==========================
# OVERVIEW
# ==========================

st.subheader("Platform Workflow")

st.markdown("""
1. Problem Definition

2. Feasibility Assessment

3. Gain–Pain Analysis

4. Expert Advice *(optional — only if the analysis needs a second look)*

5. Governance Review

6. Analytics Dashboard
""")

st.divider()

# ==========================
# MODULE 1 — Problem Definition
# ==========================

st.subheader("📄 Problem Definition")

st.markdown("""
The Idea Submitter describes a business problem in their own words, and
the AI assistant extracts the structured information needed for
governance review.

**How it works:**

* Describe the business problem in free text and click **Analyze with AI**.
* The AI extracts the problem statement, business objective, proposed
  solution, and business value automatically.
* Any required field the AI couldn't confidently fill in is flagged under
  **Missing Information**, with a short follow-up question for each one.

**Required Information:**

* Problem Statement
* Business Objective
* Proposed Solution
* Timeline
* Owner
* Workflow Location
* Decision Support Requirement
* Business Value
* Stakeholders
* Why AI?
* Data Sensitivity

If the Idea Submitter isn't satisfied with what the AI inferred, every
field can be edited directly in the **Review & Save** step before saving.

Once all required information is complete, save the opportunity — it then
becomes available to the Business Team in Feasibility Assessment.
""")

st.divider()

# ==========================
# MODULE 2 — Feasibility Assessment
# ==========================

st.subheader("📊 Feasibility Assessment")

st.markdown("""
Business teams evaluate whether a submitted opportunity is actually
suitable for an AI-based solution.

**Assessment Dimensions:**

* AI Suitability
* Economic Viability
* Data Readiness
* Workflow Maturity
* Change Management
* Risk & Compliance

**Outputs:**

* A 1–5 score for each dimension, with AI-generated reasoning
* An Overall Score and Verdict — **Feasible**, **Conditional**, or
  **Not Feasible**
* Strengths, risks/gaps, and recommendations
* A hard-gate flag if a critical risk makes the opportunity unsuitable
  regardless of its other scores

Everything appears on one scrollable page — select the problem, and the
assessment runs and displays automatically with no extra steps.
""")

st.divider()

# ==========================
# MODULE 3 — Gain-Pain Analysis
# ==========================

st.subheader("⚖️ Gain-Pain Analysis")

st.markdown("""
Once a problem has been assessed as feasible, this module weighs its
benefits against its costs and risks to produce a single priority score.

**Potential Gains:**

* Business Value Gain
* Strategic Alignment
* Efficiency Gain
* Innovation Potential

**Potential Pains:**

* Implementation Cost
* Operational Risk
* Adoption Resistance
* Compliance Burden

**Before running the analysis**, choose:

* **Ask Clarifying Questions** — the AI generates targeted questions for
  specific teams (Technical, Finance, Marketing, Legal, HR) to firm up
  the score before it's calculated, or
* **Run Gain-Pain Analysis Directly** — skip straight to scoring using
  only the information already captured.

**Outputs:**

* Gain Score, Pain Score, and an overall Priority Score (0–10)
* A Priority Band — **High**, **Medium**, or **Low**
* Quick wins and pain-mitigation suggestions

After the analysis completes, you're asked **"Satisfied with Analysis?"**
— choose **Yes** to finalize it, or **Request Expert Review** if you'd
like a domain expert to double-check or adjust any of the scores.
""")

st.divider()

# ==========================
# MODULE 4 — Expert Advice
# ==========================

st.subheader("🧑‍⚖️ Expert Advice")

st.markdown("""
This module only comes into play when someone requests a second opinion
on a Gain-Pain Analysis.

**For the person requesting review:**

* Submit a query, concern, or suggestion — e.g. *"I believe implementation
  cost should be lower"* or *"I disagree with the operational risk score."*

**For the expert reviewer:**

* See the problem statement, all current Gain and Pain values, the
  Priority Score, and the requester's query side by side.
* Adjust any of the 8 Gain-Pain dimensions directly.
* On **Save**, the Priority Score is recomputed automatically, and the
  update flows through to the Governance Review and Analytics Dashboard.

Every change is logged with the old value, new value, timestamp, expert
name, and reason — a complete audit trail.
""")

st.divider()

# ==========================
# MODULE 5 — Governance Review
# ==========================

st.subheader("🏛️ Governance Review")

st.markdown("""
The Governance Board makes the final call on each opportunity, with full
visibility into everything that came before.

**Reviewed on this page:**

* Problem Summary
* Feasibility Assessment results
* Gain-Pain Analysis results

**Decision Options:**

* Approved
* Rejected
* Pending Review
* Needs More Information

Every decision is saved with the reviewer's name and comments, and a
running history of recent decisions is shown for each opportunity.
""")

st.divider()

# ==========================
# MODULE 6 — Analytics Dashboard
# ==========================

st.subheader("📊 Analytics Dashboard")

st.markdown("""
Gives the Governance Board portfolio-level visibility across every AI
opportunity that has been submitted.

**Dashboard Features:**

* Total AI opportunities, by status
* Priority distribution (High / Medium / Low)
* Governance decision summary
* Compliance checklist (ISO 42001) and risk register (NIST AI RMF) views
* Drill-down into any individual opportunity
""")

st.divider()

# ==========================
# RECOMMENDED PROCESS
# ==========================

st.subheader("✅ Recommended Workflow")

st.markdown("""
1. Submit a new AI opportunity in **Problem Definition**.

2. Complete its **Feasibility Assessment**.

3. Run its **Gain-Pain Analysis** — ask clarifying questions first if the
   picture isn't clear yet.

4. If needed, send it to **Expert Advice** for a second opinion.

5. Bring it to the **Governance Review** board for a final decision.

6. Track everything over time on the **Analytics Dashboard**.
""")

st.success("You are now ready to use the AI Governance Platform.")
