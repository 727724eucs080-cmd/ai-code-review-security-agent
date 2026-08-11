from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


class PDFExporter:


    @staticmethod
    def export(report):


        buffer = BytesIO()


        document = SimpleDocTemplate(
            buffer
        )


        styles = getSampleStyleSheet()


        story = []



        # --------------------------------
        # Title
        # --------------------------------

        story.append(

            Paragraph(

                "AI Code Review & Security Analysis Report",

                styles["Title"]

            )

        )


        story.append(
            Spacer(1,20)
        )



        # --------------------------------
        # Metadata
        # --------------------------------

        metadata = report["metadata"]


        story.append(

            Paragraph(

                f"""
                <b>Language:</b> {metadata['language']}<br/>
                <b>Generated:</b> {metadata['generated_at']}<br/>
                <b>Risk Level:</b> {report['risk_level']}<br/>
                <b>Grade:</b> {report['grade']}<br/>
                <b>Overall Score:</b> {report['overall_score']}%<br/>
                <b>Security Score:</b> {report['security_score']}%
                """,

                styles["Normal"]

            )

        )



        story.append(
            Spacer(1,20)
        )



        # --------------------------------
        # Syntax
        # --------------------------------

        story.append(

            Paragraph(

                "Syntax Validation",

                styles["Heading2"]

            )

        )


        story.append(

            Paragraph(

                report["syntax_validation"]["message"],

                styles["Normal"]

            )

        )



        story.append(
            Spacer(1,20)
        )



        # --------------------------------
        # Code Findings
        # --------------------------------

        story.append(

            Paragraph(

                "Code Quality Findings",

                styles["Heading2"]

            )

        )


        code_findings = (

            report["code_analysis"]

            .get("llm", {})

            .get("findings", [])

        )


        for index, finding in enumerate(
            code_findings,
            start=1
        ):


            story.append(

                Paragraph(

                    f"""
                    <b>{index}. {finding.get('title')}</b><br/>
                    Severity: {finding.get('severity')}<br/>
                    Description:
                    {finding.get('description')}<br/>
                    Recommendation:
                    {finding.get('recommendation')}
                    """,

                    styles["Normal"]

                )

            )


            story.append(
                Spacer(1,12)
            )



        # --------------------------------
        # Security Findings
        # --------------------------------

        story.append(

            Paragraph(

                "Security Findings",

                styles["Heading2"]

            )

        )


        security_findings = (

            report["security_analysis"]

            .get("llm", {})

            .get("findings", [])

        )


        for index, finding in enumerate(
            security_findings,
            start=1
        ):


            story.append(

                Paragraph(

                    f"""
                    <b>{index}. {finding.get('title')}</b><br/>
                    Severity: {finding.get('severity')}<br/>
                    Description:
                    {finding.get('description')}<br/>
                    Recommendation:
                    {finding.get('recommendation')}
                    """,

                    styles["Normal"]

                )

            )


            story.append(
                Spacer(1,12)
            )



        # --------------------------------
        # Remediation
        # --------------------------------

        story.append(

            Paragraph(

                "Remediation Recommendations",

                styles["Heading2"]

            )

        )


        recommendations = (

            report["remediation"]

            .get("recommendations", [])

        )


        for index, rec in enumerate(
            recommendations,
            start=1
        ):


            story.append(

                Paragraph(

                    f"""
                    <b>{index}. {rec.get('issue')}</b><br/>
                    Category:
                    {rec.get('category','')}<br/>
                    Severity:
                    {rec.get('severity')}<br/>
                    Fix:
                    {rec.get('fix',rec.get('recommendation',''))}
                    """,

                    styles["Normal"]

                )

            )


            story.append(
                Spacer(1,12)
            )



        # --------------------------------
        # PR Summary
        # --------------------------------

        story.append(

            Paragraph(

                "Pull Request Summary",

                styles["Heading2"]

            )

        )


        story.append(

            Paragraph(

                report["pr_summary"]["executive_summary"],

                styles["Normal"]

            )

        )



        document.build(
            story
        )


        pdf = buffer.getvalue()


        buffer.close()


        return pdf