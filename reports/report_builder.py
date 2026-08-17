from datetime import datetime


class ReportBuilder:

    # ==================================================
    # SEVERITY CONFIGURATION
    # ==================================================

    SEVERITY_WEIGHTS = {
        "CRITICAL": 30,
        "HIGH": 20,
        "MEDIUM": 10,
        "LOW": 5
    }

    SECURITY_PATTERNS = [
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
    ]

    # ==================================================
    # MAIN REPORT BUILDER
    # ==================================================

    @classmethod
    def build(cls, state):

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
        # INVALID SYNTAX
        # ==================================================

        if not syntax_valid:

            return cls.build_syntax_error_report(
                language,
                syntax_message
            )

        # ==================================================
        # GET EXISTING PROCESSED FINDINGS
        # ==================================================

        code_findings = state.get(
            "code_quality_findings",
            []
        )

        security_findings = state.get(
            "security_findings",
            []
        )

        # --------------------------------------------------
        # SAFETY CHECK
        # --------------------------------------------------

        if not isinstance(
            code_findings,
            list
        ):
            code_findings = []

        if not isinstance(
            security_findings,
            list
        ):
            security_findings = []

        # ==================================================
        # NORMALIZE PROCESSED FINDINGS
        # ==================================================

        code_findings = [
            cls.normalize_finding(
                finding
            )
            for finding in code_findings
        ]

        security_findings = [
            cls.normalize_finding(
                finding
            )
            for finding in security_findings
        ]

        code_findings = [
            finding
            for finding in code_findings
            if finding is not None
        ]

        security_findings = [
            finding
            for finding in security_findings
            if finding is not None
        ]

        # ==================================================
        # FINAL DEDUPLICATION
        # ==================================================

        code_findings = (
            cls.deduplicate_findings(
                code_findings
            )
        )

        security_findings = (
            cls.deduplicate_findings(
                security_findings
            )
        )

        # ==================================================
        # CODE QUALITY SCORE
        # ==================================================

        code_quality_score = cls.calculate_score(
            code_findings
        )

        # ==================================================
        # SECURITY SCORE
        # ==================================================

        security_score = cls.calculate_score(
            security_findings
        )

        # ==================================================
        # OVERALL SCORE
        # ==================================================

        overall_score = round(
            (
                code_quality_score +
                security_score
            ) / 2
        )

        # ==================================================
        # MAINTAINABILITY SCORE
        # ==================================================

        maintainability_score = (
            code_quality_score
        )

        # ==================================================
        # GRADE
        # ==================================================

        grade = cls.calculate_grade(
            overall_score
        )

        # ==================================================
        # SECURITY RISK
        # ==================================================

        risk_level = cls.calculate_risk_level(
            security_findings
        )

        # ==================================================
        # STATISTICS
        # ==================================================

        statistics = cls.calculate_statistics(
            code_findings,
            security_findings
        )

        # ==================================================
        # CHART DATA
        # ==================================================

        chart_data = [
            {
                "Severity": "Critical",
                "Count": statistics["critical"]
            },
            {
                "Severity": "High",
                "Count": statistics["high"]
            },
            {
                "Severity": "Medium",
                "Count": statistics["medium"]
            },
            {
                "Severity": "Low",
                "Count": statistics["low"]
            }
        ]

        # ==================================================
        # EXECUTIVE SUMMARY
        # ==================================================

        total_findings = statistics["total"]

        executive_summary = (
            f"The project was analyzed successfully. "
            f"{total_findings} issue(s) were detected. "
            f"Code Quality Score is "
            f"{code_quality_score}/100. "
            f"Security Score is "
            f"{security_score}/100. "
            f"Overall Score is "
            f"{overall_score}/100 "
            f"with a {risk_level} security risk level."
        )

        # ==================================================
        # GET ANALYSIS RESULTS
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

        if not isinstance(
            code_analysis,
            dict
        ):
            code_analysis = {}

        if not isinstance(
            security_analysis,
            dict
        ):
            security_analysis = {}

        if not isinstance(
            remediation,
            dict
        ):
            remediation = {}

        if not isinstance(
            pr_summary,
            dict
        ):
            pr_summary = {}

        # ==================================================
        # FINAL REPORT
        # ==================================================

        return {

            "metadata": {
                "generated_at": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "language": language.upper()
            },

            "executive_summary":
                executive_summary,

            "code_quality_score":
                code_quality_score,

            "security_score":
                security_score,

            "overall_score":
                overall_score,

            "maintainability_score":
                maintainability_score,

            "grade":
                grade,

            "risk_level":
                risk_level,

            "statistics":
                statistics,

            "chart_data":
                chart_data,

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

            "code_quality_findings":
                code_findings,

            "security_findings":
                security_findings,

            "remediation":
                remediation,

            "pr_summary":
                pr_summary
        }

    # ==================================================
    # SYNTAX ERROR REPORT
    # ==================================================

    @classmethod
    def build_syntax_error_report(
        cls,
        language,
        syntax_message
    ):

        return {

            "metadata": {
                "generated_at": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "language": language.upper()
            },

            "executive_summary": (
                "Code analysis was stopped because "
                "the submitted source code contains "
                "syntax errors."
            ),

            "code_quality_score": None,

            "security_score": None,

            "overall_score": None,

            "maintainability_score": None,

            "grade": "N/A",

            "risk_level": "SYNTAX ERROR",

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
                "message": syntax_message
            },

            "code_analysis": {},

            "security_analysis": {},

            "code_quality_findings": [],

            "security_findings": [],

            "remediation": {},

            "pr_summary": {}
        }

    # ==================================================
    # FINDING NORMALIZATION
    # ==================================================

    @classmethod
    def normalize_finding(cls, finding):

        if not isinstance(
            finding,
            dict
        ):
            return None

        title = str(
            finding.get(
                "title",
                "Unnamed Finding"
            )
        ).strip()

        severity = str(
            finding.get(
                "severity",
                "LOW"
            )
        ).upper().strip()

        if severity not in cls.SEVERITY_WEIGHTS:

            severity = "LOW"

        description = str(
            finding.get(
                "description",
                finding.get(
                    "message",
                    ""
                )
            )
        ).strip()

        recommendation = str(
            finding.get(
                "recommendation",
                finding.get(
                    "fix",
                    ""
                )
            )
        ).strip()

        normalized = {
            "title": title,
            "severity": severity,
            "description": description,
            "recommendation": recommendation
        }

        optional_fields = [
            "category",
            "line",
            "end_line",
            "rule_id",
            "cwe",
            "owasp",
            "path",
            "source",
            "code_snippet",
            "confidence",
            "remediation_code",
            "references"
        ]

        for field in optional_fields:

            if field in finding:

                normalized[field] = (
                    finding[field]
                )

        return normalized

    # ==================================================
    # SECURITY CLASSIFICATION
    # ==================================================

    @classmethod
    def is_security_finding(
        cls,
        finding
    ):

        if not isinstance(
            finding,
            dict
        ):
            return False

        searchable_text = " ".join(
            str(
                finding.get(
                    field,
                    ""
                )
            )
            for field in [
                "title",
                "description",
                "recommendation",
                "message",
                "category",
                "rule_id",
                "cwe",
                "owasp"
            ]
        ).lower()

        category = str(
            finding.get(
                "category",
                ""
            )
        ).lower().strip()

        if category in {
            "security",
            "vulnerability",
            "security vulnerability",
            "sast"
        }:
            return True

        if "cwe-" in searchable_text:
            return True

        if "owasp" in searchable_text:
            return True

        return any(
            pattern in searchable_text
            for pattern in cls.SECURITY_PATTERNS
        )

    # ==================================================
    # FINDING KEY
    # ==================================================

    @classmethod
    def finding_key(
        cls,
        finding
    ):

        title = " ".join(
            str(
                finding.get(
                    "title",
                    ""
                )
            ).lower().split()
        )

        line = finding.get(
            "line"
        )

        end_line = finding.get(
            "end_line"
        )

        rule_id = " ".join(
            str(
                finding.get(
                    "rule_id",
                    ""
                )
            ).lower().split()
        )

        if line is not None:

            return (
                title,
                str(line),
                str(end_line),
                rule_id
            )

        return (
            title,
            rule_id
        )

    # ==================================================
    # DEDUPLICATION
    # ==================================================

    @classmethod
    def deduplicate_findings(
        cls,
        findings
    ):

        unique = []

        seen = set()

        for finding in findings:

            normalized = cls.normalize_finding(
                finding
            )

            if normalized is None:
                continue

            key = cls.finding_key(
                normalized
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                normalized
            )

        return unique

    # ==================================================
    # SEPARATE CODE QUALITY / SECURITY
    # ==================================================

    @classmethod
    def separate_findings(
        cls,
        code_findings,
        security_findings
    ):

        final_code_findings = []

        final_security_findings = []

        for finding in code_findings:

            normalized = cls.normalize_finding(
                finding
            )

            if normalized is None:
                continue

            if cls.is_security_finding(
                normalized
            ):

                final_security_findings.append(
                    normalized
                )

            else:

                final_code_findings.append(
                    normalized
                )

        for finding in security_findings:

            normalized = cls.normalize_finding(
                finding
            )

            if normalized is None:
                continue

            final_security_findings.append(
                normalized
            )

        final_code_findings = (
            cls.deduplicate_findings(
                final_code_findings
            )
        )

        final_security_findings = (
            cls.deduplicate_findings(
                final_security_findings
            )
        )

        final_code_findings = [
            finding
            for finding in final_code_findings
            if not cls.is_security_finding(
                finding
            )
        ]

        return (
            final_code_findings,
            final_security_findings
        )

    # ==================================================
    # SCORE CALCULATION
    # ==================================================

    @classmethod
    def calculate_score(
        cls,
        findings
    ):

        if not findings:
            return 100

        penalty = 0

        for finding in findings:

            severity = str(
                finding.get(
                    "severity",
                    "LOW"
                )
            ).upper()

            penalty += cls.SEVERITY_WEIGHTS.get(
                severity,
                0
            )

        return max(
            0,
            100 - penalty
        )

    # ==================================================
    # GRADE
    # ==================================================

    @classmethod
    def calculate_grade(
        cls,
        score
    ):

        if score >= 90:
            return "A"

        if score >= 80:
            return "B"

        if score >= 70:
            return "C"

        if score >= 60:
            return "D"

        return "F"

    # ==================================================
    # SECURITY RISK LEVEL
    # ==================================================

    @classmethod
    def calculate_risk_level(
        cls,
        security_findings
    ):

        severities = {
            str(
                finding.get(
                    "severity",
                    "LOW"
                )
            ).upper()
            for finding in security_findings
        }

        if "CRITICAL" in severities:
            return "CRITICAL"

        if "HIGH" in severities:
            return "HIGH"

        if "MEDIUM" in severities:
            return "MEDIUM"

        if "LOW" in severities:
            return "LOW"

        return "NONE"

    # ==================================================
    # STATISTICS
    # ==================================================

    @classmethod
    def calculate_statistics(
        cls,
        code_findings,
        security_findings
    ):

        all_findings = (
            code_findings +
            security_findings
        )

        statistics = {
            "total": len(all_findings),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "code_quality": len(code_findings),
            "security": len(security_findings),
            "code_quality_critical": 0,
            "code_quality_high": 0,
            "code_quality_medium": 0,
            "code_quality_low": 0,
            "security_critical": 0,
            "security_high": 0,
            "security_medium": 0,
            "security_low": 0
        }

        for finding in code_findings:

            severity = str(
                finding.get(
                    "severity",
                    "LOW"
                )
            ).upper()

            if severity == "CRITICAL":
                statistics["critical"] += 1
                statistics["code_quality_critical"] += 1

            elif severity == "HIGH":
                statistics["high"] += 1
                statistics["code_quality_high"] += 1

            elif severity == "MEDIUM":
                statistics["medium"] += 1
                statistics["code_quality_medium"] += 1

            elif severity == "LOW":
                statistics["low"] += 1
                statistics["code_quality_low"] += 1

        for finding in security_findings:

            severity = str(
                finding.get(
                    "severity",
                    "LOW"
                )
            ).upper()

            if severity == "CRITICAL":
                statistics["critical"] += 1
                statistics["security_critical"] += 1

            elif severity == "HIGH":
                statistics["high"] += 1
                statistics["security_high"] += 1

            elif severity == "MEDIUM":
                statistics["medium"] += 1
                statistics["security_medium"] += 1

            elif severity == "LOW":
                statistics["low"] += 1
                statistics["security_low"] += 1

        return statistics


report_builder = ReportBuilder()