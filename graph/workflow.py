import time
from langgraph.graph import StateGraph, START, END
from reports.report_builder import ReportBuilder
from graph.state import AgentState

from validators.syntax_validator import SyntaxValidator

from agents.code_analysis_agent import code_analysis_agent
from agents.security_agent import security_agent
from agents.remediation_agent import remediation_agent
from agents.pr_summary_agent import pr_summary_agent


def syntax_validation(state: AgentState):

    result = SyntaxValidator.validate(
        state["code"],
        state["language"]
    )

    state["syntax_valid"] = result["valid"]
    state["syntax_message"] = result["message"]

    return state


def code_analysis(state: AgentState):

    if state["syntax_valid"]:

        start = time.time()

        state["code_analysis"] = code_analysis_agent.analyze(
            state["code"]
        )

        print(
            f"⏱ Code Analysis: {time.time() - start:.2f} seconds"
        )

    return state


def security_analysis(state: AgentState):

    if state["syntax_valid"]:

        start = time.time()

        state["security_analysis"] = security_agent.analyze(
            state["code"],
            state["language"]
        )

        print(
            f"⏱ Security Analysis: {time.time() - start:.2f} seconds"
        )

    return state


def remediation(state: AgentState):

    if state["syntax_valid"]:

        start = time.time()

        state["remediation"] = remediation_agent.generate(
            state
        )

        print(
            f"⏱ Remediation: {time.time() - start:.2f} seconds"
        )

    return state


def pr_summary(state: AgentState):

    if state["syntax_valid"]:

        start = time.time()

        state["pr_summary"] = pr_summary_agent.generate(
            state
        )

        print(
            f"⏱ PR Summary: {time.time() - start:.2f} seconds"
        )

    return state

def merge(state: AgentState):

    state["final_report"] = ReportBuilder.build(
        state
    )

    return state


builder = StateGraph(AgentState)


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
    "remediation",
    remediation
)

builder.add_node(
    "summary",
    pr_summary
)

builder.add_node(
    "merge",
    merge
)


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
    "remediation"
)

builder.add_edge(
    "remediation",
    "summary"
)

builder.add_edge(
    "summary",
    "merge"
)

builder.add_edge(
    "merge",
    END
)


workflow = builder.compile()