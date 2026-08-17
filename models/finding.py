from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Finding:
    """
    Unified representation of a code-quality or security finding.

    All analysis agents and downstream modules should use the
    same finding structure.
    """

    title: str
    severity: str
    category: str
    description: str
    recommendation: str

    line: int = 0
    end_line: int = 0

    rule_id: str = ""
    cwe: str = ""
    owasp: str = ""

    source: str = ""

    code_snippet: str = ""

    confidence: str = ""

    remediation_code: str = ""

    references: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # VALID VALUES
    # --------------------------------------------------

    VALID_SEVERITIES = {
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    }

    VALID_CATEGORIES = {
        "CODE_QUALITY",
        "SECURITY"
    }

    # --------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------

    def __post_init__(self):
        self.title = str(
            self.title or ""
        ).strip()

        self.severity = str(
            self.severity or "LOW"
        ).upper().strip()

        if self.severity not in self.VALID_SEVERITIES:
            self.severity = "LOW"

        self.category = str(
            self.category or "CODE_QUALITY"
        ).upper().strip()

        if self.category not in self.VALID_CATEGORIES:
            self.category = "CODE_QUALITY"

        self.description = str(
            self.description or ""
        ).strip()

        self.recommendation = str(
            self.recommendation or ""
        ).strip()

        self.rule_id = str(
            self.rule_id or ""
        ).strip()

        self.cwe = str(
            self.cwe or ""
        ).strip()

        self.owasp = str(
            self.owasp or ""
        ).strip()

        self.source = str(
            self.source or ""
        ).strip()

        self.code_snippet = str(
            self.code_snippet or ""
        )

        self.confidence = str(
            self.confidence or ""
        ).strip()

        self.remediation_code = str(
            self.remediation_code or ""
        )

        if self.line is None:
            self.line = 0

        if self.end_line is None:
            self.end_line = self.line

        try:
            self.line = int(self.line)
        except (TypeError, ValueError):
            self.line = 0

        try:
            self.end_line = int(self.end_line)
        except (TypeError, ValueError):
            self.end_line = self.line

        if self.line < 0:
            self.line = 0

        if self.end_line < self.line:
            self.end_line = self.line

        if not isinstance(
            self.references,
            list
        ):
            self.references = []

        self.references = [
            str(reference).strip()
            for reference in self.references
            if str(reference).strip()
        ]

    # --------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------

    @property
    def line_number(self) -> int:
        """
        Backward-compatible access for older modules
        that use line_number instead of line.
        """

        return self.line

    @line_number.setter
    def line_number(self, value: int):
        try:
            self.line = int(value)
        except (TypeError, ValueError):
            self.line = 0

    # --------------------------------------------------
    # DICTIONARY CONVERSION
    # --------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the finding into a JSON-friendly dictionary.
        """

        return asdict(self)

    # --------------------------------------------------
    # CREATE FROM DICTIONARY
    # --------------------------------------------------

    @classmethod
    def from_dict(
        cls,
        finding: Optional[Dict[str, Any]]
    ) -> Optional["Finding"]:
        """
        Create a Finding from an existing dictionary.

        This allows the new model to work with the existing
        scanner and LLM outputs during migration.
        """

        if not isinstance(
            finding,
            dict
        ):
            return None

        title = finding.get(
            "title",
            finding.get(
                "name",
                "Unnamed Finding"
            )
        )

        severity = finding.get(
            "severity",
            "LOW"
        )

        category = finding.get(
            "category",
            "CODE_QUALITY"
        )

        category_normalized = str(
            category or ""
        ).upper().strip()

        if category_normalized in {
            "SECURITY",
            "VULNERABILITY",
            "SECURITY_VULNERABILITY",
            "SAST"
        }:
            category_normalized = "SECURITY"
        else:
            category_normalized = "CODE_QUALITY"

        line = finding.get(
            "line",
            finding.get(
                "line_number",
                finding.get(
                    "start_line",
                    0
                )
            )
        )

        end_line = finding.get(
            "end_line",
            finding.get(
                "last_line",
                line
            )
        )

        description = finding.get(
            "description",
            finding.get(
                "message",
                ""
            )
        )

        recommendation = finding.get(
            "recommendation",
            finding.get(
                "fix",
                ""
            )
        )

        return cls(
            title=title,
            severity=severity,
            category=category_normalized,
            description=description,
            recommendation=recommendation,
            line=line,
            end_line=end_line,
            rule_id=finding.get(
                "rule_id",
                finding.get(
                    "check_id",
                    finding.get(
                        "test_id",
                        ""
                    )
                )
            ),
            cwe=finding.get(
                "cwe",
                ""
            ),
            owasp=finding.get(
                "owasp",
                ""
            ),
            source=finding.get(
                "source",
                ""
            ),
            code_snippet=finding.get(
                "code_snippet",
                finding.get(
                    "snippet",
                    ""
                )
            ),
            confidence=finding.get(
                "confidence",
                ""
            ),
            remediation_code=finding.get(
                "remediation_code",
                ""
            ),
            references=finding.get(
                "references",
                []
            )
        )

    # --------------------------------------------------
    # STABLE FINDING ID
    # --------------------------------------------------

    def identity_key(self) -> tuple:
        """
        Generate a stable identity used for deduplication.

        Rule ID is preferred when available because scanner
        rules provide a stronger identity than natural-language
        descriptions.
        """

        normalized_title = " ".join(
            self.title.lower().split()
        )

        normalized_rule = " ".join(
            self.rule_id.lower().split()
        )

        if normalized_rule:
            return (
                self.category,
                normalized_rule,
                self.line,
                self.end_line
            )

        return (
            self.category,
            normalized_title,
            self.line,
            self.end_line
        )