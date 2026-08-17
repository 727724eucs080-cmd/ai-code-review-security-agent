from typing import Dict, Any


class PRSummaryAgent:

    """
    Generates the final Pull Request summary.

    This agent consumes the authoritative, already-separated
    code-quality and security findings.

    It does not independently recalculate scoring.
    Authoritative scores are taken from the final report.
    """

    SEVERITY_ORDER = {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4
    }

    VALID_SEVERITIES = {
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    }

    INVALID_TITLES = {
        "not detected",
        "no vulnerability",
        "no vulnerabilities",
        "no issues",
        "no findings"
    }

    def generate(
        self,
        state
    ) -> Dict[str, Any]:

        # ---------------------------------
        # AUTHORITATIVE CODE QUALITY FINDINGS
        # ---------------------------------

        code_findings = state.get(
            "code_quality_findings",
            []
        )

        if not isinstance(
            code_findings,
            list
        ):
            code_findings = []

        # ---------------------------------
        # AUTHORITATIVE SECURITY FINDINGS
        # ---------------------------------

        security_findings = state.get(
            "security_findings",
            []
        )

        if not isinstance(
            security_findings,
            list
        ):
            security_findings = []

        # ---------------------------------
        # Validate Findings
        # ---------------------------------

        def valid_finding(finding):

            if not isinstance(
                finding,
                dict
            ):
                return False

            title = str(
                finding.get(
                    "title",
                    ""
                )
            ).strip()

            if not title:
                return False

            normalized_title = title.lower()

            if normalized_title in self.INVALID_TITLES:
                return False

            return True

        code_findings = [
            finding
            for finding in code_findings
            if valid_finding(finding)
        ]

        security_findings = [
            finding
            for finding in security_findings
            if valid_finding(finding)
        ]

        # ---------------------------------
        # Combine With Explicit Category
        # ---------------------------------

        all_findings = []

        for finding in code_findings:

            normalized_finding = dict(
                finding
            )

            normalized_finding["category"] = (
                "Code Quality"
            )

            all_findings.append(
                normalized_finding
            )

        for finding in security_findings:

            normalized_finding = dict(
                finding
            )

            normalized_finding["category"] = (
                "Security"
            )

            all_findings.append(
                normalized_finding
            )

        # ---------------------------------
        # Remove Duplicate Findings
        # ---------------------------------

        unique_findings = []

        seen = set()

        for finding in all_findings:

            title = str(
                finding.get(
                    "title",
                    ""
                )
            ).strip().lower()

            description = str(
                finding.get(
                    "description",
                    ""
                )
            ).strip().lower()

            line = str(
                finding.get(
                    "line",
                    ""
                )
            ).strip()

            category = str(
                finding.get(
                    "category",
                    ""
                )
            ).strip().lower()

            key = (
                title,
                description,
                line,
                category
            )

            if key in seen:
                continue

            seen.add(key)

            unique_findings.append(
                finding
            )

        all_findings = unique_findings

        # ---------------------------------
        # Severity Counters
        # ---------------------------------

        critical = 0
        high = 0
        medium = 0
        low = 0

        priority_actions = []

        # ---------------------------------
        # Process Findings
        # ---------------------------------

        for finding in all_findings:

            severity = str(
                finding.get(
                    "severity",
                    "LOW"
                )
            ).upper().strip()

            if severity not in self.VALID_SEVERITIES:
                severity = "LOW"

            if severity == "CRITICAL":
                critical += 1

            elif severity == "HIGH":
                high += 1

            elif severity == "MEDIUM":
                medium += 1

            else:
                low += 1

            priority_actions.append(
                {
                    "issue": str(
                        finding.get(
                            "title",
                            ""
                        )
                    ).strip(),

                    "severity": severity,

                    "action": str(
                        finding.get(
                            "recommendation",
                            ""
                        )
                    ).strip(),

                    "category": finding.get(
                        "category",
                        "Code Quality"
                    )
                }
            )

        # ---------------------------------
        # Sort Priority Actions
        # ---------------------------------

        priority_actions.sort(
            key=lambda item: self.SEVERITY_ORDER.get(
                item.get(
                    "severity",
                    "LOW"
                ),
                4
            )
        )

        # ---------------------------------
        # Remediation Recommendations
        # ---------------------------------

        remediation = state.get(
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

        recommendation_count = len(
            recommendations
        )

        # ---------------------------------
        # Use Existing Authoritative Scores
        # ---------------------------------

        final_report = state.get(
            "final_report",
            {}
        )

        if not isinstance(
            final_report,
            dict
        ):
            final_report = {}

        overall_score = final_report.get(
            "overall_score"
        )

        code_quality_score = final_report.get(
            "code_quality_score"
        )

        security_score = final_report.get(
            "security_score"
        )

        grade = final_report.get(
            "grade"
        )

        risk_level = final_report.get(
            "risk_level"
        )

        # ---------------------------------
        # Fallback Risk Calculation
        # ---------------------------------

        if not risk_level:

            if critical > 0:
                risk_level = "CRITICAL"

            elif high > 0:
                risk_level = "HIGH"

            elif medium > 0:
                risk_level = "MEDIUM"

            elif low > 0:
                risk_level = "LOW"

            else:
                risk_level = "NONE"

        # ---------------------------------
        # Fallback Score
        # ---------------------------------

        if overall_score is None:
            overall_score = 100

        # ---------------------------------
        # Executive Summary
        # ---------------------------------

        total_findings = len(
            all_findings
        )

        if total_findings == 0:

            summary = (
                "Code review completed successfully. "
                "No code quality or security issues "
                "were identified."
            )

        else:

            summary = (
                f"Code review identified "
                f"{total_findings} issue(s). "
                f"Risk level is {risk_level}. "
                f"{recommendation_count} remediation "
                "action(s) are suggested."
            )

        # ---------------------------------
        # Final PR Summary
        # ---------------------------------

        return {

            "executive_summary":
            summary,

            "impact_analysis":
            {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },

            "risk_level":
            risk_level,

            "overall_score":
            overall_score,

            "code_quality_score":
            code_quality_score,

            "security_score":
            security_score,

            "grade":
            grade,

            "required_actions":
            priority_actions,

            "recommendation_count":
            recommendation_count
        }


pr_summary_agent = PRSummaryAgent()