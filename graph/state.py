from typing import TypedDict, Dict, Any, List


class AgentState(TypedDict):

    # ==================================================
    # SOURCE CODE
    # ==================================================

    code: str

    language: str

    # ==================================================
    # SYNTAX VALIDATION
    # ==================================================

    syntax_valid: bool

    syntax_message: str

    # ==================================================
    # RAW AGENT ANALYSIS
    # ==================================================

    code_analysis: Dict[str, Any]

    security_analysis: Dict[str, Any]

    # ==================================================
    # CENTRALIZED FINDINGS
    # ==================================================

    findings: List[Dict[str, Any]]

    code_quality_findings: List[Dict[str, Any]]

    security_findings: List[Dict[str, Any]]

    finding_statistics: Dict[str, int]

    # ==================================================
    # DOWNSTREAM AGENTS
    # ==================================================

    remediation: Dict[str, Any]

    pr_summary: Dict[str, Any]

    # ==================================================
    # FINAL REPORT
    # ==================================================

    final_report: Dict[str, Any]