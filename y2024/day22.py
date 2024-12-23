from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '1',
    '10',
    '100',
    '2024',
]

SAMPLE2 = [
    '1',
    '2',
    '3',
    '2024',
]

MOD = 16777216

def salt(n: int, reps: int = 1):
    for _ in range(reps):
        n = ((n * 64) ^ n ) % MOD
        n = ((n // 32) ^ n ) % MOD
        n = ((n * 2048) ^ n ) % MOD
    return n


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.nums = [int(l) for l in lines]


    def solve1(self) -> int:
        total = 0
        for n in self.nums:
            total += salt(n, 2000)
        
        return total
        

    def solve2(self) -> int:
        alldicts = {}
        allsequences = set()
        # Make a map of 4-differential substrings x monkey x value?
        for k, init in enumerate(self.nums):
            substr: dict[tuple[int,int,int,int], list[int]] = {}
            arr = []
            val = init
            for _ in range(3):
                nv = salt(val)
                arr += [nv % 10 - val % 10]
                val = nv
            for _ in range(1997):
                nv = salt(val)
                arr += [nv % 10 - val % 10]
                val = nv
                assert len(arr) == 4
                seq = tuple(arr)
                if not seq in substr:
                    substr[seq] = nv % 10
                    allsequences.add(seq)
                arr.pop(0)

            alldicts[k] = substr

        best_seq = None
        best_value = -1
        for seq in allsequences:
            score = 0
            for subdict in alldicts.values():
                score += subdict.get(seq, 0)
            if score > best_value:
                best_value = score
                best_seq = seq

        print(best_seq, best_value)

        return best_value


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t2 = Day(SAMPLE2, True)
    print(f'Test p2: {t2.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)