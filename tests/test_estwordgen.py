import hashlib
import random
from pathlib import Path

import pytest

from estwordgen import CORPORA, Model, build, generate_word, generate_words, load_model, score
from estwordgen.cli import main
from estwordgen.corpus import read_tokens, tokens
from estwordgen.model import PAD

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "src" / "estwordgen" / "models"


def test_tokens_split_and_omit():
    lines = ["aabitsa_jünger\n", "a-vitamiin\n", "O'Neill\n", "kaks sõna!\n", "-\n"]
    assert list(tokens(lines)) == ["aabitsa", "jünger", "a", "vitamiin", "ONeill", "kaks", "sõna"]


def test_tokens_reject_unexpected_character():
    with pytest.raises(ValueError, match=r"U\+002E"):
        list(tokens(["a.b\n"]))


def test_build_counts():
    model = build(["aba", "ab"], max_order=2)
    assert model.counts[1] == {"#": {"a": 2}, "a": {"b": 2}, "b": {"a": 1}}
    assert model.counts[2] == {"##": {"a": 2}, "#a": {"b": 2}, "ab": {"a": 1}}
    assert model.lengths == {3: 1, 2: 1}


def test_json_round_trip(tmp_path):
    model = build(["kass", "koer"], corpus="test", source_sha256="abc")
    model.save(tmp_path / "m.json")
    assert Model.load(tmp_path / "m.json") == model


def test_unknown_format_is_rejected():
    with pytest.raises(ValueError, match="format"):
        Model.from_json('{"format": 99}')


@pytest.mark.parametrize("corpus", CORPORA)
def test_bundled_models_are_up_to_date(corpus):
    """The committed models must be what `estwordgen build` makes from data/ now."""
    source = ROOT / "data" / f"{corpus}.txt"
    sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    built = build(read_tokens(source), corpus=corpus, source_sha256=sha256)
    assert built.to_json() == (MODELS / f"{corpus}.json").read_text("utf-8")


def test_load_model_is_cached_and_validates_name():
    assert load_model("lemmad") is load_model("lemmad")
    with pytest.raises(ValueError):
        load_model("../../etc/passwd")


@pytest.mark.parametrize("corpus", CORPORA)
@pytest.mark.parametrize("order", [1, 2, 3])
@pytest.mark.parametrize("length", [1, 2, 8, 50])
def test_generated_words(corpus, order, length):
    for word in generate_words(load_model(corpus), order, 20, length):
        assert PAD not in word
        assert 0 < len(word) <= length


def test_words_have_requested_length_almost_always():
    words = generate_words(load_model("lemmad"), 3, 1000, 8)
    assert sum(len(w) == 8 for w in words) / len(words) > 0.99


def test_length_drawn_from_corpus_when_omitted():
    model = load_model("lemmad")
    lengths = {len(generate_word(model, rng=random.Random(i))) for i in range(200)}
    assert len(lengths) > 5


def test_seed_makes_output_repeatable():
    model = load_model("lemmad")
    assert generate_words(model, rng=random.Random(1)) == generate_words(model, rng=random.Random(1))


def test_dead_end_returns_longest_attempt_without_padding():
    model = build(["ab"], max_order=2)  # nothing follows "ab"
    assert generate_word(model, 2, 5) == "ab"


def test_invalid_arguments():
    model = build(["ab"], max_order=2)
    with pytest.raises(ValueError):
        generate_word(model, 3, 5)
    with pytest.raises(ValueError):
        generate_word(model, 2, 0)


def test_score():
    model = build(["ab", "ac"], max_order=1)
    assert score(model, "ab") == pytest.approx(0.5)  # P(a|#) = 1, P(b|a) = 1/2
    assert score(model, "ax") == 0.0
    assert score(load_model("lemmad"), "kultuur") > score(load_model("lemmad"), "kxzqw")


def test_cli_generate(capsys):
    main(["generate", "-c", "lemmad_piir", "-n", "2", "-l", "6", "--count", "3", "--seed", "1"])
    words = capsys.readouterr().out.split()
    assert len(words) == 3 and all(len(w) == 6 for w in words)


def test_cli_build_is_deterministic(tmp_path):
    main(["build", "--data", str(ROOT / "data"), "--out", str(tmp_path)])
    for corpus in CORPORA:
        assert (tmp_path / f"{corpus}.json").read_bytes() == (MODELS / f"{corpus}.json").read_bytes()
