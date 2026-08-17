import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Code Review & Security Analysis Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CUSTOM UI STYLING
# ==========================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    html,
    body,
    [class*="css"] {

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;

    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        width: 310px !important;
        min-width: 310px !important;

        background:
            linear-gradient(
                180deg,
                #171923 0%,
                #1c1e29 50%,
                #15161e 100%
            );

        border-right:
            1px solid
            rgba(255, 255, 255, 0.08);

    }


    [data-testid="stSidebar"] > div:first-child {

        padding-top: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        padding-bottom: 1rem;

    }


    /* ======================================================
       STREAMLIT NAVIGATION
       ====================================================== */

    [data-testid="stSidebarNav"] {

        padding-top: 5px;
        padding-bottom: 5px;

    }


    [data-testid="stSidebarNav"] ul {

        padding-top: 0;
        padding-bottom: 0;

    }


    [data-testid="stSidebarNav"] li {

        margin-bottom: 6px;

    }


    /* ======================================================
       NAVIGATION LINKS
       ====================================================== */

    [data-testid="stSidebarNav"] a {

        min-height: 50px !important;

        border-radius: 11px;

        padding:
            11px
            14px !important;

        margin:
            4px
            0;

        transition:
            background 0.18s ease,
            transform 0.18s ease,
            box-shadow 0.18s ease;

        text-decoration: none;

    }


    /* ======================================================
       NAVIGATION TEXT
       ====================================================== */

    [data-testid="stSidebarNav"] a span {

        font-size: 16px !important;

        font-weight: 600 !important;

        color: #c7cbd7 !important;

    }


    /* Streamlit internal navigation text */

    [data-testid="stSidebarNav"] a p {

        font-size: 16px !important;

        font-weight: 600 !important;

        color: #c7cbd7 !important;

        line-height: 1.4 !important;

    }


    /* ======================================================
       NAVIGATION HOVER
       ====================================================== */

    [data-testid="stSidebarNav"] a:hover {

        background:
            rgba(255, 255, 255, 0.07);

        transform:
            translateX(3px);

    }


    [data-testid="stSidebarNav"] a:hover span {

        color: #ffffff !important;

    }


    [data-testid="stSidebarNav"] a:hover p {

        color: #ffffff !important;

    }


    /* ======================================================
       ACTIVE PAGE
       ====================================================== */

    [data-testid="stSidebarNav"]
    a[aria-current="page"] {

        background:
            linear-gradient(
                90deg,
                rgba(79, 140, 255, 0.27),
                rgba(115, 87, 232, 0.18)
            );

        border-left:
            3px solid
            #5d91ff;

        box-shadow:
            0 5px 15px
            rgba(0, 0, 0, 0.18);

    }


    [data-testid="stSidebarNav"]
    a[aria-current="page"] span {

        color: #ffffff !important;

        font-weight: 700 !important;

    }


    [data-testid="stSidebarNav"]
    a[aria-current="page"] p {

        color: #ffffff !important;

        font-weight: 700 !important;

    }


    /* ======================================================
       NAVIGATION SECTION HEADINGS
       ====================================================== */

    [data-testid="stSidebarNav"]
    [data-testid="stMarkdownContainer"] {

        padding-left: 5px;

    }


    [data-testid="stSidebarNav"]
    [data-testid="stMarkdownContainer"] p {

        color: #8d96ad !important;

        font-size: 11px !important;

        font-weight: 700 !important;

        letter-spacing: 1.2px;

        text-transform: uppercase;

        margin-top: 18px;

        margin-bottom: 9px;

    }


    /* ======================================================
       SIDEBAR DIVIDER
       ====================================================== */

    [data-testid="stSidebar"] hr {

        border:
            none;

        border-top:
            1px solid
            rgba(255, 255, 255, 0.07);

        margin:
            15px
            5px;

    }


    /* ======================================================
       SIDEBAR BRAND
       ====================================================== */

    [data-testid="stSidebar"] .sidebar-title {

        font-size: 19px !important;

        font-weight: 700;

        color: #ffffff;

        margin-bottom: 3px;

    }


    [data-testid="stSidebar"] .sidebar-subtitle {

        font-size: 13px !important;

        color: #9298aa;

        margin-bottom: 15px;

    }


    /* ======================================================
       SIDEBAR STATUS
       ====================================================== */

    [data-testid="stSidebar"] .sidebar-status {

        font-size: 14px !important;

        font-weight: 600;

        color: #d7dbe6;

        margin-bottom: 4px;

    }


    [data-testid="stSidebar"] .sidebar-description {

        font-size: 12px !important;

        line-height: 1.45;

        color: #777f93;

        margin-bottom: 5px;

    }


    [data-testid="stSidebar"] .sidebar-version {

        font-size: 11px !important;

        color: #62697a;

    }


    /* ======================================================
       SIDEBAR MARKDOWN TEXT
       ====================================================== */

    [data-testid="stSidebar"] .stMarkdown p {

        font-size: 14px;

    }


    [data-testid="stSidebar"] .stCaptionContainer p {

        font-size: 13px !important;

    }


    /* ======================================================
       MAIN CONTENT
       ====================================================== */

    .main .block-container {

        padding-top: 2rem;

        padding-left: 2.5rem;

        padding-right: 2.5rem;

        padding-bottom: 3rem;

    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1 {

        font-weight: 700 !important;

    }


    h2,
    h3 {

        font-weight: 650 !important;

    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        border-radius: 9px;

        transition:
            all 0.18s ease;

    }


    .stButton > button:hover {

        transform:
            translateY(-1px);

    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    [data-testid="stMetric"] {

        border-radius: 12px;

        padding:
            14px
            16px;

        background:
            rgba(255, 255, 255, 0.025);

        border:
            1px solid
            rgba(255, 255, 255, 0.07);

    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    [data-testid="stExpander"] {

        border-radius: 10px;

        border:
            1px solid
            rgba(255, 255, 255, 0.08);

    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR BRAND
# ==========================================================

with st.sidebar:

    st.markdown(
        "🔍 **AI Code Review**"
    )

    st.caption(
        "Security Analysis Agent"
    )


# ==========================================================
# PAGE NAVIGATION
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


coding_assistant_page = st.Page(
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
# NAVIGATION GROUPS
# ==========================================================

pages = {

    "Application": [

        dashboard_page,

        code_submission_page,

        coding_assistant_page,

        reports_page

    ],

    "Information": [

        about_page

    ]

}


# ==========================================================
# CREATE NAVIGATION
# ==========================================================

pg = st.navigation(
    pages
)


# ==========================================================
# SIDEBAR FOOTER
# ==========================================================

with st.sidebar:

    st.divider()

    st.markdown(
        "🟢 **AI Analysis Engine Ready**"
    )

    st.caption(
        "Automated code quality, security "
        "analysis and intelligent remediation."
    )

    st.caption(
        "AI Code Review Agent • v1.0"
    )


# ==========================================================
# RUN SELECTED PAGE
# ==========================================================

pg.run()