import streamlit as st

from reports.pdf_export import PDFExporter
from reports.json_export import JSONExporter


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Final Analysis Report")


# ==========================================================
# CHECK ANALYSIS RESULT
# ==========================================================

report = st.session_state.get("analysis_result")

if report is None:
    st.info("📋 No analysis report available yet.")
    st.write("Please submit and analyze your code first.")
    st.stop()

if not isinstance(report, dict):
    st.error("❌ Invalid analysis report.")
    st.stop()


# ==========================================================
# REPORT INFORMATION
# ==========================================================

st.subheader("📋 Report Information")

metadata = report.get("metadata", {})

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Language",
        metadata.get(
            "language",
            "Unknown"
        )
    )


with col2:

    st.metric(
        "Generated",
        metadata.get(
            "generated_at",
            "Unknown"
        )
    )


with col3:

    st.metric(
        "Risk Level",
        report.get(
            "risk_level",
            "Unknown"
        )
    )


# ==========================================================
# OVERALL SUMMARY
# ==========================================================

st.divider()

st.subheader("📊 Overall Summary")

col1, col2, col3 = st.columns(3)


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


# ==========================================================
# FINDING SUMMARY
# ==========================================================

st.divider()

st.subheader("🔎 Finding Summary")

stats = report.get(
    "statistics",
    {}
)

st.write(
    f"""
**Total Issues:** {stats.get("total", 0)}

**Critical:** {stats.get("critical", 0)}

**High:** {stats.get("high", 0)}

**Medium:** {stats.get("medium", 0)}

**Low:** {stats.get("low", 0)}
"""
)


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.divider()

st.subheader("🛠️ Recommendations")

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

else:

    for index, rec in enumerate(
        recommendations,
        start=1
    ):

        if not isinstance(
            rec,
            dict
        ):
            continue

        issue = rec.get(
            "issue",
            "Unnamed Issue"
        )

        with st.expander(
            f"{index}. {issue}"
        ):

            st.write(
                "**Category:**",
                rec.get(
                    "category",
                    "N/A"
                )
            )

            st.write(
                "**Severity:**",
                rec.get(
                    "severity",
                    "N/A"
                )
            )

            st.success(
                rec.get(
                    "fix",
                    rec.get(
                        "recommendation",
                        "No fix available."
                    )
                )
            )


# ==========================================================
# PULL REQUEST SUMMARY
# ==========================================================

st.divider()

st.subheader("📝 Pull Request Summary")

pr = report.get(
    "pr_summary",
    {}
)

st.write(
    pr.get(
        "executive_summary",
        "No pull request summary available."
    )
)


# ==========================================================
# DOWNLOAD REPORTS
# ==========================================================

st.divider()

st.subheader("📥 Download Report")


# ----------------------------------------------------------
# JSON REPORT
# ----------------------------------------------------------

try:

    json_report = JSONExporter.export(
        report
    )

    st.download_button(
        label="⬇️ Download JSON Report",
        data=json_report,
        file_name="AI_Code_Review_Report.json",
        mime="application/json",
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Unable to generate JSON report: {e}"
    )


# ----------------------------------------------------------
# PDF REPORT
# ----------------------------------------------------------

try:

    pdf_report = PDFExporter.export(
        report
    )

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_report,
        file_name="AI_Code_Review_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Unable to generate PDF report: {e}"
    )