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

    if filename:

        filename_lower = filename.lower()

        if filename_lower.endswith(".py"):
            return "python"

        if filename_lower.endswith(".java"):
            return "java"

    stripped_code = source_code.strip()

    if not stripped_code:
        return None

    python_patterns = [
        "def ",
        "import ",
        "from ",
        "elif ",
        "for ",
        "while ",
        "if ",
        "print(",
        "async def ",
        "with ",
        "try:",
    ]

    java_patterns = [
        "public class ",
        "private class ",
        "protected class ",
        "public static void main",
        "System.out.println",
        "import java.",
        "package ",
        "extends ",
        "implements ",
        "interface ",
        "enum ",
    ]

    python_score = sum(
        1
        for pattern in python_patterns
        if pattern in stripped_code
    )

    java_score = sum(
        1
        for pattern in java_patterns
        if pattern in stripped_code
    )

    if python_score == 0 and java_score == 0:
        return None

    if python_score > java_score:
        return "python"

    if java_score > python_score:
        return "java"

    return None


# ==========================================================
# SECURITY PATTERNS
# ==========================================================

SECURITY_PATTERNS = [
    "sql injection",
    "command injection",
    "os command injection",
    "shell injection",
    "code injection",
    "arbitrary code execution",
    "remote code execution",
    "path traversal",
    "directory traversal",
    "unsafe deserialization",
    "insecure deserialization",
    "hardcoded password",
    "hardcoded credential",
    "hardcoded credentials",
    "hardcoded secret",
    "hardcoded api key",
    "hardcoded token",
    "weak authentication",
    "authentication bypass",
    "authorization bypass",
    "privilege escalation",
    "sensitive information exposure",
    "information disclosure",
    "cross-site scripting",
    "xss",
    "cross-site request forgery",
    "csrf",
    "server-side request forgery",
    "ssrf",
    "weak cryptography",
    "weak encryption",
    "insecure random",
    "eval(",
    "exec(",
    "os.system",
    "subprocess",
]


# ==========================================================
# NORMALIZE FINDING
# ==========================================================

def normalize_finding(finding):

    if not isinstance(finding, dict):
        return None

    title = str(
        finding.get(
            "title",
            "Unnamed Finding"
        )
    ).strip()

    severity = str(
        finding.get(
            "severity",
            "LOW"
        )
    ).upper().strip()

    if severity not in {
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    }:
        severity = "LOW"

    description = str(
        finding.get(
            "description",
            finding.get(
                "message",
                ""
            )
        )
    ).strip()

    recommendation = str(
        finding.get(
            "recommendation",
            finding.get(
                "fix",
                ""
            )
        )
    ).strip()

    normalized = {
        "title": title,
        "severity": severity,
        "description": description,
        "recommendation": recommendation,
    }

    optional_fields = [
        "category",
        "line",
        "end_line",
        "rule_id",
        "cwe",
        "owasp",
        "path",
        "developer_action",
    ]

    for field in optional_fields:

        if field in finding:
            normalized[field] = finding[field]

    return normalized


# ==========================================================
# SECURITY FINDING DETECTION
# ==========================================================

def is_security_finding(finding):

    if not isinstance(finding, dict):
        return False

    title = str(
        finding.get(
            "title",
            ""
        )
    ).lower()

    description = str(
        finding.get(
            "description",
            finding.get(
                "message",
                ""
            )
        )
    ).lower()

    recommendation = str(
        finding.get(
            "recommendation",
            finding.get(
                "fix",
                ""
            )
        )
    ).lower()

    category = str(
        finding.get(
            "category",
            ""
        )
    ).lower()

    rule_id = str(
        finding.get(
            "rule_id",
            ""
        )
    ).lower()

    cwe = str(
        finding.get(
            "cwe",
            ""
        )
    ).lower()

    owasp = str(
        finding.get(
            "owasp",
            ""
        )
    ).lower()

    searchable_text = " ".join(
        [
            title,
            description,
            recommendation,
            category,
            rule_id,
            cwe,
            owasp,
        ]
    )

    if category in {
        "security",
        "vulnerability",
        "security vulnerability",
        "sast",
    }:
        return True

    if "cwe-" in searchable_text:
        return True

    if "owasp" in searchable_text:
        return True

    for pattern in SECURITY_PATTERNS:

        if pattern in searchable_text:
            return True

    return False


# ==========================================================
# FINDING KEY
# ==========================================================

def finding_key(finding):

    if not isinstance(finding, dict):
        return None

    title = str(
        finding.get(
            "title",
            ""
        )
    ).lower().strip()

    title = " ".join(
        title.split()
    )

    line = finding.get(
        "line"
    )

    end_line = finding.get(
        "end_line"
    )

    rule_id = str(
        finding.get(
            "rule_id",
            ""
        )
    ).lower().strip()

    if line is not None:

        return (
            title,
            str(line),
            str(end_line),
            rule_id,
        )

    return (
        title,
        rule_id,
    )


# ==========================================================
# DEDUPLICATE FINDINGS
# ==========================================================

def deduplicate_findings(findings):

    unique_findings = []
    seen = set()

    for finding in findings:

        normalized = normalize_finding(
            finding
        )

        if normalized is None:
            continue

        key = finding_key(
            normalized
        )

        if key in seen:
            continue

        seen.add(key)

        unique_findings.append(
            normalized
        )

    return unique_findings


# ==========================================================
# SEPARATE FINDINGS
# ==========================================================

def separate_findings(
    code_findings,
    security_findings
):

    normalized_code_findings = []

    normalized_security_findings = []

    for finding in code_findings:

        normalized = normalize_finding(
            finding
        )

        if normalized is None:
            continue

        if is_security_finding(
            normalized
        ):

            normalized_security_findings.append(
                normalized
            )

        else:

            normalized_code_findings.append(
                normalized
            )

    for finding in security_findings:

        normalized = normalize_finding(
            finding
        )

        if normalized is None:
            continue

        normalized_security_findings.append(
            normalized
        )

    normalized_code_findings = (
        deduplicate_findings(
            normalized_code_findings
        )
    )

    normalized_security_findings = (
        deduplicate_findings(
            normalized_security_findings
        )
    )

    final_code_findings = []

    for finding in normalized_code_findings:

        if not is_security_finding(
            finding
        ):

            final_code_findings.append(
                finding
            )

    final_security_findings = (
        deduplicate_findings(
            normalized_security_findings
        )
    )

    return (
        final_code_findings,
        final_security_findings
    )


# ==========================================================
# STATISTICS
# ==========================================================

def calculate_statistics(
    code_findings,
    security_findings
):

    all_findings = (
        code_findings +
        security_findings
    )

    statistics = {
        "total": len(all_findings),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for finding in all_findings:

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper()

        severity_key = severity.lower()

        if severity_key in statistics:

            statistics[
                severity_key
            ] += 1

    return statistics


# ==========================================================
# SCORE
# ==========================================================

def calculate_score(findings):

    if not findings:
        return 100

    weights = {
        "CRITICAL": 30,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5,
    }

    penalty = 0

    for finding in findings:

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper()

        penalty += weights.get(
            severity,
            0
        )

    return max(
        0,
        100 - penalty
    )


# ==========================================================
# GRADE
# ==========================================================

def calculate_grade(score):

    if score >= 90:
        return "A"

    if score >= 80:
        return "B"

    if score >= 70:
        return "C"

    if score >= 60:
        return "D"

    return "F"


# ==========================================================
# RISK LEVEL
# ==========================================================

def calculate_risk_level(
    code_findings,
    security_findings
):

    all_findings = (
        code_findings +
        security_findings
    )

    severities = {
        str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper()
        for finding in all_findings
    }

    if "CRITICAL" in severities:
        return "CRITICAL"

    if "HIGH" in severities:
        return "HIGH"

    if "MEDIUM" in severities:
        return "MEDIUM"

    if "LOW" in severities:
        return "LOW"

    return "NONE"


# ==========================================================
# NORMALIZE RECOMMENDATIONS
# ==========================================================

def normalize_recommendations(
    recommendations
):

    unique = []
    seen = set()

    for recommendation in recommendations:

        if not isinstance(
            recommendation,
            dict
        ):
            continue

        issue = str(
            recommendation.get(
                "issue",
                ""
            )
        ).strip()

        fix = str(
            recommendation.get(
                "fix",
                ""
            )
        ).strip()

        severity = str(
            recommendation.get(
                "severity",
                recommendation.get(
                    "priority",
                    "LOW"
                )
            )
        ).upper()

        category = recommendation.get(
            "category",
            ""
        )

        key = (
            issue.lower(),
            category.lower(),
            fix.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(
            {
                "issue": issue,
                "fix": fix,
                "severity": severity,
                "priority": severity,
                "category": category,
                "description": recommendation.get(
                    "description",
                    ""
                ),
                "developer_action": recommendation.get(
                    "developer_action",
                    ""
                ),
            }
        )

    return unique


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
    detected_language
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

    st.session_state.analysis_result = None
    st.session_state.syntax_result = None

    # ======================================================
    # STEP 1 — SYNTAX VALIDATION
    # ======================================================

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

    st.session_state.syntax_result = (
        syntax_result
    )

    # ======================================================
    # INVALID SYNTAX
    # ======================================================

    if not syntax_result["valid"]:

        st.error(
            "❌ Syntax Invalid"
        )

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

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Error Line",
                error_line
                if error_line is not None
                else "Unknown"
            )

        with col2:

            st.metric(
                "Error Column",
                error_column
                if error_column is not None
                else "Unknown"
            )

        if error_message:

            st.warning(
                f"⚠️ {error_message}"
            )

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

        st.markdown(
            "**🔎 Validation Details:**"
        )

        st.code(
            syntax_result.get(
                "message",
                "Syntax validation failed."
            )
        )

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

    # ======================================================
    # RUN WORKFLOW
    # ======================================================

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
    # EXTRACT FINAL REPORT
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

    if not isinstance(
        final_report,
        dict
    ):

        st.error(
            "❌ Invalid final analysis report."
        )

        st.stop()

    # ======================================================
    # EXTRACT RAW FINDINGS
    # ======================================================

    raw_code_findings = (
        final_report
        .get(
            "code_analysis",
            {}
        )
        .get(
            "llm",
            {}
        )
        .get(
            "findings",
            []
        )
    )

    raw_security_findings = (
        final_report
        .get(
            "security_analysis",
            {}
        )
        .get(
            "llm",
            {}
        )
        .get(
            "findings",
            []
        )
    )

    # ======================================================
    # SEPARATE FINDINGS
    # ======================================================

    (
        code_findings,
        security_findings
    ) = separate_findings(
        raw_code_findings,
        raw_security_findings
    )

    # ======================================================
    # UPDATE CODE QUALITY
    # ======================================================

    if "code_analysis" not in final_report:

        final_report[
            "code_analysis"
        ] = {}

    if "llm" not in final_report[
        "code_analysis"
    ]:

        final_report[
            "code_analysis"
        ][
            "llm"
        ] = {}

    final_report[
        "code_analysis"
    ][
        "llm"
    ][
        "findings"
    ] = code_findings

    # ======================================================
    # UPDATE SECURITY
    # ======================================================

    if "security_analysis" not in final_report:

        final_report[
            "security_analysis"
        ] = {}

    if "llm" not in final_report[
        "security_analysis"
    ]:

        final_report[
            "security_analysis"
        ][
            "llm"
        ] = {}

    final_report[
        "security_analysis"
    ][
        "llm"
    ][
        "findings"
    ] = security_findings

    # ======================================================
    # STATISTICS
    # ======================================================

    statistics = calculate_statistics(
        code_findings,
        security_findings
    )

    final_report[
        "statistics"
    ] = statistics

    # ======================================================
    # SCORES
    # ======================================================

    code_quality_score = calculate_score(
        code_findings
    )

    security_score = calculate_score(
        security_findings
    )

    overall_score = round(
        (
            code_quality_score +
            security_score
        ) / 2
    )

    final_report[
        "code_quality_score"
    ] = code_quality_score

    final_report[
        "security_score"
    ] = security_score

    final_report[
        "overall_score"
    ] = overall_score

    final_report[
        "grade"
    ] = calculate_grade(
        overall_score
    )

    final_report[
        "risk_level"
    ] = calculate_risk_level(
        code_findings,
        security_findings
    )

    # ======================================================
    # REMEDIATION
    # ======================================================

    remediation = final_report.get(
        "remediation",
        {}
    )

    if not isinstance(
        remediation,
        dict
    ):

        remediation = {}

    recommendations = remediation.get(
        "recommendations",
        []
    )

    remediation[
        "recommendations"
    ] = normalize_recommendations(
        recommendations
    )

    final_report[
        "remediation"
    ] = remediation

    # ======================================================
    # STORE FINAL REPORT
    # ======================================================

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
    # RESULTS
    # ======================================================

    st.divider()

    st.subheader(
        "📋 Analysis Results"
    )

    # ======================================================
    # SCORE CARDS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall Score",
            f"{final_report.get('overall_score', 0)}/100"
        )

    with col2:

        st.metric(
            "Code Quality Score",
            f"{final_report.get('code_quality_score', 0)}/100"
        )

    with col3:

        st.metric(
            "Security Score",
            f"{final_report.get('security_score', 0)}/100"
        )

    with col4:

        st.metric(
            "Grade",
            final_report.get(
                "grade",
                "N/A"
            )
        )

    # ======================================================
    # RISK
    # ======================================================

    st.write(
        f"**Risk Level:** "
        f"{final_report.get('risk_level', 'NONE')}"
    )

    # ======================================================
    # FINDING SEVERITY
    # ======================================================

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

    # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================

    st.markdown(
        "### 📝 Executive Summary"
    )

    st.write(
        final_report.get(
            "executive_summary",
            "No summary available."
        )
    )

    # ======================================================
    # CODE QUALITY FINDINGS
    # ======================================================

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

    code_quality_findings = code_llm.get(
        "findings",
        []
    )

    if code_quality_findings:

        for index, finding in enumerate(
            code_quality_findings,
            start=1
        ):

            if not isinstance(
                finding,
                dict
            ):
                continue

            title = finding.get(
                "title",
                "Code Quality Finding"
            )

            severity = finding.get(
                "severity",
                "LOW"
            )

            with st.expander(
                f"{index}. {title} [{severity}]"
            ):

                # ------------------------------------------
                # BASIC INFORMATION
                # ------------------------------------------

                st.markdown(
                    "#### 📌 Finding Information"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        "**Category:** Code Quality"
                    )

                with col2:

                    st.write(
                        f"**Severity:** {severity}"
                    )

                with col3:

                    if finding.get("line"):

                        st.write(
                            f"**Line:** "
                            f"{finding.get('line')}"
                        )

                # ------------------------------------------
                # RULE ID
                # ------------------------------------------

                if finding.get("rule_id"):

                    st.write(
                        f"**Rule ID:** "
                        f"{finding.get('rule_id')}"
                    )

                # ------------------------------------------
                # DESCRIPTION
                # ------------------------------------------

                if finding.get("description"):

                    st.markdown(
                        "#### 📖 Description"
                    )

                    st.write(
                        finding.get(
                            "description"
                        )
                    )

                # ------------------------------------------
                # RECOMMENDATION
                # ------------------------------------------

                if finding.get(
                    "recommendation"
                ):

                    st.markdown(
                        "#### 🛠️ Recommended Fix"
                    )

                    st.success(
                        finding.get(
                            "recommendation"
                        )
                    )

    else:

        st.success(
            "No code quality issues detected."
        )

    # ======================================================
    # SECURITY FINDINGS
    # ======================================================

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

    security_summary = security_llm.get(
        "summary",
        "No security findings."
    )

    st.write(
        security_summary
    )

    security_findings_display = (
        security_llm.get(
            "findings",
            []
        )
    )

    if security_findings_display:

        for index, finding in enumerate(
            security_findings_display,
            start=1
        ):

            if not isinstance(
                finding,
                dict
            ):
                continue

            title = finding.get(
                "title",
                "Security Finding"
            )

            severity = finding.get(
                "severity",
                "LOW"
            )

            with st.expander(
                f"{index}. {title} [{severity}]"
            ):

                # ------------------------------------------
                # FINDING INFORMATION
                # ------------------------------------------

                st.markdown(
                    "#### 📌 Finding Information"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        "**Category:** Security"
                    )

                with col2:

                    st.write(
                        f"**Severity:** {severity}"
                    )

                with col3:

                    if finding.get("line"):

                        st.write(
                            f"**Line:** "
                            f"{finding.get('line')}"
                        )

                # ------------------------------------------
                # RULE ID
                # ------------------------------------------

                if finding.get("rule_id"):

                    st.write(
                        f"**Rule ID:** "
                        f"{finding.get('rule_id')}"
                    )

                # ------------------------------------------
                # CWE
                # ------------------------------------------

                if finding.get("cwe"):

                    st.write(
                        f"**CWE:** "
                        f"{finding.get('cwe')}"
                    )

                # ------------------------------------------
                # OWASP
                # ------------------------------------------

                if finding.get("owasp"):

                    st.write(
                        f"**OWASP:** "
                        f"{finding.get('owasp')}"
                    )

                # ------------------------------------------
                # DESCRIPTION
                # ------------------------------------------

                if finding.get("description"):

                    st.markdown(
                        "#### 📖 Description"
                    )

                    st.write(
                        finding.get(
                            "description"
                        )
                    )

                # ------------------------------------------
                # RECOMMENDATION
                # ------------------------------------------

                if finding.get(
                    "recommendation"
                ):

                    st.markdown(
                        "#### 🛠️ Recommended Fix"
                    )

                    st.success(
                        finding.get(
                            "recommendation"
                        )
                    )

                else:

                    st.info(
                        "No recommendation was returned "
                        "for this finding."
                    )

                # ------------------------------------------
                # SOURCE LOCATION
                # ------------------------------------------

                if finding.get("path"):

                    st.write(
                        f"**File:** "
                        f"{finding.get('path')}"
                    )

    else:

        st.success(
            "No security vulnerabilities detected."
        )

    # ======================================================
    # REMEDIATION RECOMMENDATIONS
    # ======================================================

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

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            if not isinstance(
                recommendation,
                dict
            ):
                continue

            issue = recommendation.get(
                "issue",
                "Recommendation"
            )

            severity = recommendation.get(
                "severity",
                "LOW"
            )

            category = recommendation.get(
                "category",
                "Code Quality"
            )

            with st.expander(
                f"{index}. {issue} [{severity}]"
            ):

                st.markdown(
                    "#### 📌 Recommendation Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Category:** {category}"
                    )

                with col2:

                    st.write(
                        f"**Severity:** {severity}"
                    )

                # ------------------------------------------
                # DESCRIPTION
                # ------------------------------------------

                if recommendation.get(
                    "description"
                ):

                    st.markdown(
                        "#### 📖 Issue Description"
                    )

                    st.write(
                        recommendation.get(
                            "description"
                        )
                    )

                # ------------------------------------------
                # FIX
                # ------------------------------------------

                if recommendation.get(
                    "fix"
                ):

                    st.markdown(
                        "#### 🛠️ Recommended Fix"
                    )

                    st.success(
                        recommendation.get(
                            "fix"
                        )
                    )

                # ------------------------------------------
                # DEVELOPER ACTION
                # ------------------------------------------

                if recommendation.get(
                    "developer_action"
                ):

                    st.markdown(
                        "#### 👨‍💻 Developer Action"
                    )

                    st.info(
                        recommendation.get(
                            "developer_action"
                        )
                    )

    else:

        st.info(
            "No remediation recommendations available."
        )

    # ======================================================
    # PULL REQUEST SUMMARY
    # ======================================================

    st.markdown(
        "### 📝 Pull Request Summary"
    )

    pr_summary = final_report.get(
        "pr_summary",
        {}
    )

    if pr_summary:

        st.write(
            pr_summary.get(
                "executive_summary",
                "No PR summary available."
            )
        )

        # ----------------------------------------------
        # IMPACT ANALYSIS
        # ----------------------------------------------

        impact = pr_summary.get(
            "impact_analysis",
            {}
        )

        if impact:

            st.markdown(
                "#### 📊 Impact Analysis"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Critical",
                    impact.get(
                        "critical",
                        0
                    )
                )

            with col2:

                st.metric(
                    "High",
                    impact.get(
                        "high",
                        0
                    )
                )

            with col3:

                st.metric(
                    "Medium",
                    impact.get(
                        "medium",
                        0
                    )
                )

            with col4:

                st.metric(
                    "Low",
                    impact.get(
                        "low",
                        0
                    )
                )

        # ----------------------------------------------
        # REQUIRED ACTIONS
        # ----------------------------------------------

        required_actions = pr_summary.get(
            "required_actions",
            []
        )

        if required_actions:

            st.markdown(
                "#### 🎯 Required Actions"
            )

            for index, action in enumerate(
                required_actions,
                start=1
            ):

                if not isinstance(
                    action,
                    dict
                ):
                    continue

                st.write(
                    f"{index}. "
                    f"**{action.get('issue', '')}** "
                    f"— "
                    f"{action.get('severity', 'LOW')}"
                )

                if action.get(
                    "action"
                ):

                    st.caption(
                        action.get(
                            "action"
                        )
                    )

        st.write(
            f"**Risk Level:** "
            f"{pr_summary.get('risk_level', 'NONE')}"
        )

        st.write(
            f"**Overall Score:** "
            f"{pr_summary.get('overall_score', 0)}/100"
        )

        st.write(
            f"**Code Quality Score:** "
            f"{pr_summary.get('code_quality_score', 0)}/100"
        )

        st.write(
            f"**Security Score:** "
            f"{pr_summary.get('security_score', 0)}/100"
        )

        st.write(
            f"**Grade:** "
            f"{pr_summary.get('grade', 'N/A')}"
        )

    else:

        st.info(
            "No PR summary available."
        )

    # ======================================================
    # SUBMITTED SOURCE CODE
    # ======================================================

    st.divider()

    with st.expander(
        "📄 View Submitted Source Code"
    ):

        st.code(
            code,
            language=detected_language
        )