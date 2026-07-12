"""
chunker.py

Splits large documents into smaller chunks for embedding.
"""


def split_documents(text, chunk_size=100):
    """
    Splits text into chunks of approximately 'chunk_size' words.

    Parameters
    ----------
    text : str
        Input document text.

    chunk_size : int
        Number of words per chunk.

    Returns
    -------
    list
        List of text chunks.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append(chunk)

    return chunks