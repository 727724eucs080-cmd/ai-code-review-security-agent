from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# ---------------------------------
# Embedding Model
# ---------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------
# Vector Database
# ---------------------------------

vector_db = None


try:

    vector_db = FAISS.load_local(
        "rag/vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )

except Exception:

    vector_db = None


# ---------------------------------
# Retrieve Documents
# ---------------------------------

def retrieve_documents(
    query,
    k=2
):

    if vector_db is None:
        return []

    if not query or not query.strip():
        return []

    try:

        return vector_db.similarity_search(
            query,
            k=k
        )

    except Exception:

        return []

