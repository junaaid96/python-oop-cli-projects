"""Command pattern: each verb is a small class with an `execute` method."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from text_adventure.world import GameState


class Command(ABC):
    # ClassVar marks a class-level attribute (not a per-instance field).
    verbs: ClassVar[tuple[str, ...]] = ()
    help: ClassVar[str] = ""

    @abstractmethod
    def execute(self, state: GameState, arg: str) -> str: ...


class Look(Command):
    verbs = ("look", "l")
    help = "describe the room"

    def execute(self, state: GameState, arg: str) -> str:
        room = state.room
        items = f" You see: {', '.join(room.items)}." if room.items else ""
        return f"[{room.name}] {room.description}{items} Exits: {', '.join(room.exits)}."


class Go(Command):
    verbs = ("go", "move")
    help = "go <direction>"

    def execute(self, state: GameState, arg: str) -> str:
        room = state.room
        if arg not in room.exits:
            return "You can't go that way."
        needed = room.locks.get(arg)
        if needed and needed not in state.inventory:
            # Note: no dark-room puzzle without a lamp would be a nice exercise.
            return f"It's locked. You need the {needed}."
        state.location = room.exits[arg]
        state.moves += 1
        return Look().execute(state, "")


class Take(Command):
    verbs = ("take", "get")
    help = "take <item>"

    def execute(self, state: GameState, arg: str) -> str:
        if arg not in state.room.items:
            return f"There is no {arg} here."
        if arg == "key" and "lamp" not in state.inventory:
            return "It's too dark to find it. Maybe a light would help."
        state.room.items.remove(arg)
        state.inventory.append(arg)
        if arg == "trophy":
            state.won = True
            return f"You lift the trophy. You win in {state.moves} moves!"
        return f"Taken: {arg}."


class Inventory(Command):
    verbs = ("inventory", "i")
    help = "list what you carry"

    def execute(self, state: GameState, arg: str) -> str:
        return "You carry: " + (", ".join(state.inventory) or "nothing")


class Read(Command):
    verbs = ("read",)
    help = "read <item>"

    def execute(self, state: GameState, arg: str) -> str:
        if arg != "note" or "note" not in state.inventory:
            return "You have nothing like that to read."
        return "The note says: 'Light reveals what darkness hides. Look up.'"


# A registry built from the classes: verb -> command instance.
COMMANDS: dict[str, Command] = {
    verb: cls() for cls in (Look, Go, Take, Inventory, Read) for verb in cls.verbs
}
DIRECTIONS = {"n": "north", "s": "south", "e": "east", "w": "west", "u": "up", "d": "down"}


def handle(state: GameState, line: str) -> str:
    words = line.lower().split()
    if not words:
        return "Say something."
    verb, arg = words[0], " ".join(words[1:])
    # Shortcuts: "n" or "north" alone means "go north".
    if verb in DIRECTIONS or verb in DIRECTIONS.values():
        verb, arg = "go", DIRECTIONS.get(verb, verb)
    command = COMMANDS.get(verb)
    if command is None:
        return "Commands: " + "; ".join(
            f"{c.verbs[0]} ({c.help})" for c in dict.fromkeys(COMMANDS.values())
        )
    return command.execute(state, arg)
