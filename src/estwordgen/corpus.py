"""Reading word lists: one lemma per line, UTF-8."""

import re
from collections.abc import Iterable, Iterator
from pathlib import Path

SEPARATORS = " -_!"
"""Split a line into separate tokens. `_` marks compound boundaries in lemmad_piir.txt."""
OMITTED = "'"
"""Dropped as if it wasn't there."""
_LETTER = re.compile(r"\w")


def tokens(lines: Iterable[str]) -> Iterator[str]:
    """Yield the tokens of word-list lines. Raises ValueError on an unexpected character."""
    for line in lines:
        token = ""
        for char in line.rstrip("\n"):
            if char in OMITTED:
                continue
            if char in SEPARATORS:
                if token:
                    yield token
                token = ""
                continue
            if not _LETTER.fullmatch(char):
                raise ValueError(f"unexpected character {char!r} (U+{ord(char):04X}) in {line!r}")
            token += char
        if token:
            yield token


def read_tokens(path: Path) -> Iterator[str]:
    with path.open(encoding="utf-8") as f:
        yield from tokens(f)
