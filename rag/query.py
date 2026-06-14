# This file does retrieval and the end-to-end RAG answer.

from config import SYSTEM_PROMPT, GROQ_MODEL


def retrieve(query: str, collection, embedder, top_k: int = 5) -> list[dict]:
    query_vector = embedder.encode(query).tolist()

    # Ask Chroma for the chunks whose vectors are closest to the question's vector.
    res = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "distances"],
    )

    # Chroma returns lists-inside-lists (one inner list per question).
    # We only asked one question, so we take the first inner list with [0].
    docs = res["documents"][0]
    distances = res["distances"][0]

    # Build a tidy list of dictionaries to return.
    return [
        # distance and similarity are opposites for cosine, so similarity = 1 - distance.
        # round(..., 4) keeps just 4 decimal places so it's readable.
        {"content": doc, "score": round(1 - dist, 4)}
        for doc, dist in zip(docs, distances)
        # zip() pairs each doc with its distance
    ]


def build_context(retrieved_chunks: list[dict]) -> str:
    # Turn the retrieved chunks into one labelled text block to feed the LLM.
    parts = [
        f"[Source {i}]\n{chunk['content']}"
        for i, chunk in enumerate(retrieved_chunks, 1)
    ]
    # Glue the sources together with a divider line between each.
    return "\n\n---\n\n".join(parts)


def rag(query: str, collection, embedder, groq_client, top_k: int = 5):
    # Step 1: find the most relevant chunks for the question.
    chunks = retrieve(query, collection, embedder, top_k=top_k)
    if not chunks:
        return "No relevant content found in the document.", ""

    # Step 2: format those chunks into a single context block.
    context = build_context(chunks)

    # Combine the context and the question into one message for the LLM.
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    # Step 3: send it to Groq and ask for an answer.
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temprature=0.2
    )

    return response.choices[0].message.content, context
