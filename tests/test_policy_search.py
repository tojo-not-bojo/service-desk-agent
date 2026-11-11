"""Unit tests for policy chunking and search.

semantic_search is replaced with fake results, so these make no embedding calls.
"""
import pytest

from policy_qa import search
from policy_qa.documents import load_chunks


# ---------- Chunking ----------

def test_every_policy_section_becomes_a_chunk():
    chunks = load_chunks()
    assert len(chunks) == 16                                # 4 documents x 4 sections
    assert len({c["id"] for c in chunks}) == len(chunks)    # ids are unique
    assert all(c["text"] for c in chunks)                   # no empty sections


# ---------- Keyword search ----------

def test_tokenize_drops_stopwords_and_punctuation():
    assert search.tokenize("How do I book a laptop?") == {"book", "laptop"}


@pytest.mark.parametrize(
    ("query", "expected_id"),
    [
        ("hotel limit in London", "expenses#hotels-and-meals"),
        ("carry over unused days", "annual_leave#carrying-over-leave"),
    ],
)
def test_keyword_search_top_result(query, expected_id):
    assert search.keyword_search(query)[0]["id"] == expected_id


# ---------- search_policies (semantic_search replaced) ----------

def fake_semantic_search(*scores):
    """Return a stand-in for semantic_search that gives one result per score, best first."""
    def _search(query):
        return [{**chunk, "score": score} for chunk, score in zip(search.CHUNKS, scores)]
    return _search


def test_results_below_min_score_are_dropped(monkeypatch):
    monkeypatch.setattr(search, "semantic_search", fake_semantic_search(0.8, search.MIN_SCORE - 0.01))
    result = search.search_policies("annual leave")
    assert result["status"] == "success"
    assert [r["score"] for r in result["results"]] == [0.8]


def test_score_equal_to_min_score_is_kept(monkeypatch):
    monkeypatch.setattr(search, "semantic_search", fake_semantic_search(search.MIN_SCORE))
    assert search.search_policies("annual leave")["status"] == "success"


def test_error_when_nothing_is_close_enough(monkeypatch):
    monkeypatch.setattr(search, "semantic_search", fake_semantic_search(0.5, 0.4))
    result = search.search_policies("what's for lunch?")
    assert result["status"] == "error"
    assert "error_message" in result


def test_empty_query_is_rejected(monkeypatch):
    monkeypatch.setattr(search, "semantic_search", fake_semantic_search(0.9))
    result = search.search_policies("   ")
    assert result["status"] == "error"
    assert "empty" in result["error_message"]


def test_results_include_what_citations_need(monkeypatch):
    monkeypatch.setattr(search, "semantic_search", fake_semantic_search(0.9))
    first = search.search_policies("annual leave")["results"][0]
    for key in ("document", "section", "source", "text"):
        assert first[key]
    assert first["source"].endswith(".md")
