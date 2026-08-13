import json

from llm.gemini_service import gemini_service
from google.genai import types


class GeminiTool:

    @staticmethod
    def generate(prompt: str):

        return gemini_service.invoke(prompt)

    @staticmethod
    def generate_json(prompt: str, schema: dict):

        response = gemini_service.client.models.generate_content(
            model=gemini_service.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=400,
                response_mime_type="application/json",
                response_json_schema=schema
            )
        )

        return json.loads(response.text)