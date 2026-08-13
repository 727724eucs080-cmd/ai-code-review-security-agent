import json

from tools.gemini_tool import GeminiTool
from tools.bandit_tool import BanditTool
from tools.semgrep_tool import SemgrepTool


class SecurityAgent:

    def analyze(self, code: str, language: str):

        language = language.lower().strip()

        if language == "python":

            bandit_report = BanditTool.scan(code)

            findings = bandit_report.get(
                "results",
                []
            )

            if not findings:

                return {
                    "bandit": bandit_report,
                    "llm": {
                        "summary": (
                            "No security vulnerabilities were "
                            "detected by Bandit."
                        ),
                        "findings": []
                    }
                }

            prompt = f"""
You are a senior Python application security engineer.

Analyze the security findings produced by Bandit.

Do not invent vulnerabilities.

Use only the supplied Bandit findings and Python code
as evidence.

Explain the findings clearly and determine their practical
security impact.

Return ONLY valid JSON in exactly this format:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "specific explanation",
            "recommendation": "specific fix"
        }}
    ]
}}

Python Code:
{code}

Bandit Findings:
{json.dumps(findings, ensure_ascii=False)}
"""

            schema = {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string"
                    },
                    "findings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string"
                                },
                                "severity": {
                                    "type": "string"
                                },
                                "description": {
                                    "type": "string"
                                },
                                "recommendation": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "title",
                                "severity",
                                "description",
                                "recommendation"
                            ]
                        }
                    }
                },
                "required": [
                    "summary",
                    "findings"
                ]
            }

            try:

                llm = GeminiTool.generate_json(
                    prompt,
                    schema
                )

            except Exception:

                llm = {
                    "summary": (
                        "Bandit detected security findings, "
                        "but AI analysis could not be completed."
                    ),
                    "findings": []
                }

            return {
                "bandit": bandit_report,
                "llm": llm
            }

        if language == "java":

            semgrep_report = SemgrepTool.scan(
                code,
                language
            )

            findings = semgrep_report.get(
                "results",
                []
            )

            if not findings:

                return {
                    "semgrep": semgrep_report,
                    "llm": {
                        "summary": (
                            "No security vulnerabilities were "
                            "detected by Semgrep."
                        ),
                        "findings": []
                    }
                }

            prompt = f"""
You are a senior Java application security engineer.

Analyze the security findings detected by Semgrep.

Do not invent vulnerabilities.

Use the supplied Semgrep findings as the primary
security evidence.

For each finding:

1. Explain what the vulnerability means.
2. Explain why the specific code is risky.
3. Give a practical remediation.
4. Preserve the actual vulnerability type.
5. Do not create additional vulnerabilities that are
   not supported by the Semgrep findings.

Return ONLY valid JSON in exactly this format:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "specific explanation",
            "recommendation": "specific fix"
        }}
    ]
}}

Java Code:
{code}

Semgrep Findings:
{json.dumps(findings, ensure_ascii=False)}
"""

            schema = {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string"
                    },
                    "findings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string"
                                },
                                "severity": {
                                    "type": "string"
                                },
                                "description": {
                                    "type": "string"
                                },
                                "recommendation": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "title",
                                "severity",
                                "description",
                                "recommendation"
                            ]
                        }
                    }
                },
                "required": [
                    "summary",
                    "findings"
                ]
            }

            try:

                llm = GeminiTool.generate_json(
                    prompt,
                    schema
                )

            except Exception:

                llm = {
                    "summary": (
                        "Semgrep detected security findings, "
                        "but AI analysis could not be completed."
                    ),
                    "findings": []
                }

            return {
                "semgrep": semgrep_report,
                "llm": llm
            }

        return {
            "static": {
                "findings": []
            },
            "llm": {
                "summary": (
                    "Unsupported programming language."
                ),
                "findings": []
            }
        }


security_agent = SecurityAgent()