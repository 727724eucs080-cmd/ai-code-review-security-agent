from llm.ollama_service import ollama_service


response = ollama_service.invoke(

    "Reply with exactly one sentence: Ollama connection successful."

)

print(response)