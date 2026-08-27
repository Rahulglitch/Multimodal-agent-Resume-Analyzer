# utils/session_utils.py

import streamlit as st


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

def initialize_session_state():

    defaults = {

        "resume_bytes": None,
        "resume_filename": None,
        "resume_valid": False,

        "resume_text": None,
        "resume_skills": None,

        "resume_analysis": None,
        "review_result": None,
        "training_plan": None,

        "analysis_failed": False,
        "analysis_completed": False,

        "last_error": None,
        "retry_count": 0,

        "job_description": "",
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ============================================================
# CLEAR ANALYSIS
# ============================================================

def clear_analysis():

    st.session_state.resume_text = None
    st.session_state.resume_skills = None

    st.session_state.resume_analysis = None
    st.session_state.review_result = None
    st.session_state.training_plan = None

    st.session_state.analysis_failed = False
    st.session_state.analysis_completed = False

    st.session_state.last_error = None
    st.session_state.retry_count = 0


# ============================================================
# CLEAR EVERYTHING
# ============================================================

def clear_resume():

    st.session_state.resume_bytes = None
    st.session_state.resume_filename = None

    st.session_state.resume_text = None
    st.session_state.resume_skills = None

    st.session_state.resume_analysis = None
    st.session_state.review_result = None
    st.session_state.training_plan = None

    st.session_state.resume_valid = False

    st.session_state.analysis_failed = False
    st.session_state.analysis_completed = False

    st.session_state.last_error = None
    st.session_state.retry_count = 0
