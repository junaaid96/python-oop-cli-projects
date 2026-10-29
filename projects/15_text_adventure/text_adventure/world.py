"""World data and game state. Rooms are data, so new maps need no new code."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Room:
    name: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)  # direction -> room name
    items: list[str] = field(default_factory=list)
    # A locked exit needs an item: direction -> required item.
    locks: dict[str, str] = field(default_factory=dict)


@dataclass
class GameState:
    rooms: dict[str, Room]
    location: str
    inventory: list[str] = field(default_factory=list)
    moves: int = 0
    won: bool = False

    @property
    def room(self) -> Room:
        return self.rooms[self.location]

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> GameState:
        data = json.loads(path.read_text(encoding="utf-8"))
        # Nested dicts must be turned back into Room objects explicitly.
        data["rooms"] = {name: Room(**room) for name, room in data["rooms"].items()}
        return cls(**data)


def new_game() -> GameState:
    rooms = [
        Room(
            "hall",
            "A dusty hall. Stairs lead up; a corridor runs east.",
            {"east": "library", "up": "attic"},
            ["lamp"],
        ),
        Room(
            "library",
            "Shelves of old manuals. A heavy door is to the north.",
            {"west": "hall", "north": "vault"},
            ["note"],
            {"north": "key"},
        ),
        Room(
            "attic", "Dark and cramped. Something glints in the corner.", {"down": "hall"}, ["key"]
        ),
        Room(
            "vault",
            "A small vault holding the legendary Clean Code trophy!",
            {"south": "library"},
            ["trophy"],
        ),
    ]
    return GameState({r.name: r for r in rooms}, "hall")
