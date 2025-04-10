import bisect
import random
from collections import deque
"""
Extract original code from class. 
"""


def get_word(quick_dict, depth, length):
    word = get_start(quick_dict, depth)
    while len(word) < length:
        # TODO: sometimes key not found
        try:
            prev_slice = quick_dict[word[len(word) - depth:]]
            next_char = get_character(prev_slice)
            word += next_char
        except KeyError as e:
            break
    return word


def get_start(quick_dict, depth):
    char_que = deque('#' * depth, maxlen = depth)
    for i in range(depth):
        try:
            ''' TODO: sometimes key not found '''
            char_que.append(get_character(quick_dict[''.join(l for l in char_que)]))
        except KeyError as e:
            break
    chars = ''.join(l for l in char_que)
    return chars


def get_character(qd_slice):
    rnd = random.random() * qd_slice[0]
    character = qd_slice[1][bisect.bisect_left(qd_slice[2], rnd)]
    return character
