import typing as typ

import hashlib

SAMPLESALT = b'abc'

REALSALT = b'ahsbgdzn'

def make_md5(salt: bytes, count: int, morehashing: bool = False) -> str:
    hash = hashlib.md5(salt + str(count).encode('ascii')).hexdigest()

    if morehashing:
        for _ in range(2016):
            hash = hashlib.md5(hash.encode('ascii')).hexdigest()


    return hash


def find_kplets(hash: str, n:int, first: bool = True) -> typ.Set[str]:
    which = set()
    for k in range(len(hash) - n + 1):
        char = hash[k]
        if char in which:
            continue
        can = True
        for ii in range(1, n):
            can = can and hash[k+ii] == char
            if not can:
                break

        if can:
            which.add(char)
            if first:
                break

    return which

def solve(salt: bytes, N: int = 64, morehashing: bool = False):
    counter = 0
    tri_deck: typ.Dict[int, typ.Set[str]] = {}
    keys: typ.Set[int] = set()

    counterbreak = 0

    while True:
        hash = make_md5(salt, counter, morehashing=morehashing)
        if len(p5 := find_kplets(hash, 5, False)) > 0:
            to_remove = set()
            for idx, tris in tri_deck.items():
                if len(p5.intersection(tris)) > 0:
                    keys.add(idx)
                    print(f'Counter {idx} makes key #{len(keys)} (validated by {counter})')
        
        if len(p3 := find_kplets(hash, 3, True)) > 0:
            tri_deck[counter] = p3
        
        if counter - 1000 in tri_deck:
            tri_deck.pop(counter-1000)

        if len(keys) >= N:
            if counterbreak == 0:
                counterbreak = counter + 1002
            elif counter >= counterbreak:
                break
        counter += 1

    print(f'Halting counter: {counter}')

    lkeys = list(keys)
    lkeys.sort()

    print(lkeys[N-1])

    return lkeys

