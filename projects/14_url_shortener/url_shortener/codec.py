"""Base62 encoding: turns database ids into short codes (1 -> "1", 62 -> "10")."""

import string

# 0-9, a-z, A-Z = 62 URL-safe characters.
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(ALPHABET)


def encode(number: int) -> str:
    if number < 0:
        raise ValueError("number must be >= 0")
    if number == 0:
        return ALPHABET[0]
    chars: list[str] = []
    while number:
        # divmod returns (quotient, remainder) in one step.
        number, rem = divmod(number, BASE)
        chars.append(ALPHABET[rem])
    return "".join(reversed(chars))


def decode(code: str) -> int:
    number = 0
    for ch in code:
        number = number * BASE + ALPHABET.index(ch)
    return number
