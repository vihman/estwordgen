# estwordgen

Estonian pseudoword generator. It learns which character follows each 1–3 character context in a list of Estonian lemmas, then makes new words by a random walk over those counts (a character n-gram Markov chain). It started as a bachelor thesis in 2013. The live site is <https://wordgen.vihman.com>.

## Use

Python 3.13+, no dependencies.

```shell
pip install -e .                                 # or: pip install git+https://github.com/vihman/estwordgen@v2.0.0
estwordgen generate                              # 20 words, trigram model, lengths drawn from the corpus
estwordgen generate -c lemmad_piir -n 2 -l 8     # compound-split corpus, digram model, 8 letters
estwordgen score kultuur kxzqw                   # probability of the model producing each word
```

```python
from estwordgen import generate_words, load_model

generate_words(load_model("lemmad"), order=3, count=5, length=8)
```

## Corpora

| Name | Source | Content |
| --- | --- | --- |
| `lemmad` | `data/lemmad.txt` | Estonian lemmas, one per line |
| `lemmad_piir` | `data/lemmad_piir.txt` | The same lemmas with compound boundaries marked by `_` (`aabitsa_jünger`). The parts are learned as separate words. |

Space, `-`, `_` and `!` split a line into separate words, and `'` is ignored.

## Models

`estwordgen build` turns each word list into `src/estwordgen/models/<corpus>.json`, which ships with the package. A test checks that the committed models match the word lists, so rebuild and commit them after changing either.

```json
{
 "format": 1,
 "corpus": "lemmad",
 "source_sha256": "<sha256 of data/lemmad.txt>",
 "counts": {"3": {"###": {"k": 16015, ...}, "kul": {"t": 426, ...}, ...}, "2": {...}, "1": {...}},
 "lengths": {"8": 13734, ...}
}
```

- `counts[order][context][next]` is how many times `next` followed `context`. Words are padded at the start with `#`, so `###` (order 3) is the start of a word.
- `lengths[n]` is how many words had `n` letters. Generation draws a length from it when none is given.

There is no end-of-word state: a word ends when it reaches its length. If the model has no continuation for a context, the walk is retried, and in rare cases the word comes out shorter.

## Development

```shell
python3 -m venv .venv && .venv/bin/pip install -e . pytest ruff
.venv/bin/pytest
pre-commit install
```

Version 1.0.0 (git tag `v1.0.0`) is the original 2013 code: a CGI web page and pickled models.
