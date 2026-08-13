from google import genai
from google.genai import types
import os


class GeminiService:
    """
    Centralized Gemini LLM Service.

    Used by:
    - Code Analysis Agent
    - Security Agent
    - Remediation Agent
    - Secure Coding Assistant
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.1-flash-lite"

    def invoke(self, prompt: str):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=800
            )
        )

        return response.text


gemini_service = GeminiService()