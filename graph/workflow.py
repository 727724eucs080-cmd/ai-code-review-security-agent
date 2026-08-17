import time

from langgraph.graph import StateGraph, START, END

from reports.report_builder import ReportBuilder
from graph.state import AgentState

from validators.syntax_validator import SyntaxValidator

from agents.code_analysis_agent import code_analysis_agent
from agents.security_agent import security_agent
from agents.finding_processor import FindingProcessor
from agents.remediation_agent import remediation_agent
from agents.pr_summary_agent import pr_summary_agent


# ==========================================================
# SYNTAX VALIDATION
# ==========================================================

def syntax_validation(state: AgentState):

    result = SyntaxValidator.validate(
        state["code"],
        state["language"]
    )

    state["syntax_valid"] = result["valid"]
    state["syntax_message"] = result["message"]

    return state


# ==========================================================
# CODE QUALITY ANALYSIS
# ==========================================================

def code_analysis(state: AgentState):

    if not state["syntax_valid"]:
        return state

    start = time.time()

    state["code_analysis"] = (
        code_analysis_agent.analyze(
            state["code"]
        )
    )

    print(
        f"⏱ Code Analysis: "
        f"{time.time() - start:.2f} seconds"
    )

    return state


# ==========================================================
# SECURITY ANALYSIS
# ==========================================================

def security_analysis(state: AgentState):

    if not state["syntax_valid"]:
        return state

    start = time.time()

    state["security_analysis"] = (
        security_agent.analyze(
            state["code"],
            state["language"]
        )
    )

    print(
        f"⏱ Security Analysis: "
        f"{time.time() - start:.2f} seconds"
    )

    return state


# ==========================================================
# FINDING PROCESSING
# ==========================================================

def process_findings(state: AgentState):

    if not state["syntax_valid"]:
        return state

    start = time.time()

    result = FindingProcessor.process(
        state.get(
            "code_analysis",
            {}
        ),
        state.get(
            "security_analysis",
            {}
        )
    )

    state["findings"] = (
        FindingProcessor.to_dicts(
            result["findings"]
        )
    )

    state["code_quality_findings"] = (
        FindingProcessor.to_dicts(
            result["code_quality_findings"]
        )
    )

    state["security_findings"] = (
        FindingProcessor.to_dicts(
            result["security_findings"]
        )
    )

    state["finding_statistics"] = (
        result["statistics"]
    )

    print(
        f"⏱ Finding Processing: "
        f"{time.time() - start:.2f} seconds"
    )

    print(
        "📋 Findings:",
        len(state["findings"])
    )

    print(
        "🔧 Code Quality:",
        len(
            state["code_quality_findings"]
        )
    )

    print(
        "🛡 Security:",
        len(
            state["security_findings"]
        )
    )

    return state


# ==========================================================
# REMEDIATION
# ==========================================================

def remediation(state: AgentState):

    if not state["syntax_valid"]:
        return state

    start = time.time()

    state["remediation"] = (
        remediation_agent.generate(
            state
        )
    )

    print(
        f"⏱ Remediation: "
        f"{time.time() - start:.2f} seconds"
    )

    return state


# ==========================================================
# FINAL REPORT
# ==========================================================

def merge(state: AgentState):

    start = time.time()

    state["final_report"] = (
        ReportBuilder.build(
            state
        )
    )

    print(
        f"⏱ Final Report: "
        f"{time.time() - start:.2f} seconds"
    )

    return state


# ==========================================================
# PULL REQUEST SUMMARY
# ==========================================================

def pr_summary(state: AgentState):

    if not state["syntax_valid"]:
        return state

    start = time.time()

    state["pr_summary"] = (
        pr_summary_agent.generate(
            state
        )
    )

    print(
        f"⏱ PR Summary: "
        f"{time.time() - start:.2f} seconds"
    )

    return state


# ==========================================================
# ATTACH PR SUMMARY TO FINAL REPORT
# ==========================================================

def attach_pr_summary(state: AgentState):

    if not state["syntax_valid"]:
        return state

    final_report = state.get(
        "final_report",
        {}
    )

    if not isinstance(
        final_report,
        dict
    ):
        final_report = {}

    final_report["pr_summary"] = (
        state.get(
            "pr_summary",
            {}
        )
    )

    state["final_report"] = final_report

    return state


# ==========================================================
# BUILD LANGGRAPH WORKFLOW
# ==========================================================

builder = StateGraph(
    AgentState
)


# ==========================================================
# REGISTER NODES
# ==========================================================

builder.add_node(
    "syntax",
    syntax_validation
)

builder.add_node(
    "code",
    code_analysis
)

builder.add_node(
    "security",
    security_analysis
)

builder.add_node(
    "process_findings",
    process_findings
)

builder.add_node(
    "remediation",
    remediation
)

builder.add_node(
    "merge",
    merge
)

builder.add_node(
    "summary",
    pr_summary
)

builder.add_node(
    "attach_pr_summary",
    attach_pr_summary
)


# ==========================================================
# WORKFLOW ORDER
# ==========================================================

builder.add_edge(
    START,
    "syntax"
)

builder.add_edge(
    "syntax",
    "code"
)

builder.add_edge(
    "code",
    "security"
)

builder.add_edge(
    "security",
    "process_findings"
)

builder.add_edge(
    "process_findings",
    "remediation"
)

builder.add_edge(
    "remediation",
    "merge"
)

builder.add_edge(
    "merge",
    "summary"
)

builder.add_edge(
    "summary",
    "attach_pr_summary"
)

builder.add_edge(
    "attach_pr_summary",
    END
)


# ==========================================================
# COMPILE WORKFLOW
# ==========================================================

workflow = builder.compile()