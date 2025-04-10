import pickle
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, conint
from fastapi.middleware.cors import CORSMiddleware

from extract.graphcollection import GraphCollection
from extract.search import get_word

origins = [
    "http://localhost",
    "https://*",
]

# Only these headers are allowed
headers = ["Content-Type", "Authorization"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["PUT"],
    allow_headers=headers,
)


class Model(BaseModel):
    len: conint(ge=2, le=50)
    how: Literal[
        "qd2g_f", # "dgf" digrammid (2)
        "qd3g_f", # "tgf", # trigrammid (3)
        "qd2g_h", # "dgh", # tükeldatud liitsõnad digrammid (2)
        "qd3g_h", # "tgh"  # tükeldatud liitsõnad trigrammid (3)
    ]


@app.put("/api/")
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
