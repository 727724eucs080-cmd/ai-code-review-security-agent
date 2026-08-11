import json
from datetime import datetime
from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer


def generate_summary(findings):

    summary = {

        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "TOTAL": len(findings)

    }

    for finding in findings:

        severity = finding.severity

        if severity in summary:

            summary[severity] += 1

    return summary


def generate_json_report(file_name, findings, severity_count):

    report = {

    "report_info": {

        "project": "AI Code Review & Security Analysis Agent",

        "generated_on": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        "file_name": file_name

    },

    "summary": {

        "total_findings": len(findings),

        "critical": severity_count["CRITICAL"],

        "high": severity_count["HIGH"],

        "medium": severity_count["MEDIUM"],

        "low": severity_count["LOW"]

    },

    "findings": []

}
    for finding in findings:

        report["findings"].append({

    "id": len(report["findings"]) + 1,

    "title": finding.title,

    "severity": finding.severity,

    "line_number": finding.line_number,

    "description": finding.description,

    "recommendation": finding.recommendation

})

    return json.dumps(

        report,

        indent=4

    )


def generate_pdf_report(file_name, findings, severity_count):

    buffer = BytesIO()

    document = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(

        Paragraph(

            "<b>AI Code Review & Security Analysis Report</b>",

            styles["Title"]

        )

    )

    story.append(

        Spacer(1, 20)

    )

    story.append(

        Paragraph(

            f"<b>File :</b> {file_name}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"<b>Total Findings :</b> {len(findings)}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"<b>Critical :</b> {severity_count['CRITICAL']}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"<b>High :</b> {severity_count['HIGH']}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"<b>Medium :</b> {severity_count['MEDIUM']}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"<b>Low :</b> {severity_count['LOW']}",

            styles["Normal"]

        )

    )

    story.append(

        Spacer(1, 20)

    )

    story.append(

        Paragraph(

            "<b>Findings</b>",

            styles["Heading2"]

        )

    )

    story.append(

        Spacer(1, 10)

    )

    for index, finding in enumerate(findings, start=1):

        story.append(

            Paragraph(

                f"<b>{index}. {finding.title}</b>",

                styles["Heading3"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Severity :</b> {finding.severity}",

                styles["Normal"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Description :</b> {finding.description}",

                styles["Normal"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Recommendation :</b> {finding.recommendation}",

                styles["Normal"]

            )

        )

        story.append(

            Spacer(1, 12)

        )

    document.build(

        story

    )

    pdf = buffer.getvalue()

    buffer.close()

    return pdf