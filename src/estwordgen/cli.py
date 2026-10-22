"""Command line: estwordgen build | generate | score"""

import argparse
import hashlib
import random
from pathlib import Path

from .corpus import read_tokens
from .generate import generate_words, score
from .model import CORPORA, build, load_model


def cmd_build(args: argparse.Namespace) -> None:
    args.out.mkdir(parents=True, exist_ok=True)
    for corpus in CORPORA:
        source = args.data / f"{corpus}.txt"
        sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
        model = build(read_tokens(source), corpus=corpus, source_sha256=sha256)
        model.save(args.out / f"{corpus}.json")
        print(f"{source} -> {args.out / f'{corpus}.json'}")


def cmd_generate(args: argparse.Namespace) -> None:
    rng = random.Random(args.seed)
    for word in generate_words(load_model(args.corpus), args.order, args.count, args.length, rng):
        print(word)


def cmd_score(args: argparse.Namespace) -> None:
    model = load_model(args.corpus)
    for word in args.words:
        print(f"{word}\t{score(model, word, args.order):.3g}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="estwordgen", description=__doc__)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("build", help="build the bundled models from the word lists")
    p.add_argument("--data", type=Path, default=Path("data"), help="word list directory (default: %(default)s)")
    p.add_argument("--out", type=Path, default=Path("src/estwordgen/models"), help="default: %(default)s")
    p.set_defaults(func=cmd_build)

    corpus = argparse.ArgumentParser(add_help=False)
    corpus.add_argument("-c", "--corpus", choices=CORPORA, default="lemmad", help="default: %(default)s")

    p = sub.add_parser("generate", parents=[corpus], help="generate pseudowords")
    p.add_argument("-n", "--order", type=int, choices=(1, 2, 3), default=3, help="context length (default: 3)")
    p.add_argument("-l", "--length", type=int, help="word length (default: drawn from the corpus)")
    p.add_argument("--count", type=int, default=20, help="default: %(default)s")
    p.add_argument("--seed", type=int, help="random seed, for repeatable output")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("score", parents=[corpus], help="probability of the model producing each word")
    p.add_argument("words", nargs="+")
    p.add_argument("-n", "--order", type=int, choices=(1, 2, 3), default=1, help="context length (default: 1)")
    p.set_defaults(func=cmd_score)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
