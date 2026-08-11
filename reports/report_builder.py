from datetime import datetime


class ReportBuilder:

    @staticmethod
    def build(state):

        # ==================================================
        # SYNTAX VALIDATION RESULT
        # ==================================================

        syntax_valid = state.get(
            "syntax_valid",
            False
        )

        syntax_message = state.get(
            "syntax_message",
            ""
        )

        language = state.get(
            "language",
            ""
        )

        # ==================================================
        # STOP REPORT GENERATION FOR INVALID SYNTAX
        # ==================================================

        if not syntax_valid:

            return {

                "metadata": {

                    "generated_at":
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                    "language":
                    language.upper()

                },

                "executive_summary":
                (
                    "Code analysis was stopped because "
                    "the submitted source code contains "
                    "syntax errors."
                ),

                "overall_score":
                None,

                "security_score":
                None,

                "maintainability_score":
                None,

                "grade":
                "N/A",

                "risk_level":
                "SYNTAX ERROR",

                "statistics": {

                    "total": 0,

                    "critical": 0,

                    "high": 0,

                    "medium": 0,

                    "low": 0

                },

                "chart_data": [

                    {
                        "Severity": "Critical",
                        "Count": 0
                    },

                    {
                        "Severity": "High",
                        "Count": 0
                    },

                    {
                        "Severity": "Medium",
                        "Count": 0
                    },

                    {
                        "Severity": "Low",
                        "Count": 0
                    }

                ],

                "syntax_validation": {

                    "valid": False,

                    "message":
                    syntax_message

                },

                "code_analysis": {},

                "security_analysis": {},

                "remediation": {},

                "pr_summary": {}

            }

        # ==================================================
        # NORMAL ANALYSIS
        # ==================================================

        code_analysis = state.get(
            "code_analysis",
            {}
        )

        security_analysis = state.get(
            "security_analysis",
            {}
        )

        remediation = state.get(
            "remediation",
            {}
        )

        pr_summary = state.get(
            "pr_summary",
            {}
        )

        # ==================================================
        # EXTRACT LLM FINDINGS
        # ==================================================

        code_llm = code_analysis.get(
            "llm",
            {}
        )

        security_llm = security_analysis.get(
            "llm",
            {}
        )

        code_findings = code_llm.get(
            "findings",
            []
        )

        security_findings = security_llm.get(
            "findings",
            []
        )

        # ==================================================
        # COMBINE FINDINGS
        # ==================================================

        all_findings = (
            code_findings +
            security_findings
        )

        # ==================================================
        # SEVERITY COUNTS
        # ==================================================

        stats = {

            "CRITICAL": 0,

            "HIGH": 0,

            "MEDIUM": 0,

            "LOW": 0

        }

        for finding in all_findings:

            if not isinstance(
                finding,
                dict
            ):
                continue

            severity = finding.get(
                "severity",
                "LOW"
            )

            if not isinstance(
                severity,
                str
            ):
                continue

            severity = severity.upper()

            if severity in stats:

                stats[severity] += 1

        total = sum(
            stats.values()
        )

        # ==================================================
        # SCORE CALCULATION
        # ==================================================

        overall_penalty = (

            stats["CRITICAL"] * 35 +

            stats["HIGH"] * 25 +

            stats["MEDIUM"] * 12 +

            stats["LOW"] * 4

        )

        security_penalty = (

            stats["CRITICAL"] * 40 +

            stats["HIGH"] * 30 +

            stats["MEDIUM"] * 15 +

            stats["LOW"] * 5

        )

        overall_score = max(
            0,
            100 - overall_penalty
        )

        security_score = max(
            0,
            100 - security_penalty
        )

        # ==================================================
        # MAINTAINABILITY SCORE
        # ==================================================

        quality_findings = len(
            code_findings
        )

        maintainability_penalty = (
            quality_findings * 10
        )

        maintainability_score = max(
            0,
            100 - maintainability_penalty
        )

        # ==================================================
        # GRADE
        # ==================================================

        if overall_score >= 90:

            grade = "A"

        elif overall_score >= 80:

            grade = "B"

        elif overall_score >= 70:

            grade = "C"

        elif overall_score >= 60:

            grade = "D"

        else:

            grade = "F"

        # ==================================================
        # RISK LEVEL
        # ==================================================

        if stats["CRITICAL"] > 0:

            risk = "CRITICAL"

        elif stats["HIGH"] > 0:

            risk = "HIGH"

        elif stats["MEDIUM"] > 0:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        # ==================================================
        # EXECUTIVE SUMMARY
        # ==================================================

        executive_summary = (

            f"The project was analyzed successfully. "

            f"{total} issue(s) were detected. "

            f"Overall Code Quality Score is "
            f"{overall_score}/100 "

            f"with a {risk} risk level."

        )

        # ==================================================
        # FINAL REPORT
        # ==================================================

        return {

            "metadata": {

                "generated_at":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

                "language":
                language.upper()

            },

            "executive_summary":
            executive_summary,

            "overall_score":
            overall_score,

            "security_score":
            security_score,

            "maintainability_score":
            maintainability_score,

            "grade":
            grade,

            "risk_level":
            risk,

            "statistics": {

                "total":
                total,

                "critical":
                stats["CRITICAL"],

                "high":
                stats["HIGH"],

                "medium":
                stats["MEDIUM"],

                "low":
                stats["LOW"]

            },

            "chart_data": [

                {
                    "Severity": "Critical",
                    "Count": stats["CRITICAL"]
                },

                {
                    "Severity": "High",
                    "Count": stats["HIGH"]
                },

                {
                    "Severity": "Medium",
                    "Count": stats["MEDIUM"]
                },

                {
                    "Severity": "Low",
                    "Count": stats["LOW"]
                }

            ],

            "syntax_validation": {

                "valid":
                syntax_valid,

                "message":
                syntax_message

            },

            "code_analysis":
            code_analysis,

            "security_analysis":
            security_analysis,

            "remediation":
            remediation,

            "pr_summary":
            pr_summary

        }