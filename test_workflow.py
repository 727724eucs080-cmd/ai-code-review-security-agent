from graph.workflow import workflow


state = {

    "code": """

password = "admin123"

print(password)

""",

    "language": "python",

    "syntax_valid": False,

    "syntax_message": "",

    "code_analysis": {},

    "security_analysis": {},

    "remediation": {},

    "pr_summary": {},

    "final_report": {}

}


result = workflow.invoke(state)

print(result["final_report"])