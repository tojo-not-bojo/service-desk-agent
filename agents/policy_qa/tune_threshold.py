"""Print the top semantic search score for answerable and unanswerable questions."""
from .search import semantic_search

GROUPS = {
    "answerable": [
        "What's the hotel limit in London?",
        "I've lost my laptop on the train",
        "Can I work from Spain for a couple of weeks?",
        "How many holiday days do I get?",
        "How long must my password be?",
        "Can I install my own software on my laptop?",
    ],
    "unanswerable": [
        "What's the capital of France?",
        "Can I bring my dog to the office?",
        "How do I book a meeting room?",
    ],
    "borderline": [
        "How much parental leave do I get?",
    ],
}

for group, questions in GROUPS.items():
    print(group)
    for q in questions:
        top = semantic_search(q, top_k=1)[0]
        print(f"  {top['score']:.3f}  {top['id']:40}  {q}")
