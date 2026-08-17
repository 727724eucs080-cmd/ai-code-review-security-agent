import streamlit as st
import plotly.express as px
import pandas as pd

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

report = st.session_state.get(
    "analysis_result"
)

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
# GET STATISTICS
# ==========================================================

stats = report.get(
    "statistics",
    {}
)

if not isinstance(
    stats,
    dict
):
    stats = {}


critical_count = stats.get(
    "critical",
    0
)

high_count = stats.get(
    "high",
    0
)

medium_count = stats.get(
    "medium",
    0
)

low_count = stats.get(
    "low",
    0
)

total_findings = stats.get(
    "total",
    0
)


# ==========================================================
# GET CODE QUALITY FINDINGS
# ==========================================================

code_analysis = report.get(
    "code_analysis",
    {}
)

if not isinstance(
    code_analysis,
    dict
):
    code_analysis = {}


code_llm = code_analysis.get(
    "llm",
    {}
)

if not isinstance(
    code_llm,
    dict
):
    code_llm = {}


code_quality_findings = code_llm.get(
    "findings",
    []
)

if not isinstance(
    code_quality_findings,
    list
):
    code_quality_findings = []


# ==========================================================
# GET SECURITY FINDINGS
# ==========================================================

security_analysis = report.get(
    "security_analysis",
    {}
)

if not isinstance(
    security_analysis,
    dict
):
    security_analysis = {}


security_llm = security_analysis.get(
    "llm",
    {}
)

if not isinstance(
    security_llm,
    dict
):
    security_llm = {}


security_findings = security_llm.get(
    "findings",
    []
)

if not isinstance(
    security_findings,
    list
):
    security_findings = []


# ==========================================================
# GET REMEDIATION
# ==========================================================

remediation = report.get(
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

if not isinstance(
    recommendations,
    list
):
    recommendations = []


# ==========================================================
# SCORE VALUES
# ==========================================================

overall_score = report.get(
    "overall_score",
    0
)

security_score = report.get(
    "security_score",
    0
)

code_quality_score = report.get(
    "code_quality_score",
    0
)

grade = report.get(
    "grade",
    "N/A"
)

risk_level = report.get(
    "risk_level",
    "UNKNOWN"
)


# ==========================================================
# OVERALL ASSESSMENT
# ==========================================================

st.subheader(
    "Overall Assessment"
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Overall Score",
        f"{overall_score}%"
    )


with col2:

    st.metric(
        "Security Score",
        f"{security_score}%"
    )


with col3:

    st.metric(
        "Grade",
        grade
    )


with col4:

    st.metric(
        "Risk Level",
        risk_level
    )


# ==========================================================
# FINDING OVERVIEW CARDS
# ==========================================================

st.divider()

st.subheader(
    "📌 Finding Overview"
)

code_quality_count = len(
    code_quality_findings
)

security_count = len(
    security_findings
)

remediation_count = len(
    recommendations
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Findings",
        total_findings
    )


with col2:

    st.metric(
        "Code Quality Issues",
        code_quality_count
    )


with col3:

    st.metric(
        "Security Issues",
        security_count
    )


with col4:

    st.metric(
        "Remediation Actions",
        remediation_count
    )


# ==========================================================
# CHART SECTION
# ==========================================================

st.divider()

st.subheader(
    "📊 Visual Analysis"
)


# ==========================================================
# SEVERITY DATA
# ==========================================================

severity_data = pd.DataFrame(
    {
        "Severity": [
            "Critical",
            "High",
            "Medium",
            "Low"
        ],

        "Count": [
            critical_count,
            high_count,
            medium_count,
            low_count
        ]
    }
)


# ==========================================================
# CATEGORY DATA
# ==========================================================

category_data = pd.DataFrame(
    {
        "Category": [
            "Code Quality",
            "Security"
        ],

        "Count": [
            code_quality_count,
            security_count
        ]
    }
)


# ==========================================================
# SCORE DATA
# ==========================================================

score_data = pd.DataFrame(
    {
        "Score": [
            "Overall",
            "Code Quality",
            "Security"
        ],

        "Value": [
            overall_score,
            code_quality_score,
            security_score
        ]
    }
)


# ==========================================================
# FIRST ROW — BAR + DONUT
# ==========================================================

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# SEVERITY BAR CHART
# ----------------------------------------------------------

with col1:

    fig_severity_bar = px.bar(
        severity_data,
        x="Severity",
        y="Count",
        title="Issues by Severity",
        text="Count"
    )

    fig_severity_bar.update_traces(
        textposition="outside"
    )

    fig_severity_bar.update_layout(
        xaxis_title="Severity",
        yaxis_title="Number of Findings",
        showlegend=False
    )

    st.plotly_chart(
        fig_severity_bar,
        use_container_width=True
    )


# ----------------------------------------------------------
# SEVERITY DONUT CHART
# ----------------------------------------------------------

with col2:

    severity_pie_data = severity_data[
        severity_data["Count"] > 0
    ]

    if not severity_pie_data.empty:

        fig_severity_pie = px.pie(
            severity_pie_data,
            names="Severity",
            values="Count",
            title="Severity Distribution",
            hole=0.45
        )

        fig_severity_pie.update_traces(
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_severity_pie,
            use_container_width=True
        )

    else:

        st.info(
            "No findings available for severity distribution."
        )


# ==========================================================
# SECOND ROW — CATEGORY + SCORE
# ==========================================================

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# CATEGORY DONUT
# ----------------------------------------------------------

with col1:

    category_pie_data = category_data[
        category_data["Count"] > 0
    ]

    if not category_pie_data.empty:

        fig_category_pie = px.pie(
            category_pie_data,
            names="Category",
            values="Count",
            title="Code Quality vs Security",
            hole=0.45
        )

        fig_category_pie.update_traces(
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_category_pie,
            use_container_width=True
        )

    else:

        st.info(
            "No category data available."
        )


# ----------------------------------------------------------
# SCORE COMPARISON
# ----------------------------------------------------------

with col2:

    fig_scores = px.bar(
        score_data,
        x="Score",
        y="Value",
        title="Score Comparison",
        text="Value"
    )

    fig_scores.update_traces(
        textposition="outside"
    )

    fig_scores.update_layout(
        yaxis_title="Score",
        xaxis_title="",
        yaxis_range=[0, 100],
        showlegend=False
    )

    st.plotly_chart(
        fig_scores,
        use_container_width=True
    )


# ==========================================================
# SEVERITY BY CATEGORY
# ==========================================================

st.markdown(
    "### 📈 Severity by Finding Category"
)


category_severity_data = []


for finding in code_quality_findings:

    if not isinstance(
        finding,
        dict
    ):
        continue

    severity = str(
        finding.get(
            "severity",
            "LOW"
        )
    ).upper()

    category_severity_data.append(
        {
            "Category": "Code Quality",
            "Severity": severity
        }
    )


for finding in security_findings:

    if not isinstance(
        finding,
        dict
    ):
        continue

    severity = str(
        finding.get(
            "severity",
            "LOW"
        )
    ).upper()

    category_severity_data.append(
        {
            "Category": "Security",
            "Severity": severity
        }
    )


if category_severity_data:

    category_severity_df = pd.DataFrame(
        category_severity_data
    )

    category_severity_df = (
        category_severity_df
        .groupby(
            [
                "Category",
                "Severity"
            ]
        )
        .size()
        .reset_index(
            name="Count"
        )
    )

    fig_category_severity = px.bar(
        category_severity_df,
        x="Category",
        y="Count",
        color="Severity",
        barmode="stack",
        title="Severity Breakdown by Category",
        text="Count"
    )

    fig_category_severity.update_layout(
        xaxis_title="Finding Category",
        yaxis_title="Number of Findings"
    )

    st.plotly_chart(
        fig_category_severity,
        use_container_width=True
    )

else:

    st.info(
        "No finding data available for category analysis."
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

if not isinstance(
    syntax,
    dict
):
    syntax = {}


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

st.write(
    code_llm.get(
        "summary",
        "No code quality summary available."
    )
)


if code_quality_findings:

    for finding in code_quality_findings:

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

            recommendation = finding.get(
                "recommendation",
                ""
            )

            if recommendation:

                st.success(
                    recommendation
                )

else:

    st.success(
        "No code quality issues detected."
    )


# ==========================================================
# SECURITY FINDINGS
# ==========================================================

st.divider()

st.subheader(
    "🛡️ Security Findings"
)

st.write(
    security_llm.get(
        "summary",
        "No security summary available."
    )
)


if security_findings:

    for finding in security_findings:

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

            recommendation = finding.get(
                "recommendation",
                ""
            )

            if recommendation:

                st.success(
                    recommendation
                )

else:

    st.success(
        "No security vulnerabilities detected."
    )


# ==========================================================
# REMEDIATION
# ==========================================================

st.divider()

st.subheader(
    "🛠️ Remediation Recommendations"
)


if not recommendations:

    st.info(
        "No remediation recommendations available."
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

    issue = recommendation.get(
        "issue",
        "Remediation"
    )

    with st.expander(
        f"{index}. {issue}"
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

        st.write(
            "Description:",
            recommendation.get(
                "description",
                ""
            )
        )

        st.success(
            recommendation.get(
                "fix",
                "No fix available."
            )
        )

        developer_action = recommendation.get(
            "developer_action",
            ""
        )

        if developer_action:

            st.info(
                f"Developer Action: {developer_action}"
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

if not isinstance(
    pr,
    dict
):
    pr = {}


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

if not isinstance(
    required_actions,
    list
):
    required_actions = []


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
    "⚡ Quick Actions"
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
            "pages/Secure_Coding_Assistant.py"
        )