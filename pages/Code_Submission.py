import streamlit as st

from graph.workflow import workflow
from validators.syntax_validator import SyntaxValidator


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Code Submission & Analysis",
    page_icon="🔍",
    layout="wide"
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

if "syntax_result" not in st.session_state:
    st.session_state.syntax_result = None


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🔍 Code Submission & Analysis")

st.write(
    "Upload or paste your source code. "
    "The programming language will be detected automatically."
)


# ==========================================================
# INPUT SECTION
# ==========================================================

st.subheader("📥 Submit Source Code")

uploaded_file = st.file_uploader(
    "Upload Source Code",
    type=["py", "java"],
    help="Supported files: Python (.py) and Java (.java)"
)


# ==========================================================
# READ UPLOADED FILE
# ==========================================================

code = ""

if uploaded_file is not None:

    try:

        code = uploaded_file.getvalue().decode(
            "utf-8"
        )

        st.session_state.source_code = code

    except UnicodeDecodeError:

        st.error(
            "❌ Unable to read the uploaded file. "
            "Please upload a UTF-8 source file."
        )

        st.stop()


# ==========================================================
# PASTE CODE
# ==========================================================

if uploaded_file is None:

    code = st.text_area(
        "Or Paste Source Code",
        value=st.session_state.source_code,
        height=350,
        placeholder=(
            "Paste your Python or Java source code here..."
        )
    )

    st.session_state.source_code = code


# ==========================================================
# CHECK EMPTY CODE
# ==========================================================

if not code.strip():

    st.info(
        "👆 Upload a Python/Java file or paste source code "
        "to begin the analysis."
    )

    st.stop()


# ==========================================================
# AUTOMATIC LANGUAGE DETECTION
# ==========================================================

def detect_language(source_code, filename=None):

    """
    Detect Python or Java automatically.

    File extension is used when available.
    Source-code patterns are used as fallback.
    """

    # ------------------------------------------------------
    # File extension detection
    # ------------------------------------------------------

    if filename:

        filename_lower = filename.lower()

        if filename_lower.endswith(".py"):
            return "python"

        if filename_lower.endswith(".java"):
            return "java"

    # ------------------------------------------------------
    # Python syntax detection
    # ------------------------------------------------------

    try:

        SyntaxValidator.validate_python(
            source_code
        )

        import ast

        ast.parse(source_code)

        return "python"

    except Exception:
        pass

    # ------------------------------------------------------
    # Java pattern detection
    # ------------------------------------------------------

    java_patterns = [
        "public class ",
        "private class ",
        "protected class ",
        "class ",
        "public static void main",
        "System.out.println",
        "import java.",
        "package "
    ]

    for pattern in java_patterns:

        if pattern in source_code:

            return "java"

    return None


# ==========================================================
# DETECT LANGUAGE
# ==========================================================

filename = None

if uploaded_file is not None:
    filename = uploaded_file.name


detected_language = detect_language(
    code,
    filename
)


# ==========================================================
# LANGUAGE RESULT
# ==========================================================

if detected_language is None:

    st.error(
        "❌ Unable to confidently detect the programming "
        "language. Please provide valid Python or Java code."
    )

    st.stop()


st.session_state.detected_language = (
    detected_language.upper()
)


st.success(
    f"🟢 Detected Programming Language: "
    f"{detected_language.upper()}"
)


# ==========================================================
# SOURCE CODE PREVIEW
# ==========================================================

with st.expander(
    "📄 View Submitted Source Code",
    expanded=False
):

    st.code(
        code,
        language=detected_language
    )


# ==========================================================
# ANALYZE BUTTON
# ==========================================================

analyze_button = st.button(
    "🚀 Analyze Code",
    use_container_width=True,
    type="primary"
)


# ==========================================================
# ANALYSIS
# ==========================================================

if analyze_button:

    # ------------------------------------------------------
    # Clear previous result
    # ------------------------------------------------------

    st.session_state.analysis_result = None
    st.session_state.syntax_result = None

    # ------------------------------------------------------
    # STEP 1 — SYNTAX VALIDATION
    # ------------------------------------------------------

    st.divider()

    st.subheader(
        "1️⃣ Syntax Validation"
    )

    with st.spinner(
        "Checking source-code syntax..."
    ):

        syntax_result = SyntaxValidator.validate(
            code,
            detected_language
        )

    st.session_state.syntax_result = syntax_result

    # ======================================================
    # INVALID SYNTAX
    # ======================================================

    if not syntax_result["valid"]:

        st.error(
            "❌ Syntax Invalid"
        )

        # --------------------------------------------------
        # Error details
        # --------------------------------------------------

        error_line = syntax_result.get(
            "line"
        )

        error_column = syntax_result.get(
            "column"
        )

        error_message = syntax_result.get(
            "error"
        )

        source_line = syntax_result.get(
            "source_line"
        )

        pointer = syntax_result.get(
            "pointer"
        )

        # --------------------------------------------------
        # Error information
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if error_line is not None:

                st.metric(
                    "Error Line",
                    error_line
                )

            else:

                st.metric(
                    "Error Line",
                    "Unknown"
                )

        with col2:

            if error_column is not None:

                st.metric(
                    "Error Column",
                    error_column
                )

            else:

                st.metric(
                    "Error Column",
                    "Unknown"
                )

        # --------------------------------------------------
        # Error message
        # --------------------------------------------------

        if error_message:

            st.warning(
                f"⚠️ {error_message}"
            )

        # --------------------------------------------------
        # Show exact problematic line
        # --------------------------------------------------

        if source_line:

            st.markdown(
                "**📍 Problematic Code:**"
            )

            st.code(
                source_line,
                language=detected_language
            )

            if pointer:

                st.markdown(
                    f"`{pointer}`"
                )

        # --------------------------------------------------
        # Full syntax message
        # --------------------------------------------------

        st.markdown(
            "**🔎 Validation Details:**"
        )

        st.code(
            syntax_result.get(
                "message",
                "Syntax validation failed."
            )
        )

        # --------------------------------------------------
        # IMPORTANT:
        # DO NOT RUN AI AGENTS
        # --------------------------------------------------

        st.error(
            "🛑 AI analysis has been stopped because "
            "the submitted source code contains syntax errors."
        )

        st.info(
            "Please fix the syntax error shown above "
            "and click **Analyze Code** again."
        )

        st.stop()


    # ======================================================
    # VALID SYNTAX
    # ======================================================

    st.success(
        f"✅ Syntax Valid — "
        f"{syntax_result['message']}"
    )


    # ======================================================
    # STEP 2 — AI ANALYSIS
    # ======================================================

    st.divider()

    st.subheader(
        "2️⃣ AI Code Review"
    )

    state = {

        "code": code,

        "language": detected_language,

        "syntax_valid": True,

        "syntax_message": syntax_result[
            "message"
        ],

        "code_analysis": {},

        "security_analysis": {},

        "remediation": {},

        "pr_summary": {},

        "final_report": {}

    }


    # ------------------------------------------------------
    # RUN WORKFLOW
    # ------------------------------------------------------

    with st.spinner(
        "🤖 Running code quality and security analysis..."
    ):

        try:

            result = workflow.invoke(
                state
            )

        except Exception as e:

            st.error(
                "❌ Analysis failed."
            )

            st.exception(e)

            st.stop()


    # ======================================================
    # STORE RESULT
    # ======================================================

    final_report = result.get(
        "final_report"
    )


    if final_report is None:

        st.error(
            "❌ Analysis completed, but no final report "
            "was generated."
        )

        st.stop()


    st.session_state.analysis_result = (
        final_report
    )


    # ======================================================
    # ANALYSIS COMPLETED
    # ======================================================

    st.success(
        "✅ Analysis completed successfully."
    )


    # ======================================================
    # SHOW RESULT ON SAME PAGE
    # ======================================================

    st.divider()

    st.subheader(
        "📋 Analysis Results"
    )


    # ------------------------------------------------------
    # Scores
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Overall Score",
            f"{final_report.get('overall_score', 0)}/100"
        )


    with col2:

        st.metric(
            "Security Score",
            f"{final_report.get('security_score', 0)}/100"
        )


    with col3:

        st.metric(
            "Grade",
            final_report.get(
                "grade",
                "N/A"
            )
        )


    with col4:

        st.metric(
            "Risk Level",
            final_report.get(
                "risk_level",
                "UNKNOWN"
            )
        )


    # ------------------------------------------------------
    # Findings
    # ------------------------------------------------------

    statistics = final_report.get(
        "statistics",
        {}
    )


    st.markdown(
        "### 📊 Finding Severity"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Critical",
            statistics.get(
                "critical",
                0
            )
        )


    with col2:

        st.metric(
            "High",
            statistics.get(
                "high",
                0
            )
        )


    with col3:

        st.metric(
            "Medium",
            statistics.get(
                "medium",
                0
            )
        )


    with col4:

        st.metric(
            "Low",
            statistics.get(
                "low",
                0
            )
        )


    # ------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------

    st.markdown(
        "### 📝 Executive Summary"
    )

    st.write(
        final_report.get(
            "executive_summary",
            "No summary available."
        )
    )


    # ------------------------------------------------------
    # Code Findings
    # ------------------------------------------------------

    st.markdown(
        "### 🔍 Code Quality Findings"
    )


    code_analysis = final_report.get(
        "code_analysis",
        {}
    )

    code_llm = code_analysis.get(
        "llm",
        {}
    )

    code_summary = code_llm.get(
        "summary",
        "No code quality findings."
    )


    st.write(
        code_summary
    )


    for finding in code_llm.get(
        "findings",
        []
    ):

        if not isinstance(
            finding,
            dict
        ):
            continue


        with st.expander(
            finding.get(
                "title",
                "Code Quality Finding"
            )
        ):

            severity = finding.get(
                "severity",
                "LOW"
            )

            st.write(
                f"**Severity:** {severity}"
            )

            st.write(
                finding.get(
                    "description",
                    ""
                )
            )

            st.info(
                finding.get(
                    "recommendation",
                    ""
                )
            )


    # ------------------------------------------------------
    # Security Findings
    # ------------------------------------------------------

    st.markdown(
        "### 🛡️ Security Findings"
    )


    security_analysis = final_report.get(
        "security_analysis",
        {}
    )

    security_llm = security_analysis.get(
        "llm",
        {}
    )


    st.write(
        security_llm.get(
            "summary",
            "No security findings."
        )
    )


    for finding in security_llm.get(
        "findings",
        []
    ):

        if not isinstance(
            finding,
            dict
        ):
            continue


        with st.expander(
            finding.get(
                "title",
                "Security Finding"
            )
        ):

            severity = finding.get(
                "severity",
                "LOW"
            )

            st.write(
                f"**Severity:** {severity}"
            )

            st.write(
                finding.get(
                    "description",
                    ""
                )
            )

            st.info(
                finding.get(
                    "recommendation",
                    ""
                )
            )


    # ------------------------------------------------------
    # Remediation
    # ------------------------------------------------------

    st.markdown(
        "### 🛠️ Remediation Recommendations"
    )


    remediation = final_report.get(
        "remediation",
        {}
    )


    recommendations = remediation.get(
        "recommendations",
        []
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        if not isinstance(
            recommendation,
            dict
        ):
            continue


        with st.expander(
            f"{index}. "
            f"{recommendation.get('issue', 'Recommendation')}"
        ):

            st.write(
                "**Category:**",
                recommendation.get(
                    "category",
                    ""
                )
            )

            st.write(
                "**Severity:**",
                recommendation.get(
                    "severity",
                    "LOW"
                )
            )

            st.success(
                recommendation.get(
                    "fix",
                    ""
                )
            )


    # ------------------------------------------------------
    # PR Summary
    # ------------------------------------------------------

    st.markdown(
        "### 📝 Pull Request Summary"
    )


    pr_summary = final_report.get(
        "pr_summary",
        {}
    )


    st.write(
        pr_summary.get(
            "executive_summary",
            "No PR summary available."
        )
    )


    # ------------------------------------------------------
    # Submitted Code
    # ------------------------------------------------------

    st.divider()

    with st.expander(
        "📄 View Submitted Source Code"
    ):

        st.code(
            code,
            language=detected_language
        )