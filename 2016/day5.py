import typing as typ

from tools import get_input
import numpy as np


import hashlib

from tqdm import tqdm

SAMPLE = b'abc'
REAL = b'abbhdwsy'


def md5er(key):
    count = 0
    success = 0
    pw = []

    def tgen():
        while success < 8:
            yield

    for _ in tqdm(tgen()):
        h = hashlib.md5(key + str(count).encode('ascii'))
        if h.hexdigest().startswith('00000'):
            pw += h.hexdigest()[5]
            success += 1
        count += 1


    return ''.join(pw)

def more_md5er(key):
    count = 0
    success = 0
    pw = ['.'] * 8

    def tgen():
        while success < 8:
            yield

    for _ in tqdm(tgen()):
        h = hashlib.md5(key + str(count).encode('ascii')).hexdigest()
        if h.startswith('00000') and h[5] <= '7' and pw[int(h[5])] == '.':
            pw[int(h[5])] = h[6]
            print('\n', ''.join(pw))
            success += 1
        count += 1


    return ''.join(pw)