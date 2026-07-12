from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from chunker import split_documents


def create_vector_database():

    with open(
        "rag/documents/security_rules.txt",
        "r",
        encoding="utf-8"
    ) as file:

        document = file.read()

    chunks = split_documents(document)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_texts(
        chunks,
        embeddings
    )

    vector_db.save_local(
        "rag/vector_store"
    )

    print("\nVector Database Created Successfully.")
    print(f"Total Chunks : {len(chunks)}")


if __name__ == "__main__":

    create_vector_database()