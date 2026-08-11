import json

from llm.ollama_service import ollama_service


class OllamaTool:

    @staticmethod
    def generate(prompt: str) -> str:
        """
        Generate an LLM response and normalize it into JSON text.
        """

        response = ollama_service.invoke(prompt)

        if response is None:
            return json.dumps({
                "summary": "",
                "findings": []
            })

        response = str(response).strip()

        # Remove Markdown JSON code fences if the model adds them
        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        # Try to parse the model response
        try:
            data = json.loads(response)

        except json.JSONDecodeError:
            return json.dumps({
                "summary": "",
                "findings": []
            })

        # Normalize common incorrect capitalized keys
        if isinstance(data, dict):

            if "Findings" in data and "findings" not in data:
                data["findings"] = data.pop("Findings")

            if "Summary" in data and "summary" not in data:
                data["summary"] = data.pop("Summary")

            if "Findings" in data:
                data.pop("Findings", None)

            if "Summary" in data:
                data.pop("Summary", None)

            # Always provide the expected keys
            data.setdefault("summary", "")
            data.setdefault("findings", [])

            # Make sure findings is actually a list
            if not isinstance(data["findings"], list):
                data["findings"] = []

            return json.dumps(data)

        return json.dumps({
            "summary": "",
            "findings": []
        })


ollama_tool = OllamaTool()

