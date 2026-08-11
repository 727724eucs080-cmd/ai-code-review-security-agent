def split_documents(
    text,
    chunk_size=300,
    overlap=50
):

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0."
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )


    words = text.split()

    chunks = []

    step = chunk_size - overlap


    for i in range(
        0,
        len(words),
        step
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():

            chunks.append(chunk)


    return chunks

