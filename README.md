# RAG HR Assistant

A simple Retrieval‑Augmented Generation (RAG) application that ingests a text document (HR policies), stores it in a Chroma vector store, and answers user questions using a large language model (Groq). The project demonstrates how to combine document ingestion, embedding generation, vector search, and LLM prompting in a compact, easy‑to‑run Python script.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Testing & Extending](#testing--extending)
- [License](#license)

---

## Features

- **Document ingestion** – fetches a remote text file, splits it into word‑based chunks.
- **Embedding generation** – uses `sentence‑transformers` to create vector embeddings.
- **Vector store** – stores embeddings in a persistent Chroma collection.
- **RAG query** – retrieves relevant chunks and passes them to a Groq LLM with a system prompt that forces the model to answer strictly from the provided context.
- **Interactive CLI** – simple REPL that lets you ask questions until you type `quit`.

---

## Prerequisites

- Python **3.9+**
- A Groq API key (free tier available). You will be prompted for it on first run, or you can set the environment variable `GROQ_API_KEY`.
- Internet access (to download the source document and model weights).

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your‑username/your‑repo.git
cd your-repo

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r rag/requirements.txt
```

---

## Configuration

All configurable values live in `rag/config.py`:

| Variable | Description |
|---|---|
| `GITHUB_RAW_URL` | URL of the raw text document to ingest. Change this to point at any other document you want the assistant to use. |
| `EMBEDDING_MODEL` | Sentence‑Transformer model used for embedding generation (default: `all-MiniLM-L6-v2`). |
| `GROQ_MODEL` | Groq LLM model name (default: `openai/gpt-oss-safeguard-20b`). |
| `COLLECTION_NAME` | Name of the Chroma collection where embeddings are stored. |
| `CHROMA_PATH` | Filesystem path for the persistent Chroma store. |
| `CHUNK_SIZE` | Number of words per chunk when splitting the source document. |
| `SYSTEM_PROMPT` | Prompt that guides the LLM to answer only from the supplied context. |

If you need to change any of these values, edit `rag/config.py` and the application will pick them up automatically.

---

## Running the Application

```bash
python rag/main.py
```

The script will:
1. Prompt for a Groq API key if `GROQ_API_KEY` is not set in the environment.
2. Download the document defined in `GITHUB_RAW_URL`.
3. Split the document into chunks and embed each chunk.
4. Build (or load) a Chroma collection stored at `CHROMA_PATH`.
5. Enter an interactive loop where you can type questions. Type `quit`, `exit`, or `q` to stop.

Example session:

```
Ask a question (or type 'quit' to exit):
> What is the vacation policy?

The vacation policy states that employees accrue 15 days of paid vacation per year ...
```

---

## Project Structure

```
├─ .idea/                # IDE configuration (ignore)
├─ rag/                  # Core package
│   ├─ __init__.py       # (empty) makes rag a package
│   ├─ config.py         # Global configuration constants
│   ├─ ingest.py         # Functions to download and chunk the source document
│   ├─ main.py           # Entry point – CLI REPL
│   ├─ query.py          # RAG query orchestration (retrieval + LLM call)
│   ├─ requirements.txt  # Python dependencies
│   └─ store.py          # Embedding generation and Chroma collection handling
└─ README.md             # (this file)
```

---

## How It Works

1. **Ingestion (`rag/ingest.py`)**
   - `load_document(url)` fetches the raw text from the URL.
   - `parse_word_chunks(text, chunk_size=CHUNK_SIZE)` splits the text into word‑based chunks.
2. **Embedding & Storage (`rag/store.py`)**
   - `get_embedder()` loads the Sentence‑Transformer model.
   - `build_collection(chunks, embedder)` creates a Chroma collection (or loads an existing one) and adds embeddings.
3. **Query (`rag/query.py`)**
   - `rag(question, collection, embedder, groq_client)` performs a similarity search, builds a prompt with the retrieved chunks, and calls the Groq LLM.
4. **CLI (`rag/main.py`)**
   - Orchestrates the above steps and provides a simple interactive loop.

---

## Testing & Extending

- **Changing the source document** – Update `GITHUB_RAW_URL` to point at a different plain‑text file.
- **Different embedding models** – Replace `EMBEDDING_MODEL` with any model supported by `sentence‑transformers`.
- **Alternative vector stores** – The `store.py` module is deliberately small; you can swap out Chroma for FAISS, Milvus, etc., by adjusting the `build_collection` function.
- **Unit tests** – Add tests under a `tests/` directory using `pytest` to verify ingestion, chunking, and retrieval logic.

---

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.

---

*Happy querying!*