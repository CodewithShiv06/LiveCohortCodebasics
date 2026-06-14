# This file does loading and chunking - getting the text and cutting it into pieces

import requests
from config import CHUNK_SIZE


def load_document(url: str) -> str:
    """Fetch a plain-text file from a raw GitHub URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_word_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[dict]:
    """Split text into fixed-size word chunks."""
    clean_lines = []
    for line in text.splitlines():
        line = line.strip().lstrip('#').strip()
        if line:
            clean_lines.append(line)

    # Join all the cleaned lines into one big string, then .split() breaks it
    # into a list of individual words (splitting on spaces).
    words = " ".join(clean_lines).split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        # Take words from position i up to i+50 and join them back into a string.
        content = " ".join(words[i: i + chunk_size])
        chunks.append({
            "chunk_index": len(chunks),
            "content": content,
        })
    return chunks
    # give back the full list of chunk dictionaries
