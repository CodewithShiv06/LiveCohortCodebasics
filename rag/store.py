# This file does embedding and indexing - turning chunks into numbers and saving them in Chroma.

import chromadb
from sentence_transformers import SentenceTransformer
from config import COLLECTION_NAME, CHROMA_PATH, EMBEDDING_MODEL


def get_embedder() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def build_collection(chunks: list[dict], embedder: SentenceTransformer):
    """Embed chunks and store them in a fresh Chroma collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Create a brand-new empty collection (like a fresh table).
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
        # use cosine similarity to compare vectors
        embedding_function=None,
    )

    # Pull just the text out of each chunk dictionary into a plain list of strings.
    texts = [c["content"] for c in chunks]
    print(f"Embedding {len(texts)} chunks …")  # status message; len() = how many chunks
    # Convert every chunk's text into an embedding (a list of numbers).
    embeddings = embedder.encode(texts, show_progress_bar=True)

    # Store everything in Chroma. Chroma wants four parallel lists, same length, same order.
    collection.add(
        ids=[str(c["chunk_index"]) for c in chunks],
        embeddings=[e.tolist() for e in embeddings],
        documents=texts,
        metadatas=[{"chunk_index": c["chunk_index"]} for c in chunks],
    )
    print(f"Indexed {collection.count()} chunks")
    return collection
