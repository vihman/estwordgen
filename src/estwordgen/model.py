"""Character n-gram model: counting, JSON storage and sampling tables."""

import bisect
import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache, cached_property
from importlib import resources
from pathlib import Path
from random import Random

PAD = "#"
"""Pads the start of a word, so the first context of an order-3 model is '###'."""
FORMAT = 1
CORPORA = ("lemmad", "lemmad_piir")
"""Models bundled with the package, built from data/<name>.txt."""

type Counts = dict[str, dict[str, int]]
"""context -> next character -> count"""


@dataclass(frozen=True)
class _Table:
    """Cumulative counts for sampling with bisect."""

    values: list
    cumulative: list[int]

    @classmethod
    def from_counts(cls, counts: dict) -> "_Table":
        values, cumulative, total = [], [], 0
        for value, count in counts.items():
            total += count
            values.append(value)
            cumulative.append(total)
        return cls(values, cumulative)

    def sample(self, rng: Random):
        return self.values[bisect.bisect_right(self.cumulative, rng.random() * self.cumulative[-1])]


@dataclass(frozen=True)
class Model:
    counts: dict[int, Counts]
    """order -> context -> next character -> count. Contexts are padded with PAD."""
    lengths: dict[int, int]
    """token length -> count"""
    corpus: str = ""
    source_sha256: str = ""

    @property
    def orders(self) -> list[int]:
        return sorted(self.counts)

    @cached_property
    def _tables(self) -> dict[int, dict[str, _Table]]:
        return {
            order: {context: _Table.from_counts(nexts) for context, nexts in counts.items()}
            for order, counts in self.counts.items()
        }

    @cached_property
    def _length_table(self) -> _Table:
        return _Table.from_counts(self.lengths)

    def next_char(self, context: str, rng: Random) -> str | None:
        """Sample the character following `context`; its length is the order. None if unseen."""
        table = self._tables[len(context)].get(context)
        return table.sample(rng) if table else None

    def sample_length(self, rng: Random) -> int:
        return self._length_table.sample(rng)

    def to_json(self) -> str:
        data = {
            "format": FORMAT,
            "corpus": self.corpus,
            "source_sha256": self.source_sha256,
            "counts": {str(order): counts for order, counts in self.counts.items()},
            "lengths": {str(length): count for length, count in self.lengths.items()},
        }
        return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n"

    @classmethod
    def from_json(cls, text: str) -> "Model":
        data = json.loads(text)
        if data.get("format") != FORMAT:
            raise ValueError(f"unsupported model format {data.get('format')!r}")
        return cls(
            counts={int(order): counts for order, counts in data["counts"].items()},
            lengths={int(length): count for length, count in data["lengths"].items()},
            corpus=data["corpus"],
            source_sha256=data["source_sha256"],
        )

    def save(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Model":
        return cls.from_json(path.read_text(encoding="utf-8"))


def build(tokens: Iterable[str], max_order: int = 3, corpus: str = "", source_sha256: str = "") -> Model:
    """Count, for every order 1..max_order, which character follows each context."""
    counts = {order: defaultdict(Counter) for order in range(1, max_order + 1)}
    lengths = Counter()
    for token in tokens:
        lengths[len(token)] += 1
        for order, order_counts in counts.items():
            padded = PAD * order + token
            for i in range(len(token)):
                order_counts[padded[i : i + order]][padded[i + order]] += 1
    return Model(
        counts={order: {context: dict(nexts) for context, nexts in c.items()} for order, c in counts.items()},
        lengths=dict(lengths),
        corpus=corpus,
        source_sha256=source_sha256,
    )


@cache
def load_model(corpus: str) -> Model:
    """Load a bundled model by name (see CORPORA). Cached, so it's parsed once per process."""
    if corpus not in CORPORA:
        raise ValueError(f"unknown corpus {corpus!r}, expected one of {CORPORA}")
    return Model.from_json((resources.files("estwordgen") / "models" / f"{corpus}.json").read_text("utf-8"))
