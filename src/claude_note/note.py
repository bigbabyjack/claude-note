import random
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Note:
    path: Path
    category: str = "Uncategorized"


def read_note(note: Note) -> str:
    with open(note.path) as f:
        return f.read()


def add_note(path: Path, content: str) -> Note:
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    with open(path, "a") as f:
        f.write(content + "\n")

    return Note(path)


# TODO: implement a real categorization algorithm
def categorize(note: Note, categories: list[str]) -> str:
    if not categories:
        return "Uncategorized"
    category: str = random.choice(categories)
    return category


# TODO: implement a real summarization algorithm
def summarize(notes: list[Note]) -> str:
    summaries: list[str] = []
    for note in notes:
        content = read_note(note)
        summary = content[:100]
        summaries.append(summary)
    return "\n".join(summaries)
