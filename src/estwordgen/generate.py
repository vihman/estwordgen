"""Pseudoword generation: a random walk over the n-gram model."""

import random

from .model import PAD, Model

MAX_ATTEMPTS = 10


def generate_word(model: Model, order: int = 3, length: int | None = None, rng: random.Random = random) -> str:
    """Return a word of `length` characters; without a length, one is drawn from the corpus.

    A walk stops early when the model has no continuation for a context; then it's retried.
    After MAX_ATTEMPTS the longest attempt is returned, so in rare cases the word is shorter.
    """
    if order not in model.counts:
        raise ValueError(f"order must be one of {model.orders}, got {order}")
    if length is None:
        length = model.sample_length(rng)
    if length < 1:
        raise ValueError(f"length must be positive, got {length}")
    best = ""
    for _ in range(MAX_ATTEMPTS):
        word = _walk(model, order, length, rng)
        if len(word) == length:
            return word
        best = max(best, word, key=len)
    return best


def generate_words(
    model: Model, order: int = 3, count: int = 20, length: int | None = None, rng: random.Random = random
) -> list[str]:
    return [generate_word(model, order, length, rng) for _ in range(count)]


def _walk(model: Model, order: int, length: int, rng: random.Random) -> str:
    padded = PAD * order
    while len(padded) - order < length:
        char = model.next_char(padded[-order:], rng)
        if char is None:
            break
        padded += char
    return padded[order:]


def score(model: Model, word: str, order: int = 1) -> float:
    """Probability of the model producing `word`; 0.0 if it contains an unseen n-gram."""
    counts = model.counts[order]
    padded = PAD * order + word
    probability = 1.0
    for i in range(len(word)):
        nexts = counts.get(padded[i : i + order], {})
        probability *= nexts.get(padded[i + order], 0) / (sum(nexts.values()) or 1)
    return probability
