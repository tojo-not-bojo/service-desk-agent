"""Search the policy chunks by keywords or by meaning (embeddings)."""
import json
import math
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .documents import POLICY_DIR, load_chunks

load_dotenv(Path(__file__).parent / ".env")      # so the API key is available when run directly

EMBED_MODEL = "gemini-embedding-001" #"gemini-embedding-2"             # replace with a name from list_models.py
INDEX_PATH = POLICY_DIR.parent / "policy_embeddings.json"
STOPWORDS = {
    "a", "an", "the", "i", "me", "my", "is", "are", "am", "do", "does", "can", "could",
    "to", "of", "in", "on", "for", "and", "or", "how", "what", "when", "where", "much",
    "many", "be", "it", "if", "you", "your", "get", "with", "at", "by", "from", "about",
}

CHUNKS = load_chunks()


def searchable_text(chunk: dict) -> str:
    """Combine a chunk's document title, section heading and text for searching."""
    return f"{chunk['document']} - {chunk['section']}: {chunk['text']}"


# ---------- Keyword search ----------

def tokenize(text: str) -> set[str]:
    """Lowercase text, split it into words, and drop very short and common words."""
    words = re.findall(r"[a-z0-9£]+", text.lower())
    return {w for w in words if len(w) > 1 and w not in STOPWORDS}


def keyword_search(query: str, top_k: int = 3) -> list[dict]:
    """Return the chunks sharing the most words with the query, best first."""
    query_words = tokenize(query)
    scored = []
    for chunk in CHUNKS:
        score = len(query_words & tokenize(searchable_text(chunk)))
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [{**chunk, "score": score} for score, chunk in scored[:top_k]]


# ---------- Semantic search ----------

def embed(texts: list[str], task_type: str) -> list[list[float]]:
    """Turn each text into an embedding vector using the Gemini embedding model."""
    client = genai.Client()                       # reads GOOGLE_API_KEY from the environment
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return [e.values for e in result.embeddings]


def load_index() -> dict[str, list[float]]:
    """Return {chunk_id: vector}, building and saving it first if needed."""
    if INDEX_PATH.exists():
        with open(INDEX_PATH, encoding="utf-8") as f:
            index = json.load(f)
        if set(index) == {c["id"] for c in CHUNKS}:
            return index

    vectors = embed([searchable_text(c) for c in CHUNKS], "RETRIEVAL_DOCUMENT")
    index = {c["id"]: v for c, v in zip(CHUNKS, vectors, strict=True)}
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f)
    return index


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return how similar two vectors are: near 1 means very similar in meaning."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


def semantic_search(query: str, top_k: int = 3) -> list[dict]:
    """Return the chunks closest in meaning to the query, best first."""
    index = load_index()
    query_vector = embed([query], "RETRIEVAL_QUERY")[0]
    scored = [(cosine_similarity(query_vector, index[c["id"]]), c) for c in CHUNKS]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [{**chunk, "score": round(score, 3)} for score, chunk in scored[:top_k]]


# ---------- The tool ----------

def search_policies(query: str) -> dict:
    """Search the company's HR and IT policy documents.

    Use this for any question about annual leave, hybrid working, working abroad,
    expenses, travel, IT equipment, passwords or acceptable use of IT.

    Args:
        query: The user's question, or its key words, in plain English.

    Returns:
        A dict with "status": "success" and "results": up to 3 policy sections,
        best match first. Each result has a chunk_id, document, section, text
        and score (higher means more relevant).
    """
    if not query.strip():
        return {
            "status": "error",
            "message": "The query is empty. Pass the user's question or its key words.",
        }

    results = semantic_search(query)
    return {
        "status": "success",
        "query": query,
        "results": [
            {
                "chunk_id": r["id"],
                "document": r["document"],
                "section": r["section"],
                "text": r["text"],
                "score": r["score"],
            }
            for r in results
        ],
    }


if __name__ == "__main__":
    questions = [
        "What's the hotel limit in London?",
        "I've lost my laptop on the train",
        "Can I work from Spain for a couple of weeks?",
        "How many holiday days do I get?",
    ]
    for q in questions:
        print(f"\n{q}")
        print("  keyword: ", [r["id"] for r in keyword_search(q)])
        print("  semantic:", [r["id"] for r in semantic_search(q)])