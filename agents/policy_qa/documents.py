"""Load the synthetic policy documents and split them into chunks."""
from pathlib import Path

POLICY_DIR = Path(__file__).resolve().parents[2] / "data" / "policies"


def slugify(text: str) -> str:
    """Turn a heading into a short id, e.g. "Carrying over leave" -> "carrying-over-leave"."""
    return "-".join(text.lower().split())


def load_chunks() -> list[dict]:
    """Split every policy document into one chunk per "## " section.

    Returns:
        A list of chunks, each a dict with id, document, section, source and text.
    """
    chunks = []
    for path in sorted(POLICY_DIR.glob("*.md")):
        document = path.stem
        sections = []                                  # each item: [heading, list of lines]

        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                document = line[2:].strip()
            elif line.startswith("## "):
                sections.append([line[3:].strip(), []])
            elif line.strip() and sections:
                sections[-1][1].append(line.strip())

        for heading, lines in sections:
            chunks.append({
                "id": f"{path.stem}#{slugify(heading)}",
                "document": document,
                "section": heading,
                "source": path.name,
                "text": " ".join(lines),
            })
    return chunks


if __name__ == "__main__":
    chunks = load_chunks()
    print(len(chunks))
    print(chunks[0])