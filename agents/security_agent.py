import json

from tools.gemini_tool import GeminiTool
from tools.bandit_tool import BanditTool
from tools.semgrep_tool import SemgrepTool


class SecurityAgent:

    @staticmethod
    def _normalize_finding(finding):
        if not isinstance(finding, dict):
            return None

        extra = finding.get("extra", {})

        if not isinstance(extra, dict):
            extra = {}

        metadata = extra.get("metadata", {})

        if not isinstance(metadata, dict):
            metadata = {}

        # --------------------------------------------------
        # SEVERITY
        # --------------------------------------------------

        severity = (
            finding.get("severity")
            or finding.get("issue_severity")
            or extra.get("severity")
            or metadata.get("severity")
            or "LOW"
        )

        severity = str(
            severity
        ).upper().strip()

        if severity not in {
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        }:
            severity = "LOW"

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = (
            finding.get("title")
            or finding.get("test_name")
            or finding.get("check_name")
            or extra.get("message")
            or finding.get("issue_text")
            or "Security Finding"
        )

        # --------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------

        description = (
            finding.get("description")
            or finding.get("issue_text")
            or extra.get("message")
            or finding.get("message")
            or ""
        )

        # --------------------------------------------------
        # RECOMMENDATION
        # --------------------------------------------------

        recommendation = (
            finding.get("recommendation")
            or extra.get("recommendation")
            or ""
        )

        # --------------------------------------------------
        # LINE
        # --------------------------------------------------

        line = (
            finding.get("line")
            or finding.get("start_line")
            or finding.get("line_number")
            or 0
        )

        # --------------------------------------------------
        # RULE ID
        # --------------------------------------------------

        rule_id = (
            finding.get("test_id")
            or finding.get("check_id")
            or finding.get("rule_id")
            or finding.get("check_name")
            or ""
        )

        # --------------------------------------------------
        # CWE
        # --------------------------------------------------

        cwe = (
            finding.get("cwe")
            or extra.get("cwe")
            or metadata.get("cwe")
            or ""
        )

        if isinstance(cwe, dict):

            cwe_id = cwe.get(
                "id",
                ""
            )

            cwe_name = cwe.get(
                "name",
                ""
            )

            if cwe_id and cwe_name:
                cwe = f"{cwe_id}: {cwe_name}"

            elif cwe_id:
                cwe = str(cwe_id)

            elif cwe_name:
                cwe = str(cwe_name)

            else:
                cwe = ""

        # --------------------------------------------------
        # OWASP
        # --------------------------------------------------

        owasp = (
            finding.get("owasp")
            or extra.get("owasp")
            or metadata.get("owasp")
            or ""
        )

        return {
            "title": str(title).strip(),
            "severity": severity,
            "description": str(description).strip(),
            "recommendation": str(
                recommendation
            ).strip(),
            "line": line,
            "rule_id": str(rule_id).strip(),
            "cwe": cwe,
            "owasp": owasp,
            "category": "Security"
        }

    @staticmethod
    def _finding_key(finding):
        """
        Create a stable identity for a security finding.

        Scanner rule + location is preferred because two
        different security findings may have similar text.
        """

        if not isinstance(finding, dict):
            return None

        rule_id = str(
            finding.get(
                "rule_id",
                ""
            )
        ).lower().strip()

        line = str(
            finding.get(
                "line",
                ""
            )
        ).strip()

        title = str(
            finding.get(
                "title",
                ""
            )
        ).lower().strip()

        if rule_id:
            return (
                rule_id,
                line
            )

        return (
            title,
            line
        )

    @classmethod
    def _deduplicate_findings(
        cls,
        findings
    ):
        """
        Remove duplicate security findings while preserving
        the first scanner-backed occurrence.
        """

        unique = []
        seen = set()

        for finding in findings:

            normalized = cls._normalize_finding(
                finding
            )

            if normalized is None:
                continue

            key = cls._finding_key(
                normalized
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                normalized
            )

        return unique

    @staticmethod
    def _build_python_prompt(
        code,
        findings
    ):
        return f"""
You are a senior Python application security engineer.

Review ONLY the security findings detected by the
static security scanner.

Do not invent additional vulnerabilities.

Do not duplicate findings.

Do not change the vulnerability type.

Do not downgrade or upgrade the scanner severity.

Preserve the supplied severity exactly.

For every supplied finding, explain:

1. What the vulnerability is.
2. Why the specific code is risky.
3. A practical remediation.

Return ONLY valid JSON.

Required format:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "specific explanation",
            "recommendation": "specific fix",
            "line": 0,
            "rule_id": "scanner rule",
            "category": "Security"
        }}
    ]
}}

Python Code:
{code}

Scanner Findings:
{json.dumps(
    findings,
    ensure_ascii=False
)}
"""

    @staticmethod
    def _build_java_prompt(
        code,
        findings
    ):
        return f"""
You are a senior Java application security engineer.

Review ONLY the security findings detected by
the static security scanner.

Do not invent additional vulnerabilities.

Do not duplicate findings.

Do not change the vulnerability type.

Do not downgrade or upgrade the scanner severity.

Preserve the supplied severity exactly.

For every supplied finding, explain:

1. What the vulnerability is.
2. Why the specific code is risky.
3. A practical remediation.

Return ONLY valid JSON.

Required format:

{{
    "summary": "short security summary",
    "findings": [
        {{
            "title": "vulnerability title",
            "severity": "CRITICAL/HIGH/MEDIUM/LOW",
            "description": "specific explanation",
            "recommendation": "specific fix",
            "line": 0,
            "rule_id": "scanner rule",
            "category": "Security"
        }}
    ]
}}

Java Code:
{code}

Scanner Findings:
{json.dumps(
    findings,
    ensure_ascii=False
)}
"""

    @staticmethod
    def _schema():
        return {
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
                            },
                            "line": {
                                "type": "integer"
                            },
                            "rule_id": {
                                "type": "string"
                            },
                            "category": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "title",
                            "severity",
                            "description",
                            "recommendation",
                            "line",
                            "rule_id",
                            "category"
                        ]
                    }
                }
            },
            "required": [
                "summary",
                "findings"
            ]
        }

    @classmethod
    def _analyze_with_llm(
        cls,
        code,
        language,
        findings
    ):
        if not findings:
            return {
                "summary": (
                    "No security vulnerabilities "
                    "were detected by the static "
                    "security scanner."
                ),
                "findings": []
            }

        if language == "python":
            prompt = cls._build_python_prompt(
                code,
                findings
            )
        else:
            prompt = cls._build_java_prompt(
                code,
                findings
            )

        try:

            result = GeminiTool.generate_json(
                prompt,
                cls._schema()
            )

            if not isinstance(
                result,
                dict
            ):
                raise ValueError(
                    "Invalid LLM security response."
                )

            llm_findings = result.get(
                "findings",
                []
            )

            normalized_llm_findings = (
                cls._deduplicate_findings(
                    llm_findings
                )
            )

            scanner_keys = {
                cls._finding_key(
                    finding
                )
                for finding in findings
            }

            validated_findings = []

            for finding in normalized_llm_findings:

                key = cls._finding_key(
                    finding
                )

                if key in scanner_keys:

                    scanner_finding = next(
                        (
                            scanner_item
                            for scanner_item in findings
                            if cls._finding_key(
                                scanner_item
                            ) == key
                        ),
                        None
                    )

                    if scanner_finding:

                        finding["severity"] = (
                            scanner_finding[
                                "severity"
                            ]
                        )

                        finding["rule_id"] = (
                            scanner_finding[
                                "rule_id"
                            ]
                        )

                        finding["line"] = (
                            scanner_finding[
                                "line"
                            ]
                        )

                        finding["category"] = (
                            "Security"
                        )

                    validated_findings.append(
                        finding
                    )

            return {
                "summary": str(
                    result.get(
                        "summary",
                        ""
                    )
                ),
                "findings": validated_findings
            }

        except Exception:

            return {
                "summary": (
                    "Security vulnerabilities were "
                    "detected by the static scanner."
                ),
                "findings": findings
            }

    @classmethod
    def analyze(
        cls,
        code: str,
        language: str
    ):

        language = (
            language
            .lower()
            .strip()
        )

        # ==================================================
        # PYTHON SECURITY ANALYSIS
        # ==================================================

        if language == "python":

            bandit_report = BanditTool.scan(
                code
            )

            raw_findings = bandit_report.get(
                "results",
                []
            )

            security_findings = (
                cls._deduplicate_findings(
                    raw_findings
                )
            )

            llm_result = cls._analyze_with_llm(
                code,
                language,
                security_findings
            )

            return {
                "bandit": bandit_report,
                "llm": llm_result,
                "findings": security_findings
            }

        # ==================================================
        # JAVA SECURITY ANALYSIS
        # ==================================================

        if language == "java":

            semgrep_report = SemgrepTool.scan(
                code,
                language
            )

            raw_findings = semgrep_report.get(
                "results",
                []
            )

            security_findings = (
                cls._deduplicate_findings(
                    raw_findings
                )
            )

            llm_result = cls._analyze_with_llm(
                code,
                language,
                security_findings
            )

            return {
                "semgrep": semgrep_report,
                "llm": llm_result,
                "findings": security_findings
            }

        # ==================================================
        # UNSUPPORTED LANGUAGE
        # ==================================================

        return {
            "static": {
                "findings": []
            },
            "llm": {
                "summary": (
                    "Unsupported programming language."
                ),
                "findings": []
            },
            "findings": []
        }


security_agent = SecurityAgent()