# app.py — entry point. Run: streamlit run app.py
#
# MODULE 1 — Problem Definition. Taken completely from Friend's Project per
# the merge spec ("No changes required"): same landing page, same intake
# flow (free-text description -> AI extraction -> missing-field follow-up
# -> review & save). The only edits are mechanical: shared theme/sidebar
# instead of copy-pasted CSS, and database calls routed through
# database/problem_repository.py so this page and Module 4's Governance
# Review share one canonical database.

import streamlit as st

from llm.extractor import extract_problem
from llm.missing_fields import get_missing_fields
from llm.question_generator import QUESTION_MAP

from database.problem_repository import save_problem
from database.db import init_db, db_remove_duplicate_problems

from ui.theme import apply_theme
from ui.sidebar import render_sidebar

# ==========================
# PAGE CONFIGURATION
# ==========================

st.set_page_config(
    page_title="AI Governance Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
if not st.session_state.get("_dedup_done"):
    db_remove_duplicate_problems()
    st.session_state["_dedup_done"] = True

apply_theme()
render_sidebar("m1")

# ==========================
# PAGE TITLE
# ==========================

st.title("Problem Definition & Validation")

# ==========================
# PROCESS STEPPER
# ==========================

st.markdown("""
<div class="stepper">
<b>🟣 Describe Problem</b>
&nbsp;&nbsp;&nbsp;→&nbsp;&nbsp;&nbsp;
<b> Extract & Validate</b>
&nbsp;&nbsp;&nbsp;→&nbsp;&nbsp;&nbsp;
<b> Fill Missing Info</b>
&nbsp;&nbsp;&nbsp;→&nbsp;&nbsp;&nbsp;
<b> Review & Save</b>
</div>
""", unsafe_allow_html=True)

# ==========================
# TOP SECTION
# ==========================

left_col, right_col = st.columns([2, 1])

# ==========================
# PROBLEM INPUT
# ==========================

with left_col:
    with st.container(border=True):
        st.subheader("Describe Your Business Problem")
        st.caption("Provide a detailed description of the problem you want to solve.")

        problem_text = st.text_area(
            "Business problem description",
            height=220,
            placeholder="Describe the business problem...",
            label_visibility="collapsed"
        )

        analyze_clicked = st.button("Analyze with AI")

        if analyze_clicked:
            if not problem_text.strip():
                st.warning("Please enter a business problem.")
                st.stop()

            with st.spinner("Analyzing problem..."):
                try:
                    extracted_data = extract_problem(
                        problem_text,
                        st.session_state.get("llm_provider")
                    )
                    st.session_state["problem_data"] = extracted_data
                    st.session_state["missing_fields"] = get_missing_fields(extracted_data)
                except Exception as e:
                    st.error(f"Extraction Error: {e}")

# ==========================
# EXTRACTED INFORMATION
# ==========================

with right_col:
    with st.container(border=True):
        st.subheader("Extracted Information")

        if "problem_data" in st.session_state:
            data = st.session_state["problem_data"]

            st.markdown("**Problem Statement**")
            st.write(data.get("problem_statement") or "-")

            st.markdown("**Business Objective**")
            st.write(data.get("business_objective") or "-")

            st.markdown("**Proposed Solution**")
            st.write(data.get("proposed_solution") or "-")
        else:
            st.info("Analyze a problem to see extracted information.")

# ==========================
# MISSING INFORMATION
# ==========================

if "problem_data" in st.session_state:
    missing_fields = st.session_state["missing_fields"]

    if missing_fields:
        st.write("")
        st.write("")

        with st.container(border=True):
            st.subheader("Missing Information")
            st.caption("Please provide the remaining information required for governance review.")

            answers = {}
            col1, col2, col3 = st.columns(3)
            columns = [col1, col2, col3]

            for index, field in enumerate(missing_fields):
                if field in QUESTION_MAP:
                    with columns[index % 3]:
                        answers[field] = st.text_input(QUESTION_MAP[field], key=f"input_{field}")

            st.write("")

            if st.button("Update Information"):
                empty_fields = []
                for field, answer in answers.items():
                    if not answer.strip():
                        empty_fields.append(field)

                if empty_fields:
                    st.error("All missing fields must be completed.")
                    st.stop()

                for field, answer in answers.items():
                    st.session_state["problem_data"][field] = answer

                st.session_state["missing_fields"] = get_missing_fields(st.session_state["problem_data"])
                st.success("Information updated.")
                st.rerun()

# ==========================
# REVIEW & SAVE
# ==========================

if "problem_data" in st.session_state and not st.session_state["missing_fields"]:
    data = st.session_state["problem_data"]

    st.write("")
    st.write("")
    st.success("All required information has been captured.")
    st.subheader("Review & Save")
    st.markdown("---")

    review_left, review_right = st.columns(2)

    sensitivity_options = ["Public", "Internal", "Confidential", "Personal Data (PII)"]

    with review_left:
        with st.container(border=True):
            st.markdown("### 📋 Business Problem Summary")

            data["problem_statement"] = st.text_area(
                "Problem Statement", value=data.get("problem_statement", ""), height=120)
            data["business_objective"] = st.text_area(
                "Business Objective", value=data.get("business_objective", ""), height=120)
            data["proposed_solution"] = st.text_area(
                "Proposed Solution", value=data.get("proposed_solution", ""), height=120)
            data["business_value"] = st.text_area(
                "Business Value", value=data.get("business_value", ""), height=120)

    with review_right:
        with st.container(border=True):
            st.markdown("### ⚙️ Implementation Details")

            data["timeline"] = st.text_input("Timeline", value=data.get("timeline", ""))
            data["owner"] = st.text_input("Owner", value=data.get("owner", ""))
            data["workflow_location"] = st.text_input(
                "Workflow Location", value=data.get("workflow_location", ""))
            data["decision_support"] = st.text_area(
                "Decision Support", value=data.get("decision_support", ""), height=100)
            data["stakeholders"] = st.text_area(
                "Stakeholders", value=data.get("stakeholders", ""), height=80)
            data["why_ai"] = st.text_area(
                "Why AI?", value=data.get("why_ai", ""), height=100)

            data["data_sensitivity"] = st.selectbox(
                "Data Sensitivity",
                sensitivity_options,
                index=(sensitivity_options.index(data.get("data_sensitivity", "Internal"))
                       if data.get("data_sensitivity", "Internal") in sensitivity_options else 1),
                key="review_data_sensitivity"
            )

    st.write("")
    st.write("")

    save_col1, save_col2, save_col3 = st.columns([5, 1, 1])

    with save_col3:
        if "save_feedback" not in st.session_state:
            st.session_state.save_feedback = None

        if st.button("💾 Save Problem", use_container_width=True):
            for field, value in data.items():
                if isinstance(value, str):
                    data[field] = value.strip()

            missing = get_missing_fields(data)
            if missing:
                st.session_state.save_feedback = (
                    "error", f"Cannot save. Missing fields: {', '.join(missing)}")
                st.rerun()

            try:
                save_problem(data)
                st.session_state.save_feedback = ("success", "Problem saved successfully.")
            except Exception as e:
                st.session_state.save_feedback = ("error", f"Could not save problem: {e}")

            st.rerun()

        if st.session_state.save_feedback:
            feedback_type, feedback_message = st.session_state.save_feedback
            if feedback_type == "success":
                st.success(feedback_message)
            else:
                st.error(feedback_message)
