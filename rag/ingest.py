import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from rag.chunker import split_documents


# ---------------------------------
# Paths
# ---------------------------------

DOCUMENT_FOLDER = "rag/documents"
VECTOR_PATH = "rag/vector_store"


# ---------------------------------
# Create Vector Database
# ---------------------------------

def create_vector_database():

    if not os.path.exists(DOCUMENT_FOLDER):

        print(
            f"Document folder not found: {DOCUMENT_FOLDER}"
        )

        return


    all_chunks = []


    # ---------------------------------
    # Read Documents
    # ---------------------------------

    for filename in os.listdir(
        DOCUMENT_FOLDER
    ):

        if not filename.lower().endswith(".txt"):
            continue


        file_path = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()


        except Exception as error:

            print(
                f"Unable to read {filename}: {error}"
            )

            continue


        chunks = split_documents(
            text
        )


        all_chunks.extend(
            chunks
        )


    # ---------------------------------
    # Validate Chunks
    # ---------------------------------

    if not all_chunks:

        print(
            "No document chunks found."
        )

        return


    # ---------------------------------
    # Embedding Model
    # ---------------------------------

    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"

    )


    # ---------------------------------
    # Create FAISS Database
    # ---------------------------------

    vector_db = FAISS.from_texts(

        all_chunks,

        embeddings

    )


    # ---------------------------------
    # Save Vector Database
    # ---------------------------------

    os.makedirs(
        VECTOR_PATH,
        exist_ok=True
    )


    vector_db.save_local(
        VECTOR_PATH
    )


    print(
        "Vector Database Created Successfully"
    )


    print(
        "Total Chunks:",
        len(all_chunks)
    )


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    create_vector_database()

