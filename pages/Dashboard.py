import streamlit as st
import plotly.express as px

from utils.ui_helper import severity_badge


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title("📊 AI Code Review Dashboard")

st.caption(
    "Overview of the latest code quality and security analysis."
)


# ==========================================================
# CHECK ANALYSIS RESULT
# ==========================================================

report = st.session_state.get("analysis_result")

if not report:

    st.info(
        "No analysis report is available yet."
    )

    st.write(
        "Go to **Code Submission & Analysis** "
        "to upload or paste your code."
    )

    if st.button(
        "🔍 Go to Code Submission & Analysis"
    ):

        st.switch_page(
            "pages/Code_Submission.py"
        )

    st.stop()


# ==========================================================
# SCORE CARDS
# ==========================================================

st.subheader("Overall Assessment")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Overall Score",
        f"{report.get('overall_score', 0)}%"
    )


with col2:

    st.metric(
        "Security Score",
        f"{report.get('security_score', 0)}%"
    )


with col3:

    st.metric(
        "Grade",
        report.get(
            "grade",
            "N/A"
        )
    )


with col4:

    st.metric(
        "Risk Level",
        report.get(
            "risk_level",
            "UNKNOWN"
        )
    )


# ==========================================================
# SEVERITY DATA
# ==========================================================

st.divider()

st.subheader(
    "Finding Severity Distribution"
)

stats = report.get(
    "statistics",
    {}
)

severity_data = {

    "Severity": [
        "Critical",
        "High",
        "Medium",
        "Low"
    ],

    "Count": [

        stats.get(
            "critical",
            0
        ),

        stats.get(
            "high",
            0
        ),

        stats.get(
            "medium",
            0
        ),

        stats.get(
            "low",
            0
        )
    ]
}


fig = px.bar(

    severity_data,

    x="Severity",

    y="Count",

    title="Issues by Severity"

)


st.plotly_chart(

    fig,

    use_container_width=True
)


# ==========================================================
# SYNTAX VALIDATION
# ==========================================================

st.divider()

st.subheader(
    "✅ Syntax Validation"
)

syntax = report.get(
    "syntax_validation",
    {}
)


if syntax.get(
    "valid",
    False
):

    st.success(
        syntax.get(
            "message",
            "Syntax is valid."
        )
    )

else:

    st.error(
        syntax.get(
            "message",
            "Syntax validation failed."
        )
    )


# ==========================================================
# CODE QUALITY FINDINGS
# ==========================================================

st.divider()

st.subheader(
    "🔍 Code Quality Findings"
)

code_analysis = report.get(
    "code_analysis",
    {}
)

code_llm = code_analysis.get(
    "llm",
    {}
)


st.write(
    code_llm.get(
        "summary",
        "No code quality summary available."
    )
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


    title = finding.get(
        "title",
        "Code Quality Finding"
    )


    with st.expander(
        title
    ):

        severity_badge(
            finding.get(
                "severity",
                "LOW"
            )
        )

        st.write(
            finding.get(
                "description",
                "No description available."
            )
        )

        st.success(
            finding.get(
                "recommendation",
                "No recommendation available."
            )
        )


# ==========================================================
# SECURITY FINDINGS
# ==========================================================

st.divider()

st.subheader(
    "🛡️ Security Findings"
)

security_analysis = report.get(
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
        "No security summary available."
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


    title = finding.get(
        "title",
        "Security Finding"
    )


    with st.expander(
        title
    ):

        severity_badge(
            finding.get(
                "severity",
                "LOW"
            )
        )

        st.write(
            finding.get(
                "description",
                "No description available."
            )
        )

        st.success(
            finding.get(
                "recommendation",
                "No recommendation available."
            )
        )


# ==========================================================
# REMEDIATION
# ==========================================================

st.divider()

st.subheader(
    "🛠️ Remediation Recommendations"
)

remediation = report.get(
    "remediation",
    {}
)

recommendations = remediation.get(
    "recommendations",
    []
)


if not recommendations:

    st.info(
        "No remediation recommendations available."
    )


for recommendation in recommendations:

    if not isinstance(
        recommendation,
        dict
    ):

        continue


    issue = recommendation.get(
        "issue",
        "Remediation"
    )


    with st.expander(
        issue
    ):

        severity_badge(
            recommendation.get(
                "severity",
                "LOW"
            )
        )

        st.write(
            "Category:",
            recommendation.get(
                "category",
                "General"
            )
        )

        st.success(
            recommendation.get(
                "fix",
                "No fix available."
            )
        )


# ==========================================================
# PR SUMMARY
# ==========================================================

st.divider()

st.subheader(
    "📝 Pull Request Summary"
)

pr = report.get(
    "pr_summary",
    {}
)


st.write(
    pr.get(
        "executive_summary",
        "No PR summary available."
    )
)


required_actions = pr.get(
    "required_actions",
    []
)


st.metric(
    "Recommended Actions",
    len(required_actions)
)


if required_actions:

    for action in required_actions:

        if isinstance(
            action,
            dict
        ):

            st.write(
                f"• {action.get('issue', 'Issue')}"
            )


# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

st.subheader(
    "Quick Actions"
)

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "🔍 Analyze New Code",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Code_Submission.py"
        )


with col2:

    if st.button(
        "💬 Open Coding Assistant",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Coding_Assistant.py"
        )