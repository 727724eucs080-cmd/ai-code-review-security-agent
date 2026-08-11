from typing import Dict, Any


class RemediationAgent:

    """
    Generates actionable remediation guidance
    from code quality and security findings.
    """


    def generate(
        self,
        state
    ) -> Dict[str, Any]:


        recommendations = []


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
    if "not detected" not in finding.get("title", "").lower()
]


        for finding in code_findings:


            severity = finding.get(
                "severity",
                "LOW"
            ).upper()


            if severity not in [
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ]:

                continue



            recommendations.append({

                "issue":

                finding.get(
                    "title",
                    ""
                ),


                "severity":

                severity,


                "category":

                "Code Quality",


                "fix":

                finding.get(
                    "recommendation",
                    ""
                ),


                "developer_action":

                (
                    "Refactor the code according "
                    "to the recommended practice."
                )

            })



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
    if "not detected" not in finding.get("title", "").lower()
    and "no vulnerability" not in finding.get("title", "").lower()
]

        for finding in security_findings:


            severity = finding.get(
                "severity",
                "LOW"
            ).upper()



            if severity not in [
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ]:

                continue



            recommendations.append({

                "issue":

                finding.get(
                    "title",
                    ""
                ),


                "severity":

                severity,


                "category":

                "Security",


                "fix":

                finding.get(
                    "recommendation",
                    ""
                ),


                "developer_action":

                (
                    "Apply secure coding practices "
                    "and validate the fix."
                )

            })



        # ---------------------------------
        # Remove Duplicate Recommendations
        # ---------------------------------

        unique_recommendations = []

        seen = set()


        for item in recommendations:


            key = item["issue"].lower().strip()


            if key not in seen:

                seen.add(key)

                unique_recommendations.append(item)



        recommendations = unique_recommendations



        # ---------------------------------
        # Priority Sorting
        # ---------------------------------

        priority_order = {

            "CRITICAL": 0,

            "HIGH": 1,

            "MEDIUM": 2,

            "LOW": 3

        }


        recommendations.sort(

            key=lambda item:

            priority_order.get(

                item["severity"],

                3

            )

        )



        # ---------------------------------
        # Summary
        # ---------------------------------

        if len(recommendations) == 0:


            summary = (

                "No remediation actions required."

            )


        else:


            summary = (

                f"{len(recommendations)} "

                "remediation action(s) generated "

                "based on detected findings."

            )



        return {


            "summary":

            summary,


            "total_actions":

            len(recommendations),


            "recommendations":

            recommendations

        }



remediation_agent = RemediationAgent()