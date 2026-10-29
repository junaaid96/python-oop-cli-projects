"""Domain model and storage for the contact book."""

# `annotations` lets type hints refer to classes defined later in the file.
from __future__ import annotations

# json turns Python dicts/lists into text and back.
import json

# asdict converts a dataclass instance into a plain dict (handy for JSON).
from dataclasses import asdict, dataclass

# Path is the modern, object-oriented way to work with file paths.
from pathlib import Path


# @dataclass writes __init__, __repr__ and __eq__ for us from the fields below.
# frozen=True makes instances immutable, so a Contact can't change by accident.
@dataclass(frozen=True)
class Contact:
    # Each field has a type hint; mypy uses these to catch mistakes.
    name: str
    phone: str
    # A default value makes the field optional when creating a Contact.
    email: str = ""

    # __post_init__ runs right after the generated __init__: perfect for validation.
    def __post_init__(self) -> None:
        # strip() removes spaces; an empty name is not allowed.
        if not self.name.strip():
            raise ValueError("name must not be empty")
        # Allow digits plus common phone symbols only.
        if not self.phone or not all(ch.isdigit() or ch in "+- " for ch in self.phone):
            raise ValueError(f"invalid phone number: {self.phone!r}")


class ContactBook:
    """Holds contacts in memory and saves them to a JSON file."""

    def __init__(self, path: Path) -> None:
        # The leading underscore marks attributes as "internal" (encapsulation).
        self._path = path
        # Keyed by lower-case name, so lookups ignore letter case.
        self._contacts: dict[str, Contact] = {}
        # Load whatever was saved last time.
        self._load()

    def _load(self) -> None:
        # If the file doesn't exist yet we simply start empty.
        if not self._path.exists():
            return
        # read_text() opens, reads and closes the file in one call.
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        # `**item` unpacks the dict as keyword arguments: Contact(name=..., phone=...).
        for item in raw:
            contact = Contact(**item)
            self._contacts[contact.name.lower()] = contact

    def save(self) -> None:
        # Make sure the folder exists before writing.
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Sorted output keeps the file stable and easy to diff.
        data = [asdict(c) for c in self.all()]
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, contact: Contact) -> None:
        key = contact.name.lower()
        # Refuse duplicates instead of silently overwriting.
        if key in self._contacts:
            raise KeyError(f"contact {contact.name!r} already exists")
        self._contacts[key] = contact

    def remove(self, name: str) -> Contact:
        # dict.pop raises KeyError when the key is missing; we re-raise a clearer one.
        try:
            return self._contacts.pop(name.lower())
        except KeyError:
            raise KeyError(f"no contact named {name!r}") from None

    def search(self, text: str) -> list[Contact]:
        # A list comprehension filters contacts whose name or email contains `text`.
        needle = text.lower()
        return [c for c in self.all() if needle in c.name.lower() or needle in c.email.lower()]

    def all(self) -> list[Contact]:
        # sorted() with a key function orders contacts alphabetically.
        return sorted(self._contacts.values(), key=lambda c: c.name.lower())

    # __len__ lets us call len(book), a small example of Python's "dunder" protocol.
    def __len__(self) -> int:
        return len(self._contacts)
