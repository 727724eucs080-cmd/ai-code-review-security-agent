import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.html(
    """
    <style>

    /* ======================================================
       HERO
       ====================================================== */

    .about-hero {
        padding: 30px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            rgba(79, 140, 255, 0.18),
            rgba(115, 87, 232, 0.12)
        );
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 28px;
    }

    .about-hero-icon {
        font-size: 40px;
        margin-bottom: 8px;
    }

    .about-hero-title {
        font-size: 34px;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .about-hero-subtitle {
        font-size: 15px;
        line-height: 1.7;
        color: #aeb5c7;
        max-width: 1000px;
    }


    /* ======================================================
       SECTION TITLE
       ====================================================== */

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 28px;
        margin-bottom: 18px;
    }


    /* ======================================================
       INFORMATION CARD
       ====================================================== */

    .info-card {
        min-height: 155px;
        padding: 22px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .info-icon {
        font-size: 28px;
        margin-bottom: 10px;
    }

    .info-title {
        font-size: 17px;
        font-weight: 650;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .info-text {
        font-size: 13px;
        line-height: 1.6;
        color: #9da4b6;
    }


    /* ======================================================
       TECHNOLOGY CARD
       ====================================================== */

    .tech-card {
        min-height: 165px;
        padding: 22px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .tech-title {
        color: #ffffff;
        font-size: 16px;
        font-weight: 650;
        margin-bottom: 13px;
    }

    .tech-item {
        color: #a5acbd;
        font-size: 13px;
        padding: 5px 0;
    }


    /* ======================================================
       MODULE
       ====================================================== */

    .module-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border-radius: 11px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .module-icon {
        font-size: 20px;
        width: 30px;
    }

    .module-name {
        color: #d9ddea;
        font-size: 14px;
        font-weight: 500;
    }


    /* ======================================================
       STANDARD
       ====================================================== */

    .standard-card {
        text-align: center;
        padding: 22px 15px;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .standard-icon {
        font-size: 30px;
        margin-bottom: 9px;
    }

    .standard-name {
        color: #ffffff;
        font-size: 13px;
        font-weight: 600;
        line-height: 1.5;
    }


    /* ======================================================
       WORKFLOW
       ====================================================== */

    .workflow-card {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 18px;
        margin-bottom: 10px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .workflow-number {
        min-width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(79, 140, 255, 0.15);
        color: #75a7ff;
        font-size: 12px;
        font-weight: 700;
    }

    .workflow-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
    }

    .workflow-description {
        color: #8e95a8;
        font-size: 12px;
        margin-top: 4px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .project-footer {
        margin-top: 30px;
        margin-bottom: 30px;
        padding: 25px;
        text-align: center;
        border-radius: 15px;
        background: linear-gradient(
            135deg,
            rgba(79, 140, 255, 0.10),
            rgba(115, 87, 232, 0.08)
        );
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .footer-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 650;
    }

    .footer-text {
        color: #858c9f;
        font-size: 12px;
        margin-top: 6px;
    }

    </style>
    """
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.html(
    """
    <div class="about-hero">

        <div class="about-hero-icon">
            🔍
        </div>

        <div class="about-hero-title">
            AI Code Review & Security Analysis Agent
        </div>

        <div class="about-hero-subtitle">
            An intelligent software quality assurance platform
            that combines Artificial Intelligence, Static Code
            Analysis, and Retrieval-Augmented Generation (RAG)
            to analyze source code and provide actionable
            security and code-quality guidance.
        </div>

    </div>
    """
)


# ==========================================================
# PROJECT OVERVIEW
# ==========================================================

st.html(
    """
    <div class="section-title">
        🎯 Project Overview
    </div>
    """
)

st.caption(
    "The platform automates important parts of the software "
    "code-review process and helps developers understand "
    "and resolve identified issues."
)


col1, col2, col3 = st.columns(3)


with col1:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🤖
            </div>

            <div class="info-title">
                AI-Powered Analysis
            </div>

            <div class="info-text">
                Uses Artificial Intelligence to analyze source
                code and identify code-quality issues and
                security vulnerabilities.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🛡️
            </div>

            <div class="info-title">
                Security Analysis
            </div>

            <div class="info-text">
                Detects security vulnerabilities using static
                analysis and security-focused AI analysis
                aligned with secure coding practices.
            </div>

        </div>
        """
    )


with col3:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                💡
            </div>

            <div class="info-title">
                Intelligent Guidance
            </div>

            <div class="info-text">
                Provides remediation recommendations and a
                conversational secure-coding assistant using
                retrieved knowledge.
            </div>

        </div>
        """
    )


# ==========================================================
# TECHNOLOGIES
# ==========================================================

st.html(
    """
    <div class="section-title">
        ⚙️ Technologies Used
    </div>
    """
)


col1, col2, col3 = st.columns(3)


with col1:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-title">
                🐍 Backend & Orchestration
            </div>

            <div class="tech-item">
                • Python
            </div>

            <div class="tech-item">
                • LangGraph
            </div>

            <div class="tech-item">
                • LangChain
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-title">
                🧠 AI & Knowledge
            </div>

            <div class="tech-item">
                • Gemini
            </div>

            <div class="tech-item">
                • FAISS
            </div>

            <div class="tech-item">
                • Retrieval-Augmented Generation
            </div>

        </div>
        """
    )


with col3:

    st.html(
        """
        <div class="tech-card">

            <div class="tech-title">
                🔎 Static Analysis
            </div>

            <div class="tech-item">
                • Pylint
            </div>

            <div class="tech-item">
                • Bandit
            </div>

            <div class="tech-item">
                • Syntax Validation
            </div>

        </div>
        """
    )


# ==========================================================
# FRONTEND
# ==========================================================

st.html(
    """
    <div class="section-title">
        🖥️ Frontend
    </div>
    """
)


col1, col2 = st.columns(2)


with col1:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🎨
            </div>

            <div class="info-title">
                Streamlit
            </div>

            <div class="info-text">
                Provides the interactive web interface for
                source-code submission, analysis results,
                dashboards, reports, and the coding assistant.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                📊
            </div>

            <div class="info-title">
                Interactive Visualization
            </div>

            <div class="info-text">
                Analysis scores, severity information,
                findings, remediation actions, and reports
                are presented through an interactive interface.
            </div>

        </div>
        """
    )


# ==========================================================
# AI MODEL
# ==========================================================

st.html(
    """
    <div class="section-title">
        🧠 AI Model
    </div>
    """
)


col1, col2 = st.columns(2)


with col1:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                ✨
            </div>

            <div class="info-title">
                Gemini
            </div>

            <div class="info-text">
                Used for AI-powered code analysis, security
                reasoning, remediation guidance, summaries,
                and conversational assistance.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🔗
            </div>

            <div class="info-title">
                RAG Integration
            </div>

            <div class="info-text">
                Retrieves relevant secure-coding knowledge
                to provide context-aware answers for developer
                questions.
            </div>

        </div>
        """
    )


# ==========================================================
# SYSTEM MODULES
# ==========================================================

st.html(
    """
    <div class="section-title">
        🧩 System Modules
    </div>
    """
)


modules = [
    ("✓", "Syntax Validation"),
    ("🔍", "Code Analysis Agent"),
    ("🛡️", "Security Analysis Agent"),
    ("🛠️", "Remediation Agent"),
    ("📝", "PR Summary Agent"),
    ("📄", "Report Generator"),
    ("💬", "Secure Coding Assistant"),
]


col1, col2 = st.columns(2)


for index, module in enumerate(modules):

    icon, name = module

    column = col1 if index % 2 == 0 else col2

    with column:

        st.html(
            f"""
            <div class="module-card">

                <div class="module-icon">
                    {icon}
                </div>

                <div class="module-name">
                    {name}
                </div>

            </div>
            """
        )


# ==========================================================
# SECURITY STANDARDS
# ==========================================================

st.html(
    """
    <div class="section-title">
        🛡️ Security Standards
    </div>
    """
)


standards = [
    ("🔐", "OWASP Top 10"),
    ("🐍", "Python Secure Coding Guidelines"),
    ("☕", "Java Secure Coding Guidelines"),
]


col1, col2, col3 = st.columns(3)


for column, standard in zip(
    [col1, col2, col3],
    standards
):

    icon, name = standard

    with column:

        st.html(
            f"""
            <div class="standard-card">

                <div class="standard-icon">
                    {icon}
                </div>

                <div class="standard-name">
                    {name}
                </div>

            </div>
            """
        )


# ==========================================================
# ANALYSIS WORKFLOW
# ==========================================================

st.html(
    """
    <div class="section-title">
        🔄 Analysis Workflow
    </div>
    """
)


workflow_steps = [

    (
        "01",
        "Submit Code",
        "Upload or paste Python or Java source code."
    ),

    (
        "02",
        "Validate",
        "Validate the source-code syntax before analysis."
    ),

    (
        "03",
        "Analyze",
        "Run code-quality and security analysis."
    ),

    (
        "04",
        "Remediate",
        "Generate actionable remediation recommendations."
    ),

    (
        "05",
        "Summarize",
        "Generate a Pull Request summary and final report."
    ),

    (
        "06",
        "Assist",
        "Answer developer questions using RAG and analysis context."
    ),

]


for number, title, description in workflow_steps:

    st.html(
        f"""
        <div class="workflow-card">

            <div class="workflow-number">
                {number}
            </div>

            <div>

                <div class="workflow-title">
                    {title}
                </div>

                <div class="workflow-description">
                    {description}
                </div>

            </div>

        </div>
        """
    )


# ==========================================================
# PROJECT FOOTER
# ==========================================================

st.html(
    """
    <div class="project-footer">

        <div class="footer-title">
            🎓 Academic Major Project
        </div>

        <div class="footer-text">
            AI Code Review & Security Analysis Agent
        </div>

        <div class="footer-text">
            Intelligent code quality, security analysis,
            remediation, reporting, and secure-coding assistance.
        </div>

    </div>
    """
)