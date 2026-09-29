import pickle
from functools import lru_cache
from pathlib import Path

from extract.search import get_word

RESOURCE_DIR = Path(__file__).parent / "resource"
ALLOWED = {"qd2g_f", "qd3g_f", "qd2g_h", "qd3g_h"}
COUNT = 20


@lru_cache(maxsize=None)          # loaded once per warm environment, per model
def load_model(how: str):
    with open(RESOURCE_DIR / f"{how}.pck", "rb") as f:
        return pickle.load(f)


def handler(event, context):
    how = event.get("how")
    if how not in ALLOWED:
        return {"error": "invalid 'how'"}
    try:
        length = max(2, min(int(event.get("len")), 50))
    except (TypeError, ValueError):
        return {"error": "invalid 'len'"}

    quick_dict = load_model(how)
    depth = 2 if how.startswith("qd2g_") else 3
    return [get_word(quick_dict, depth, length) for _ in range(COUNT)]