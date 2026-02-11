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
