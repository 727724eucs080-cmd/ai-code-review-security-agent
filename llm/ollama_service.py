from langchain_ollama import ChatOllama


class OllamaService:
    """
    Centralized Ollama LLM Service.

    Used by:
    - Code Analysis Agent
    - Security Agent
    - Remediation Agent
    - Secure Coding Assistant
    """

    def __init__(self):

        self.llm = ChatOllama(
            model="qwen2.5:3b",

            temperature=0,

            # Keep responses concise for faster generation
            num_predict=400,

            # Smaller context reduces processing overhead
            num_ctx=2048,

            # Keep model loaded between requests
            keep_alive="30m"
        )

    def invoke(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content


ollama_service = OllamaService()