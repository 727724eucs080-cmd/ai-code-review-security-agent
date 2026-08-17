from typing import Dict, Any


class RemediationAgent:

    """
    Generates actionable remediation guidance from the
    authoritative, already-separated code-quality and
    security findings.
    """

    SEVERITY_ORDER = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    VALID_SEVERITIES = {
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    }

    def generate(
        self,
        state
    ) -> Dict[str, Any]:

        recommendations = []

        # ==================================================
        # CODE QUALITY FINDINGS
        # ==================================================

        code_findings = state.get(
            "code_quality_findings",
            []
        )

        if not isinstance(
            code_findings,
            list
        ):
            code_findings = []

        for finding in code_findings:

            if not isinstance(
                finding,
                dict
            ):
                continue

            recommendation = self.build_recommendation(
                finding,
                "Code Quality"
            )

            if recommendation is not None:
                recommendations.append(
                    recommendation
                )

        # ==================================================
        # SECURITY FINDINGS
        # ==================================================

        security_findings = state.get(
            "security_findings",
            []
        )

        if not isinstance(
            security_findings,
            list
        ):
            security_findings = []

        for finding in security_findings:

            if not isinstance(
                finding,
                dict
            ):
                continue

            recommendation = self.build_recommendation(
                finding,
                "Security"
            )

            if recommendation is not None:
                recommendations.append(
                    recommendation
                )

        # ==================================================
        # REMOVE DUPLICATE RECOMMENDATIONS
        # ==================================================

        unique_recommendations = []

        seen = set()

        for recommendation in recommendations:

            key = self.recommendation_key(
                recommendation
            )

            if key in seen:
                continue

            seen.add(key)

            unique_recommendations.append(
                recommendation
            )

        # ==================================================
        # SORT BY SEVERITY
        # ==================================================

        unique_recommendations.sort(
            key=lambda item: self.SEVERITY_ORDER.get(
                item.get(
                    "severity",
                    "LOW"
                ),
                3
            )
        )

        recommendations = unique_recommendations

        # ==================================================
        # SUMMARY
        # ==================================================

        total_actions = len(
            recommendations
        )

        security_count = sum(
            1
            for recommendation in recommendations
            if recommendation.get(
                "category"
            ) == "Security"
        )

        code_quality_count = sum(
            1
            for recommendation in recommendations
            if recommendation.get(
                "category"
            ) == "Code Quality"
        )

        if total_actions == 0:

            summary = (
                "No remediation actions required."
            )

        else:

            summary = (
                f"{total_actions} remediation action(s) "
                f"generated: "
                f"{security_count} security and "
                f"{code_quality_count} code-quality."
            )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {
            "summary": summary,
            "total_actions": total_actions,
            "recommendations": recommendations
        }

    # ==================================================
    # BUILD REMEDIATION
    # ==================================================

    def build_recommendation(
        self,
        finding,
        category
    ):

        title = str(
            finding.get(
                "title",
                ""
            )
        ).strip()

        description = str(
            finding.get(
                "description",
                ""
            )
        ).strip()

        recommendation = str(
            finding.get(
                "recommendation",
                ""
            )
        ).strip()

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper().strip()

        if not title:
            return None

        if severity not in self.VALID_SEVERITIES:
            severity = "LOW"

        # ==================================================
        # USE FINDING-SPECIFIC RECOMMENDATION
        # ==================================================

        if not recommendation:

            if category == "Security":

                recommendation = (
                    "Review this security vulnerability and "
                    "apply an appropriate secure implementation "
                    "based on the identified vulnerability type."
                )

            else:

                recommendation = (
                    "Refactor the identified code according "
                    "to the recommended code-quality practice "
                    "and validate the resulting implementation."
                )

        # ==================================================
        # DEVELOPER ACTION
        # ==================================================

        if category == "Security":

            developer_action = (
                "Apply the recommended security fix and "
                "rerun the security analysis to verify that "
                "the vulnerability has been resolved."
            )

        else:

            developer_action = (
                "Apply the recommended code-quality change "
                "and rerun the code-quality analysis."
            )

        # ==================================================
        # FINAL RECOMMENDATION
        # ==================================================

        return {
            "issue": title,
            "severity": severity,
            "priority": severity,
            "category": category,
            "fix": recommendation,
            "developer_action": developer_action,
            "description": description
        }

    # ==================================================
    # REMEDIATION KEY
    # ==================================================

    def recommendation_key(
        self,
        recommendation
    ):

        issue = str(
            recommendation.get(
                "issue",
                ""
            )
        ).strip().lower()

        category = str(
            recommendation.get(
                "category",
                ""
            )
        ).strip().lower()

        return (
            category,
            issue
        )


remediation_agent = RemediationAgent()