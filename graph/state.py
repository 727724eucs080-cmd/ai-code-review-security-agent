from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    code: str

    language: str

    syntax_valid: bool

    syntax_message: str

    code_analysis: Dict[str, Any]

    security_analysis: Dict[str, Any]

    remediation: Dict[str, Any]

    pr_summary: Dict[str, Any]

    final_report: Dict[str, Any]