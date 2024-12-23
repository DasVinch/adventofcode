from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

from collections import Counter
from enum import Enum
import itertools
import functools

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    '029A',
    '980A',
    '179A',
    '456A',
    '379A',
]

class DPE(str, Enum):
    U = '^'
    D = 'v'
    L = '<'
    R = '>'
    A = 'A'

U, D, L, R, A = DPE.U, DPE.D, DPE.L, DPE.R, DPE.A

DIRKEYPADPOS: dict[DPE, tuple[int, int]] = {
    A: (0, 0),
    U: (-1, 0),
    R: (0, -1),
    D: (-1, -1),
    L: (-2, -1)
}
DIRKEYPADPOS_INV = {v: k for k, v in DIRKEYPADPOS.items()}

class NPE(str, Enum):
    NA = 'A'
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '9'


NUMKEYPADPOS: dict[NPE, tuple[int, int]] = {
    NPE.NA: (0, 0),
    NPE._0: (-1, 0),
    NPE._1: (-2, 1),
    NPE._2: (-1, 1),
    NPE._3: (0, 1),
    NPE._4: (-2, 2),
    NPE._5: (-1, 2),
    NPE._6: (0, 2),
    NPE._7: (-2, 3),
    NPE._8: (-1, 3),
    NPE._9: (0, 3),
}

NUMKEYPADPOS_INV = {v: k for k, v in NUMKEYPADPOS.items()}

class NumRobot:

    def __init__(self) -> None:
        self.ij = NUMKEYPADPOS[NPE.NA]

        self.sequence: list[str] = []

    def next_char(self, char: NPE) -> str:
        ti, tj = NUMKEYPADPOS[NPE(char)]
        i, j = self.ij
        out: list[DPE] = []

        di, dj = ti - i, tj - j
        if ti == -2:
            out += [U] * dj if dj > 0 else [D] * -dj
            out += [L] * -di  # di <= 0
        else:
            out += [R] * di if di > 0 else [L] * -di
            out += [U] * dj if dj > 0 else [D] * -dj

        self.ij = (ti, tj)

        out += [DPE.A]

        self.sequence += [''.join(out)]

        return ''.join(out)



    def apply_blindly_and_check_valid(self, charseq: str) -> bool:
        i, j = self.ij
        for c in charseq:
            if c == U:
                i, j = i, j + 1
            elif c == D:
                i, j = i, j - 1
            elif c == L:
                i, j = i - 1, j
            elif c == R:
                i, j = i + 1, j
            if NUMKEYPADPOS_INV.get((i, j), None) == None:
                return False

        return True



class DirRobot:

    def __init__(self) -> None:
        self.ij = DIRKEYPADPOS[DPE.A]

        self.sequence: list[str] = []

        self.debug = False


    def next_char(self, char: DPE) -> str:
        ti, tj = DIRKEYPADPOS[char]
        i, j = self.ij
        out: list[str] = []

        di, dj = ti - i, tj - j
        if tj == -1:  # Move j first
            out += [U] * dj if dj > 0 else [D] * -dj
            out += [R] * di if di > 0 else [L] * -di
        else:
            out += [R] * di if di > 0 else [L] * -di
            out += [U] * dj if dj > 0 else [D] * -dj

        self.ij = (ti, tj)

        out += [DPE.A]

        self.sequence += [''.join(out)]

        return ''.join(out)

    def apply_blindly_and_check_valid(self, charseq: str) -> bool:
        i, j = self.ij
        for c in charseq:
            if c == U:
                i, j = i, j + 1
            elif c == D:
                i, j = i, j - 1
            elif c == L:
                i, j = i - 1, j
            elif c == R:
                i, j = i + 1, j
            if DIRKEYPADPOS_INV.get((i, j), None) == None:
                if self.debug:
                    import pdb;pdb.set_trace()
                return False

        return True

def seq_to_pairs_of_transitions(s: str) -> list[tuple[DPE,DPE]]:
    out = [(DPE.A, DPE(s[0]))]
    for k in range(1, len(s)):
        out += [(DPE(s[k-1]), DPE(s[k]))]

    return out

def code_to_NPE_transition_seq(s: str) -> list[tuple[NPE, NPE]]:
    out = [(NPE.NA, NPE(s[0]))]
    for k in range(1, len(s)):
        out += [(NPE(s[k-1]), NPE(s[k]))]

    return out


def optimal_seq_for_numbot_transition(depth: int, t: tuple[NPE, NPE]) -> Counter[DPE]:
    bot = NumRobot()
    bot.next_char(t[0])
    move = bot.next_char(t[1])
    bot.next_char(t[0])
    
    best_perm_total = 0
    best_counter: Counter[DPE]
    for perm in itertools.permutations(move[:-1]):
        pp = ''.join(perm) + 'A'
        if bot.apply_blindly_and_check_valid(pp):
            new_counter: Counter[DPE] = Counter()
            #print(pp)
            tseq_for_pp = seq_to_pairs_of_transitions(pp)
            for transition in tseq_for_pp:
                recursor = optimal_dirseq_through_bots(depth, transition)
                for c ,val in recursor.items():
                    if c not in new_counter:
                        new_counter[c] = 0
                    new_counter[c] += val
            total_this_perm = sum(new_counter.values())
            if best_perm_total == 0 or total_this_perm < best_perm_total:
                best_perm_total = total_this_perm
                best_counter = new_counter
    
    return best_counter

@functools.cache
def optimal_dirseq_through_bots(depth: int, t: tuple[DPE, DPE]) -> Counter[DPE]:
    bot = DirRobot()
    bot.next_char(t[0])
    move = bot.next_char(t[1])
    bot.next_char(t[0])
    
    if depth == 1:
        return Counter((DPE(m) for m in move))

    best_perm_total = 0
    best_counter: Counter[DPE]
    for perm in itertools.permutations(move[:-1]):
        pp = ''.join(perm) + 'A'
        if bot.apply_blindly_and_check_valid(pp):
            new_counter: Counter[DPE] = Counter()
            #print(pp)
            tseq_for_pp = seq_to_pairs_of_transitions(pp)
            for transition in tseq_for_pp:
                recursor = optimal_dirseq_through_bots(depth-1, transition)
                for c ,val in recursor.items():
                    if c not in new_counter:
                        new_counter[c] = 0
                    new_counter[c] += val
            total_this_perm = sum(new_counter.values())
            if best_perm_total == 0 or total_this_perm < best_perm_total:
                best_perm_total = total_this_perm
                best_counter = new_counter
    
    return best_counter





class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.codes = lines

    def nsolve1(self, depth: int = 2) -> tuple[int, int]:
        total = 0
        chksum = 0
        for code in self.codes:
            ctr = Counter()
            seq = code_to_NPE_transition_seq(code)

            for t in seq:
                tctr = optimal_seq_for_numbot_transition(depth, t)
                ctr.update(tctr) # update is additive for a counter yay.

            s = sum(ctr.values())
            total += s
            chksum += int(code[:-1]) * s

        return chksum, total

    def solve1(self) -> tuple[int, int]:
        return self.nsolve1(2)

    def solve2(self) -> tuple[int, int]:
        return self.nsolve1(25)




if __name__ == "__main__":
    
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
