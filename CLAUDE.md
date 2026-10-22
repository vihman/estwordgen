# CLAUDE.md

Estonian pseudoword generator: character n-gram Markov chains (orders 1–3) trained on Estonian lemma lists. A pure-Python package with no runtime dependencies. User-facing docs are in [README.md](README.md).

## Scope

This repo only builds models and generates words. The website (wordgen.vihman.com: Lambda handler, static page, terraform) lives in `../tf.aws`. It installs this package pinned to a git tag (`wordgen-api/requirements.txt`) and maps the API's `how` values (`qd3g_f` etc.) to `(corpus, order)`. Don't add web or deploy code here. Changing the public API (`load_model`, `generate_word(s)`, `score`, `CORPORA`) or the model format affects that handler.

## Layout

- `src/estwordgen/corpus.py` — word list to tokens. Splits on space, `-`, `_` and `!`, drops `'`, and raises on any other non-`\w` character.
- `src/estwordgen/model.py` — `build()` counts n-grams into a `Model`. Also JSON save/load and `load_model(corpus)`, which is cached and bundled-only. Cumulative tables for `bisect` sampling are derived lazily.
- `src/estwordgen/generate.py` — random walk (`generate_word(s)`) and `score()`.
- `src/estwordgen/cli.py` — `estwordgen build | generate | score`.
- `src/estwordgen/models/*.json` — **build output, committed**, shipped as package data.
- `data/*.txt` — training word lists, not packaged.

## Commands

```shell
python3 -m venv .venv && .venv/bin/pip install -e . pytest ruff
.venv/bin/pytest                    # ~2 s
.venv/bin/ruff check . && .venv/bin/ruff format --check .
.venv/bin/estwordgen build          # run from the repo root; rewrites src/estwordgen/models/
```

## Rules

- After changing `data/`, `corpus.py` or `build()`, run `estwordgen build` and commit the models. `test_bundled_models_are_up_to_date` fails otherwise.
- Model JSON must stay deterministic: sorted keys, `indent=1`, `ensure_ascii=False`. Rebuilding unchanged input must give byte-identical files.
- Bump `FORMAT` in `model.py` for incompatible changes to the model file.
- Releases are git tags `vX.Y.Z` matching `version` in `pyproject.toml`; tf.aws pins them. `v1.0.0` is the original 2013 CGI version.

## Behaviour worth knowing

- Padding: an order-k context is padded with k `#`. Generated words never contain `#`.
- There is no end-of-word state. Length is given or drawn from `Model.lengths`, and the walk stops there. If a context has no continuation, the walk is retried up to `MAX_ATTEMPTS`, then the longest attempt is returned, which can be shorter than asked.
- Compared with v1's pickles: order-3 counts and length tables are identical. Orders 1–2 now also count the n-grams at the end of each word, which v1's fixed 4-character window missed. `score()` returns 0.0 for an unseen n-gram, where v1 silently skipped it.
