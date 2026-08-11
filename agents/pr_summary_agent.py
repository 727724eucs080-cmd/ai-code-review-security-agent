from typing import Dict, Any


class PRSummaryAgent:

    """
    Generates the final Pull Request summary
    for developers.
    """

    def generate(
        self,
        state
    ) -> Dict[str, Any]:

        # ---------------------------------
        # Code Quality Findings
        # ---------------------------------

        code_findings = (
            state["code_analysis"]
            .get("llm", {})
            .get("findings", [])
        )

        code_findings = [
            finding
            for finding in code_findings
            if "not detected" not in
            finding.get("title", "").lower()
            and "no vulnerability" not in
            finding.get("title", "").lower()
        ]


        # ---------------------------------
        # Security Findings
        # ---------------------------------

        security_findings = (
            state["security_analysis"]
            .get("llm", {})
            .get("findings", [])
        )

        security_findings = [
            finding
            for finding in security_findings
            if "not detected" not in
            finding.get("title", "").lower()
            and "no vulnerability" not in
            finding.get("title", "").lower()
        ]


        # ---------------------------------
        # Combine Findings
        # ---------------------------------

        all_findings = (
            code_findings +
            security_findings
        )


        # ---------------------------------
        # Remove Duplicate Findings
        # ---------------------------------

        unique_findings = []

        seen_titles = set()

        for finding in all_findings:

            title = (
                finding
                .get("title", "")
                .strip()
                .lower()
            )

            if not title:
                continue

            if title in seen_titles:
                continue

            seen_titles.add(title)

            unique_findings.append(finding)


        all_findings = unique_findings


        # ---------------------------------
        # Remediation Recommendations
        # ---------------------------------

        recommendations = (
            state["remediation"]
            .get(
                "recommendations",
                []
            )
        )


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

            severity = (
                finding
                .get(
                    "severity",
                    "LOW"
                )
                .upper()
            )


            if severity == "CRITICAL":

                critical += 1

            elif severity == "HIGH":

                high += 1

            elif severity == "MEDIUM":

                medium += 1

            else:

                low += 1


            priority_actions.append({

                "issue":
                finding.get(
                    "title",
                    ""
                ),

                "severity":
                severity,

                "action":
                finding.get(
                    "recommendation",
                    ""
                )

            })


        # ---------------------------------
        # Calculate Score
        # ---------------------------------

        score = max(
            0,
            100 -
            (
                critical * 25 +
                high * 15 +
                medium * 8 +
                low * 3
            )
        )


        # ---------------------------------
        # Determine Risk
        # ---------------------------------

        if critical > 0:

            risk = "CRITICAL"

        elif high > 0:

            risk = "HIGH"

        elif medium > 0:

            risk = "MEDIUM"

        else:

            risk = "LOW"


        # ---------------------------------
        # Executive Summary
        # ---------------------------------

        summary = (

            f"Code review identified "
            f"{len(all_findings)} issue(s). "

            f"Risk level is {risk}. "

            f"{len(recommendations)} remediation "
            "actions are suggested."

        )


        # ---------------------------------
        # Final PR Summary
        # ---------------------------------

        return {

            "executive_summary":
            summary,

            "impact_analysis":
            {

                "critical":
                critical,

                "high":
                high,

                "medium":
                medium,

                "low":
                low

            },

            "risk_level":
            risk,

            "overall_score":
            score,

            "required_actions":
            priority_actions,

            "recommendation_count":
            len(recommendations)

        }


pr_summary_agent = PRSummaryAgent()

