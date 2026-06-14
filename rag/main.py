import os
import getpass
from groq import Groq

from config import GITHUB_RAW_URL
from ingest import load_document, parse_word_chunks
from store import get_embedder, build_collection
from query import rag


def main():
    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

    # --- Ingest ---
    raw_text = load_document(GITHUB_RAW_URL)
    print(f"Loaded {len(raw_text):,} characters")
    chunks = parse_word_chunks(raw_text)
    print(f"Total chunks: {len(chunks)}")

    # Build the store
    embedder = get_embedder()
    collection = build_collection(chunks, embedder)
    groq_client = Groq()

    # Interactive loop
    # loop forever until we break out
    print("\nAsk a question (or type 'quit' to exit):")

    while True:
        question = input("\n> ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            break
        if not question:
            continue
        answer, _ = rag(question, collection, embedder, groq_client)
        print("\n" + answer)


if __name__ == "__main__":
    main()
