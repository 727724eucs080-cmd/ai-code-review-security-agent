from llm.gemini_service import gemini_service


response = gemini_service.invoke(
    "Reply with exactly one sentence: Gemini connection successful."
)


print(response)