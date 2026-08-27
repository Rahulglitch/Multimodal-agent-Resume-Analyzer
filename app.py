import truststore

truststore.inject_into_ssl()


# ============================================================
# STREAMLIT
# ============================================================

import streamlit as st


# ============================================================
# ENVIRONMENT
# ============================================================

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# UTILITY IMPORTS
# ============================================================

from utils.session_utils import (
    initialize_session_state,
    clear_analysis,
    clear_resume,
)

from utils.resume_validator import (
    validate_resume,
)

from utils.retry_handler import (
    run_ai_with_retry,
)

from utils.pdf_parser import (
    extract_pdf_text,
)

from utils.doc_parser import (
    extract_docx_text,
)

from utils.skill_extractor import (
    extract_skills,
)


# ============================================================
# AGENT IMPORTS
# ============================================================

from agents.analyzer_agent import (
    analyzer_resume,
)

from agents.reviewer_agent import (
    review_resume,
)

from agents.training_agent import (
    create_training_plan,
)


# ============================================================
# SESSION STATE
# ============================================================

initialize_session_state()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 AI Resume Analyzer"
)

st.caption(
    "Multi-Agent AI system for resume analysis, "
    "job matching and personalized skill development."
)

st.divider()


# ============================================================
# PIPELINE
# ============================================================

st.subheader(
    "🔄 AI Analysis Pipeline"
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.info(
        "📄\n\n**Resume Parser**"
    )


with col2:

    st.info(
        "🔧\n\n**Skill Extractor**"
    )


with col3:

    st.info(
        "🔍\n\n**Analyzer Agent**"
    )


with col4:

    st.info(
        "🧐\n\n**Reviewer Agent**"
    )


with col5:

    st.info(
        "🎓\n\n**Training Agent**"
    )


st.divider()


# ============================================================
# INPUT
# ============================================================

st.subheader(
    "📥 Resume Analysis Input"
)

resume_col, job_col = st.columns(2)


# ============================================================
# RESUME
# ============================================================

with resume_col:

    st.markdown(
        "### 📄 Upload Resume"
    )

    resume_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        max_upload_size=10,
        help=(
            "Upload your resume in PDF or DOCX format. "
            "Maximum file size is 10 MB."
        )
    )


    # ========================================================
    # NEW UPLOAD
    # ========================================================

    if resume_file is not None:

        current_file_bytes = (
            resume_file.getvalue()
        )


        is_new_file = (
            st.session_state.resume_bytes
            != current_file_bytes
        )


        if is_new_file:

            # ------------------------------------------------
            # Clear previous analysis
            # ------------------------------------------------

            clear_analysis()


            # ------------------------------------------------
            # Validate
            # ------------------------------------------------

            is_valid, message = (
                validate_resume(
                    resume_file
                )
            )


            if not is_valid:

                st.session_state.resume_valid = False

                st.error(
                    f"❌ {message}"
                )

                st.warning(
                    "Please upload another resume."
                )


            else:

                # ------------------------------------------------
                # Store resume
                # ------------------------------------------------

                st.session_state.resume_bytes = (
                    current_file_bytes
                )

                st.session_state.resume_filename = (
                    resume_file.name
                )

                st.session_state.resume_valid = True

                st.success(
                    "✅ Resume uploaded and validated."
                )

                st.caption(
                    f"📄 {resume_file.name}"
                )


        else:

            if st.session_state.resume_valid:

                st.success(
                    "✅ Resume ready for analysis."
                )

                st.caption(
                    f"📄 "
                    f"{st.session_state.resume_filename}"
                )


    # ========================================================
    # EXISTING RESUME
    # ========================================================

    elif (
        st.session_state.resume_valid
        and st.session_state.resume_filename
    ):

        st.success(
            "✅ Resume stored and ready."
        )

        st.caption(
            f"📄 "
            f"{st.session_state.resume_filename}"
        )


    # ========================================================
    # REMOVE
    # ========================================================

    if st.session_state.resume_valid:

        if st.button(
            "🗑️ Remove Resume",
            key="remove_resume",
            use_container_width=True
        ):

            clear_resume()

            st.rerun()


# ============================================================
# JOB DESCRIPTION
# ============================================================

with job_col:

    st.markdown(
        "### 💼 Job Description"
    )

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Paste the target job description here..."
        ),
        value=st.session_state.job_description
    )

    st.session_state.job_description = (
        job_description
    )


st.divider()


# ============================================================
# ANALYZE
# ============================================================

analyze_clicked = st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# RETRY
# ============================================================

retry_clicked = False


if st.session_state.analysis_failed:

    st.warning(
        """
        ⚠️ The previous AI analysis failed.

        Your resume is still stored and validated.
        You can retry without uploading it again.
        """
    )

    retry_clicked = st.button(
        "🔄 Try Analysis Again",
        key="top_retry",
        type="secondary",
        use_container_width=True
    )


# ============================================================
# START ANALYSIS
# ============================================================

if analyze_clicked or retry_clicked:


    # ========================================================
    # VALIDATE RESUME
    # ========================================================

    if not st.session_state.resume_valid:

        st.error(
            "📄 Please upload a valid resume first."
        )

        st.stop()


    # ========================================================
    # VALIDATE JD
    # ========================================================

    if not st.session_state.job_description.strip():

        st.error(
            "💼 Please enter a job description."
        )

        st.stop()


    # ========================================================
    # RESET STATUS
    # ========================================================

    st.session_state.analysis_failed = False

    st.session_state.analysis_completed = False

    st.session_state.last_error = None


    # ========================================================
    # PIPELINE
    # ========================================================

    try:

        with st.status(
            "🤖 AI Agents are working...",
            expanded=True
        ) as status:


            # ==================================================
            # 1. RESUME PARSER
            # ==================================================

            st.write(
                "📄 **Resume Parser**"
            )

            file_bytes = (
                st.session_state.resume_bytes
            )

            filename = (
                st.session_state.resume_filename.lower()
            )


            if filename.endswith(".pdf"):

                st.write(
                    "Reading PDF resume..."
                )

                resume_text = (
                    extract_pdf_text(
                        file_bytes
                    )
                )

            else:

                st.write(
                    "Reading DOCX resume..."
                )

                resume_text = (
                    extract_docx_text(
                        file_bytes
                    )
                )


            if not resume_text.strip():

                raise ValueError(
                    "No readable text was extracted."
                )


            st.session_state.resume_text = (
                resume_text
            )


            # ==================================================
            # 2. SKILLS
            # ==================================================

            st.write(
                "🔧 **Skill Extractor**"
            )

            resume_skills = (
                extract_skills(
                    resume_text
                )
            )

            st.session_state.resume_skills = (
                resume_skills
            )


            # ==================================================
            # 3. ANALYZER
            # ==================================================

            st.write(
                "🔍 **Analyzer Agent**"
            )

            resume_analysis = (
                run_ai_with_retry(

                    function=lambda:
                    analyzer_resume(
                        resume_text,
                        resume_skills
                    ),

                    max_retries=3
                )
            )


            st.session_state.resume_analysis = (
                resume_analysis
            )


            # ==================================================
            # 4. REVIEWER
            # ==================================================

            st.write(
                "🧐 **Reviewer Agent**"
            )

            review_result = (
                run_ai_with_retry(

                    function=lambda:
                    review_resume(
                        resume_analysis,
                        resume_skills,
                        st.session_state.job_description
                    ),

                    max_retries=3
                )
            )


            st.session_state.review_result = (
                review_result
            )


            # ==================================================
            # 5. TRAINING
            # ==================================================

            st.write(
                "🎓 **Training Agent**"
            )

            training_plan = (
                run_ai_with_retry(

                    function=lambda:
                    create_training_plan(
                        review_result
                    ),

                    max_retries=3
                )
            )


            st.session_state.training_plan = (
                training_plan
            )


            # ==================================================
            # COMPLETE
            # ==================================================

            st.session_state.analysis_failed = False

            st.session_state.analysis_completed = True

            st.session_state.retry_count = 0


            status.update(
                label="✅ Analysis Completed",
                state="complete"
            )


    # ========================================================
    # ERROR
    # ========================================================

    except Exception as error:

        st.session_state.analysis_failed = True

        st.session_state.analysis_completed = False

        st.session_state.last_error = str(
            error
        )


        st.error(
            "⚠️ AI Analysis Failed"
        )


        st.info(
            """
            Your resume is still stored.

            You can click **Try Analysis Again**
            without uploading the resume again.
            """
        )


        # ----------------------------------------------------
        # DEBUGGING
        # ----------------------------------------------------

        with st.expander(
            "🔧 Technical error details",
            expanded=True
        ):

            st.code(
                repr(error)
            )


# ============================================================
# RETRY SECTION
# ============================================================

if st.session_state.analysis_failed:

    st.divider()

    st.subheader(
        "🔄 Retry Analysis"
    )

    st.warning(
        "Your resume is still stored and validated."
    )


    if st.button(
        "🔄 Try Analysis Again",
        key="bottom_retry",
        type="primary",
        use_container_width=True
    ):

        st.session_state.analysis_failed = False

        st.rerun()


# ============================================================
# RESULTS
# ============================================================

if (
    st.session_state.analysis_completed
    and st.session_state.resume_analysis is not None
    and st.session_state.review_result is not None
    and st.session_state.training_plan is not None
):

    st.divider()

    st.header(
        "📊 Resume Analysis Report"
    )

    st.success(
        "Your resume has been successfully analyzed."
    )


    # ========================================================
    # SKILLS
    # ========================================================

    st.subheader(
        "🔧 Detected Resume Skills"
    )

    resume_skills = (
        st.session_state.resume_skills or []
    )


    if resume_skills:

        number_of_columns = min(
            len(resume_skills),
            4
        )

        skill_cols = st.columns(
            number_of_columns
        )


        for i, skill in enumerate(
            resume_skills
        ):

            with skill_cols[
                i % number_of_columns
            ]:

                st.success(
                    f"✓ {skill}"
                )

    else:

        st.warning(
            "No skills were detected."
        )


    st.divider()


    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🔍 Analyzer",
            "🧐 Reviewer",
            "🎓 Training Plan"
        ]
    )


    # ========================================================
    # ANALYZER
    # ========================================================

    with tab1:

        st.subheader(
            "🔍 Analyzer Agent Result"
        )

        st.write(
            st.session_state.resume_analysis
        )


    # ========================================================
    # REVIEWER
    # ========================================================

    with tab2:

        st.subheader(
            "🧐 Reviewer Agent Result"
        )

        st.write(
            st.session_state.review_result
        )


    # ========================================================
    # TRAINING
    # ========================================================

    with tab3:

        st.subheader(
            "🎓 Personalized Training Plan"
        )

        st.write(
            st.session_state.training_plan
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.divider()

    st.subheader(
        "📌 Analysis Summary"
    )

    summary1, summary2, summary3 = st.columns(3)


    with summary1:

        st.metric(
            "Skills Detected",
            len(resume_skills)
        )


    with summary2:

        st.metric(
            "AI Agents",
            "3"
        )


    with summary3:

        st.metric(
            "Status",
            "Completed"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Resume Analyzer • "
    "Powered by Multi-Agent AI"
)
