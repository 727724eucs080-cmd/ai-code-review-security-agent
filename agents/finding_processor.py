from typing import Any, Dict, List, Tuple

from models.finding import Finding


class FindingProcessor:
    """
    Central processor for all findings produced by the analysis agents.

    Responsibilities:
    1. Extract findings from agent outputs.
    2. Normalize dictionaries into the unified Finding model.
    3. Preserve scanner security metadata.
    4. Separate Code Quality and Security findings.
    5. Remove invalid findings.
    6. Deduplicate findings.
    7. Return one authoritative finding collection.
    """

    VALID_SEVERITIES = {
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    }

    SECURITY_CATEGORIES = {
        "SECURITY",
        "VULNERABILITY",
        "SECURITY_VULNERABILITY",
        "SAST"
    }

    SECURITY_PATTERNS = (
        "sql injection",
        "command injection",
        "os command injection",
        "shell injection",
        "code injection",
        "arbitrary code execution",
        "remote code execution",
        "path traversal",
        "directory traversal",
        "unsafe deserialization",
        "insecure deserialization",
        "hardcoded password",
        "hardcoded credential",
        "hardcoded credentials",
        "hardcoded secret",
        "hardcoded api key",
        "hardcoded token",
        "weak authentication",
        "authentication bypass",
        "authorization bypass",
        "broken access control",
        "privilege escalation",
        "sensitive information exposure",
        "information disclosure",
        "cross-site scripting",
        "xss",
        "cross-site request forgery",
        "csrf",
        "server-side request forgery",
        "ssrf",
        "weak cryptography",
        "weak encryption",
        "insecure random",
        "eval(",
        "exec(",
        "os.system",
        "subprocess",
        "cwe-",
        "owasp"
    )

    # ==================================================
    # PUBLIC PROCESSING METHOD
    # ==================================================

    @classmethod
    def process(
        cls,
        code_analysis: Dict[str, Any],
        security_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:

        code_raw = cls._extract_code_findings(
            code_analysis
        )

        security_raw = cls._extract_security_findings(
            security_analysis
        )

        code_findings = cls._normalize_findings(
            code_raw,
            default_category="CODE_QUALITY",
            source="CODE_ANALYSIS_AGENT"
        )

        security_findings = cls._normalize_findings(
            security_raw,
            default_category="SECURITY",
            source="SECURITY_AGENT"
        )

        # --------------------------------------------------
        # Separate Code Quality and Security findings.
        # --------------------------------------------------

        separated_code = []
        moved_security = []

        for finding in code_findings:

            if cls._is_security_finding(
                finding
            ):
                finding.category = "SECURITY"
                moved_security.append(
                    finding
                )
            else:
                finding.category = "CODE_QUALITY"
                separated_code.append(
                    finding
                )

        security_findings.extend(
            moved_security
        )

        # Security Agent findings are authoritative
        # security findings.
        for finding in security_findings:
            finding.category = "SECURITY"

        # --------------------------------------------------
        # Deduplicate independently.
        # --------------------------------------------------

        separated_code = cls.deduplicate(
            separated_code
        )

        security_findings = cls.deduplicate(
            security_findings
        )

        all_findings = (
            separated_code +
            security_findings
        )

        return {
            "findings": all_findings,
            "code_quality_findings": separated_code,
            "security_findings": security_findings,
            "statistics": cls.statistics(
                all_findings
            )
        }

    # ==================================================
    # CODE FINDINGS EXTRACTION
    # ==================================================

    @classmethod
    def _extract_code_findings(
        cls,
        code_analysis: Dict[str, Any]
    ) -> List[Any]:

        if not isinstance(
            code_analysis,
            dict
        ):
            return []

        llm = code_analysis.get(
            "llm",
            {}
        )

        if isinstance(
            llm,
            dict
        ):
            findings = llm.get(
                "findings",
                []
            )

            if isinstance(
                findings,
                list
            ):
                return findings

        findings = code_analysis.get(
            "findings",
            []
        )

        if isinstance(
            findings,
            list
        ):
            return findings

        return []

    # ==================================================
    # SECURITY FINDINGS EXTRACTION
    # ==================================================

    @classmethod
    def _extract_security_findings(
        cls,
        security_analysis: Dict[str, Any]
    ) -> List[Any]:

        if not isinstance(
            security_analysis,
            dict
        ):
            return []

        # --------------------------------------------------
        # First try LLM findings.
        # --------------------------------------------------

        llm = security_analysis.get(
            "llm",
            {}
        )

        if isinstance(
            llm,
            dict
        ):
            llm_findings = llm.get(
                "findings",
                []
            )

            if (
                isinstance(
                    llm_findings,
                    list
                )
                and llm_findings
            ):
                return llm_findings

        # --------------------------------------------------
        # IMPORTANT:
        # If LLM findings are empty, use raw Bandit results.
        # Do NOT use the already-damaged generic findings.
        # --------------------------------------------------

        bandit = security_analysis.get(
            "bandit",
            {}
        )

        if isinstance(
            bandit,
            dict
        ):
            bandit_results = bandit.get(
                "results",
                []
            )

            if isinstance(
                bandit_results,
                list
            ):
                return cls._convert_bandit_findings(
                    bandit_results
                )

        # --------------------------------------------------
        # Backward-compatible fallback.
        # --------------------------------------------------

        findings = security_analysis.get(
            "findings",
            []
        )

        if isinstance(
            findings,
            list
        ):
            return findings

        return []

    # ==================================================
    # BANDIT NORMALIZATION
    # ==================================================

    @classmethod
    def _convert_bandit_findings(
        cls,
        results: List[Any]
    ) -> List[Dict[str, Any]]:

        converted = []

        if not isinstance(
            results,
            list
        ):
            return converted

        for result in results:

            if not isinstance(
                result,
                dict
            ):
                continue

            rule_id = str(
                result.get(
                    "test_id",
                    ""
                )
                or ""
            ).strip()

            if not rule_id:
                continue

            issue_text = str(
                result.get(
                    "issue_text",
                    ""
                )
                or ""
            ).strip()

            severity = str(
                result.get(
                    "issue_severity",
                    "LOW"
                )
                or "LOW"
            ).upper().strip()

            confidence = str(
                result.get(
                    "issue_confidence",
                    ""
                )
                or ""
            ).upper().strip()

            line = result.get(
                "line_number",
                0
            )

            code_snippet = str(
                result.get(
                    "code",
                    ""
                )
                or ""
            )

            cwe_data = result.get(
                "issue_cwe",
                {}
            )

            cwe = ""

            if isinstance(
                cwe_data,
                dict
            ):
                cwe_id = cwe_data.get(
                    "id"
                )

                if cwe_id:
                    cwe = f"CWE-{cwe_id}"

            more_info = result.get(
                "more_info",
                ""
            )

            title = cls._bandit_title(
                rule_id,
                issue_text
            )

            recommendation = cls._bandit_recommendation(
                rule_id
            )

            converted.append(
                {
                    "title": title,
                    "severity": severity,
                    "description": issue_text,
                    "recommendation": recommendation,
                    "line": line,
                    "rule_id": rule_id,
                    "cwe": cwe,
                    "owasp": "",
                    "category": "SECURITY",
                    "source": "SECURITY_AGENT",
                    "code_snippet": code_snippet,
                    "confidence": confidence,
                    "remediation_code": "",
                    "references": [
                        more_info
                    ] if more_info else []
                }
            )

        return converted

    # ==================================================
    # BANDIT TITLES
    # ==================================================

    @staticmethod
    def _bandit_title(
        rule_id: str,
        issue_text: str
    ) -> str:

        titles = {
            "B105": "Hardcoded Password",
            "B107": "Hardcoded Password",
            "B108": "Insecure Temporary File",
            "B307": "Unsafe eval() Usage",
            "B605": "Command Injection Risk",
            "B602": "Shell Injection Risk",
            "B603": "Subprocess Security Risk",
            "B604": "Function Execution Risk",
            "B608": "SQL Injection Risk"
        }

        if rule_id in titles:
            return titles[rule_id]

        if issue_text:
            return issue_text

        return f"Security Vulnerability ({rule_id})"

    # ==================================================
    # BANDIT RECOMMENDATIONS
    # ==================================================

    @staticmethod
    def _bandit_recommendation(
        rule_id: str
    ) -> str:

        recommendations = {
            "B105": (
                "Remove hardcoded passwords and use a secure "
                "secret management mechanism such as environment "
                "variables or a secrets manager."
            ),

            "B107": (
                "Do not hardcode passwords in source code. "
                "Use environment variables or a secure secrets manager."
            ),

            "B307": (
                "Avoid eval() on untrusted input. Use a safe "
                "alternative such as ast.literal_eval() when appropriate."
            ),

            "B605": (
                "Avoid executing user-controlled input through "
                "os.system(). Use a safe subprocess API with "
                "validated arguments instead."
            ),

            "B602": (
                "Avoid shell execution with untrusted input. "
                "Use subprocess with shell=False and validated arguments."
            ),

            "B603": (
                "Validate subprocess arguments and avoid passing "
                "untrusted input directly to process execution."
            ),

            "B604": (
                "Avoid dynamically executing untrusted functions "
                "or input. Use an allowlist of permitted operations."
            ),

            "B608": (
                "Use parameterized SQL queries or prepared statements "
                "instead of constructing SQL statements dynamically."
            )
        }

        return recommendations.get(
            rule_id,
            "Review the security finding and apply a secure coding practice."
        )

    # ==================================================
    # NORMALIZATION
    # ==================================================

    @classmethod
    def _normalize_findings(
        cls,
        findings: List[Any],
        default_category: str,
        source: str
    ) -> List[Finding]:

        normalized = []

        if not isinstance(
            findings,
            list
        ):
            return normalized

        for raw_finding in findings:

            if isinstance(
                raw_finding,
                Finding
            ):
                finding = raw_finding

            elif isinstance(
                raw_finding,
                dict
            ):
                finding = Finding.from_dict(
                    raw_finding
                )

            else:
                continue

            if finding is None:
                continue

            if default_category == "SECURITY":
                finding.category = "SECURITY"

            elif default_category == "CODE_QUALITY":
                finding.category = "CODE_QUALITY"

            if not finding.source:
                finding.source = source

            if not cls._valid_title(
                finding.title
            ):
                continue

            finding.severity = (
                str(
                    finding.severity or "LOW"
                )
                .upper()
                .strip()
            )

            if finding.severity not in cls.VALID_SEVERITIES:
                finding.severity = "LOW"

            normalized.append(
                finding
            )

        return normalized

    # ==================================================
    # TITLE VALIDATION
    # ==================================================

    @staticmethod
    def _valid_title(
        title: str
    ) -> bool:

        normalized = " ".join(
            str(
                title or ""
            )
            .lower()
            .split()
        )

        if not normalized:
            return False

        invalid_phrases = (
            "not detected",
            "no vulnerability",
            "no vulnerabilities",
            "no security issue",
            "no security issues",
            "no issues",
            "no findings",
            "no problems",
            "none detected"
        )

        return not any(
            phrase in normalized
            for phrase in invalid_phrases
        )

    # ==================================================
    # SECURITY CLASSIFICATION
    # ==================================================

    @classmethod
    def _is_security_finding(
        cls,
        finding: Finding
    ) -> bool:

        if finding.category == "SECURITY":
            return True

        category = str(
            finding.category or ""
        ).upper().strip()

        if category in cls.SECURITY_CATEGORIES:
            return True

        searchable_text = " ".join(
            [
                str(finding.title or ""),
                str(finding.description or ""),
                str(finding.recommendation or ""),
                str(finding.rule_id or ""),
                str(finding.cwe or ""),
                str(finding.owasp or "")
            ]
        ).lower()

        if finding.cwe:
            return True

        if finding.owasp:
            return True

        return any(
            pattern in searchable_text
            for pattern in cls.SECURITY_PATTERNS
        )

    # ==================================================
    # DEDUPLICATION
    # ==================================================

    @classmethod
    def deduplicate(
        cls,
        findings: List[Finding]
    ) -> List[Finding]:

        unique = []
        seen = set()

        for finding in findings:

            if not isinstance(
                finding,
                Finding
            ):
                continue

            key = finding.identity_key()

            if key in seen:
                continue

            seen.add(
                key
            )

            unique.append(
                finding
            )

        return unique

    # ==================================================
    # STATISTICS
    # ==================================================

    @classmethod
    def statistics(
        cls,
        findings: List[Finding]
    ) -> Dict[str, int]:

        statistics = {
            "total": 0,

            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,

            "code_quality": 0,
            "security": 0,

            "code_quality_critical": 0,
            "code_quality_high": 0,
            "code_quality_medium": 0,
            "code_quality_low": 0,

            "security_critical": 0,
            "security_high": 0,
            "security_medium": 0,
            "security_low": 0
        }

        for finding in findings:

            if not isinstance(
                finding,
                Finding
            ):
                continue

            severity = finding.severity
            category = finding.category

            statistics["total"] += 1

            if severity == "CRITICAL":
                statistics["critical"] += 1

            elif severity == "HIGH":
                statistics["high"] += 1

            elif severity == "MEDIUM":
                statistics["medium"] += 1

            elif severity == "LOW":
                statistics["low"] += 1

            if category == "CODE_QUALITY":

                statistics["code_quality"] += 1

                if severity == "CRITICAL":
                    statistics["code_quality_critical"] += 1

                elif severity == "HIGH":
                    statistics["code_quality_high"] += 1

                elif severity == "MEDIUM":
                    statistics["code_quality_medium"] += 1

                elif severity == "LOW":
                    statistics["code_quality_low"] += 1

            elif category == "SECURITY":

                statistics["security"] += 1

                if severity == "CRITICAL":
                    statistics["security_critical"] += 1

                elif severity == "HIGH":
                    statistics["security_high"] += 1

                elif severity == "MEDIUM":
                    statistics["security_medium"] += 1

                elif severity == "LOW":
                    statistics["security_low"] += 1

        return statistics

    # ==================================================
    # DICTIONARY CONVERSION
    # ==================================================

    @staticmethod
    def to_dicts(
        findings: List[Finding]
    ) -> List[Dict[str, Any]]:

        return [
            finding.to_dict()
            for finding in findings
            if isinstance(
                finding,
                Finding
            )
        ]

    # ==================================================
    # CATEGORY SPLIT
    # ==================================================

    @staticmethod
    def split(
        findings: List[Finding]
    ) -> Tuple[
        List[Finding],
        List[Finding]
    ]:

        code_quality = []
        security = []

        for finding in findings:

            if not isinstance(
                finding,
                Finding
            ):
                continue

            if finding.category == "SECURITY":
                security.append(
                    finding
                )
            else:
                code_quality.append(
                    finding
                )

        return (
            code_quality,
            security
        )


finding_processor = FindingProcessor()