import json
import pickle

from extract.search import get_word


def handler(event, context):
    how = event['how']
    len = event['len']
    count = 20
    with open(f'resource/{how}.pck', mode='rb') as f:
        quick_dict = pickle.load(f)
    depth = 2 if how.startswith("qd2g_") else 3
    result = []
    for _ in range(count):
        word = get_word(quick_dict, depth, len)
        result.append(word)
    return json.dumps(result)