# This file holds settings. We keep them in one place so you change a value once, not in five files.

GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/tnahddisttud/sample-doc/"
    "refs/heads/main/atliqai_hr_policies.txt"
)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Name of the model that converts text into embeddings.

GROQ_MODEL = "openai/gpt-oss-safeguard-20b"
# Name of the Groq language model that will write the answers.

COLLECTION_NAME = "docs"
# The name we give our collection (think of it as a table) inside Chroma.

CHROMA_PATH = "./chroma_store"
# The folder on your disk where Chroma saves its data so it survives restarts.

CHUNK_SIZE = 50
# How many words go into each chunk when we split the document.

SYSTEM_PROMPT = """You are a helpful HR assistant.
Answer the user's question using ONLY the context provided below.
If the context does not contain enough information, say so — do not make things up.
Always cite the section name when referencing specific information."""
