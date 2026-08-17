import json

from langchain_core.prompts import PromptTemplate

from tools.gemini_tool import GeminiTool
from tools.pylint_tool import PylintTool


class CodeAnalysisAgent:

    def __init__(self):

        with open(
            "prompts/code_analysis_prompt.txt",
            "r",
            encoding="utf-8"
        ) as f:

            template = f.read()

        self.prompt = PromptTemplate(
            input_variables=[
                "code",
                "pylint_report"
            ],
            template=template
        )

    def analyze(self, code: str):

        # -------------------------
        # Static Analysis
        # -------------------------

        pylint_report = PylintTool.scan(code)

        # -------------------------
        # AI Analysis
        # -------------------------

        prompt = self.prompt.format(
            code=code,
            pylint_report=json.dumps(
                pylint_report,
                separators=(",", ":")
            )
        )

        # -------------------------
        # Structured Gemini Output
        # -------------------------

        schema = {
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
                                "type": "string",
                                "enum": [
                                    "CRITICAL",
                                    "HIGH",
                                    "MEDIUM",
                                    "LOW"
                                ]
                            },
                            "description": {
                                "type": "string"
                            },
                            "recommendation": {
                                "type": "string"
                            },
                            "category": {
                                "type": "string",
                                "enum": [
                                    "CODE_QUALITY"
                                ]
                            }
                        },
                        "required": [
                            "title",
                            "severity",
                            "description",
                            "recommendation",
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

        try:

            llm = GeminiTool.generate_json(
                prompt,
                schema
            )

        except Exception as e:

            llm = {
                "summary": "Unable to parse LLM response.",
                "findings": [],
                "raw_response": str(e)
            }

        # -------------------------
        # Enforce Code Quality
        # -------------------------

        findings = llm.get(
            "findings",
            []
        )

        if not isinstance(
            findings,
            list
        ):

            findings = []

        clean_findings = []

        for finding in findings:

            if not isinstance(
                finding,
                dict
            ):
                continue

            finding["category"] = "CODE_QUALITY"

            clean_findings.append(
                finding
            )

        llm["findings"] = clean_findings

        return {
            "pylint": pylint_report,
            "llm": llm
        }


code_analysis_agent = CodeAnalysisAgent()