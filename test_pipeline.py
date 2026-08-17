from graph.workflow import workflow


code = """
import os

password = "admin123"

def run_command(user_input):
    return os.system(user_input)

def execute_code(user_input):
    return eval(user_input)

run_command("echo hello")
"""


initial_state = {
    "code": code,
    "language": "python",
    "syntax_valid": False,
    "syntax_message": "",
    "code_analysis": {},
    "security_analysis": {},
    "findings": [],
    "code_quality_findings": [],
    "security_findings": [],
    "finding_statistics": {},
    "remediation": {},
    "pr_summary": {},
    "final_report": {}
}


print("\n========================================")
print("STARTING PIPELINE")
print("========================================\n")


result = workflow.invoke(initial_state)


print("\n========================================")
print("PIPELINE COMPLETED")
print("========================================\n")


print("SYNTAX VALID:")
print(result.get("syntax_valid"))


print("\nSYNTAX MESSAGE:")
print(result.get("syntax_message"))


print("\nCODE ANALYSIS:")
print(result.get("code_analysis"))


print("\nSECURITY ANALYSIS:")
print(result.get("security_analysis"))


print("\nFINDINGS:")
print(result.get("findings"))


print("\nCODE QUALITY FINDINGS:")
print(result.get("code_quality_findings"))


print("\nSECURITY FINDINGS:")
print(result.get("security_findings"))


print("\nFINDING STATISTICS:")
print(result.get("finding_statistics"))


print("\nREMEDIATION:")
print(result.get("remediation"))


print("\nPR SUMMARY:")
print(result.get("pr_summary"))


print("\nFINAL REPORT:")
print(result.get("final_report"))