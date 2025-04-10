import pickle
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, conint

from extract.graphcollection import GraphCollection
from extract.search import get_word

app = FastAPI()


class Model(BaseModel):
    len: conint(ge=2, le=50)
    how: Literal[
        "qd2g_f", # "dgf" digrammid (2)
        "qd3g_f", # "tgf", # trigrammid (3)
        "qd2g_h", # "dgh", # tükeldatud liitsõnad digrammid (2)
        "qd3g_h", # "tgh"  # tükeldatud liitsõnad trigrammid (3)
    ]


@app.put("/wordgen/")
async def read_item(params: Model):
    result = await get_words(params)
    return result


async def get_words(params):
    count = 20
    with open(f'resource/{params.how}.pck', mode='rb') as f:
        quick_dict = pickle.load(f)
    depth = 2 if params.how.startswith("qd2g_") else 3
    result = []
    for _ in range(count):
        word = get_word(quick_dict, depth, params.len)
        result.append(word)
    return result
