from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    path: Path = Path("config.json")
    notes_dir: Path = Path("notes")

    def save(self):
        with open(self.path, "w") as f:
            json.dump({"notes_dir": str(self.notes_dir)}, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> Config:
        if not path.exists():
            raise FileNotFoundError(f"Config file not found at {path}")
        with open(path) as f:
            config_dict = json.load(f)
            return cls(**config_dict)
