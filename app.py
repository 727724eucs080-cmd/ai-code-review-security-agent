import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Code Review & Security Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "source_code" not in st.session_state:
    st.session_state.source_code = ""

if "detected_language" not in st.session_state:
    st.session_state.detected_language = ""

if "analysis_running" not in st.session_state:
    st.session_state.analysis_running = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================================
# PAGE DEFINITIONS
# ==========================================================

dashboard_page = st.Page(
    "pages/Dashboard.py",
    title="Dashboard",
    icon="📊",
    default=True
)

code_submission_page = st.Page(
    "pages/Code_Submission.py",
    title="Code Submission & Analysis",
    icon="🔍"
)

assistant_page = st.Page(
    "pages/Secure_Coding_Assistant.py",
    title="Coding Assistant",
    icon="💬"
)

reports_page = st.Page(
    "pages/Reports.py",
    title="Reports Generation",
    icon="📄"
)

about_page = st.Page(
    "pages/About.py",
    title="About",
    icon="ℹ️"
)


# ==========================================================
# NAVIGATION
# ==========================================================

pg = st.navigation(
    {
        "Application": [
            dashboard_page,
            code_submission_page,
            assistant_page,
            reports_page
        ],
        "Information": [
            about_page
        ]
    },
    position="sidebar",
    expanded=True
)


# ==========================================================
# RUN CURRENT PAGE
# ==========================================================

pg.run()