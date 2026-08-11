import json

from langchain_core.prompts import PromptTemplate

from tools.ollama_tool import OllamaTool
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

        response = OllamaTool.generate(prompt)

        response = response.replace("```json", "")
        response = response.replace("```", "")

        try:

            llm = json.loads(response)

        except Exception:

            llm = {

                "summary": "Unable to parse LLM response.",

                "findings": [],

                "raw_response": response

            }

        return {

            "pylint": pylint_report,

            "llm": llm

        }


code_analysis_agent = CodeAnalysisAgent()