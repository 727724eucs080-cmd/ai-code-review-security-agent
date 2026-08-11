from rag.retriever import retrieve_documents


query = "What is SQL Injection?"

results = retrieve_documents(query)

for index, document in enumerate(results, start=1):

    print("\n")
    print(f"Result {index}")
    print("-" * 40)

    print(document.page_content)