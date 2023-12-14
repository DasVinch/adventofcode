from __future__ import annotations

import os
import typing as typ
from tools import get_input
import tools

from tqdm import tqdm

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

MAPPER = {
    '?': 0,
    '.': 1,
    '#': 2
}

SAMPLE = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]


class Values:
    UNKNOWN = 0
    EMPTY = 1
    COLORED = 2

def presolve_datum(record: np.ndarray, hints: list[int]) -> None:
    n = len(record)
    n_hints = len(hints)
    total_pack = sum(hints) + n_hints - 1
    remainder = n - total_pack
    offset = 0
    for hint in hints:
        if hint > remainder:
            for kk in range(offset+remainder, offset+hint):
                record[kk] = Values.COLORED
        offset += hint + 1
    if remainder == 0:
        record[record == 1] = 0

def fill_left_position(hints: list[int], array: np.ndarray, index: int):
    starts = []
    cursor = index
    array[index:] = False
    for hh in hints:
        if hh == 0: # Don't create a starts for hints 0!
            break
        starts += [cursor]
        array[cursor:cursor + hh] = True
        cursor += hh + 1
    return starts

def position_complies(pos, known):
    return np.all(pos[known == Values.COLORED]) and not np.any(
        pos[known == Values.EMPTY])

import functools
@functools.cache
def position_complies_bit(pos: int, sure: int, surenot: int) -> bool:
    return (pos & surenot) == 0 and (~pos & sure) == 0



def tree_xplorer_count(hints: list[int], sure_int: int, surenot_int: int, n_pos: int):
    n_hints = len(hints)
    if n_hints == 0: # equiv to [0]
        return 1
    if n_pos == 0:
        return 1
    
    min_need = sum(hints) + len(hints) - 1 if len(hints) > 1 else hints[0]
    if min_need > n_pos:
        return 0
    
    tot_positions = 0

    hint = hints[0]
    if len(hints) > 1:
        tail_length = sum(hints[1:]) + len(hints) - 1
    else:
        tail_length = 0

    positioner = 2**hint-1 # 0b11...111
    for sp in range(0, n_pos - tail_length - hint + 1):
        if position_complies_bit(positioner, sure_int, surenot_int):
            tot_positions += 1
        positioner -= 2<<sp
        if sp < n_pos - hints[0]:
            positioner += 1<<(sp+hint)



    return tot_positions
    
    tail_length = sum(known) + len(known) - 2 - known[0]
    
    
    

class LineFillRepresenter:  # LPR

    def __init__(self,
                 hints: list[int],
                 length: int,
                 known: np.ndarray = None,
                 enumerate_only: bool = False):

        self.length = length
        self.hints = hints
        self.n_hints = len(self.hints)

        self.rpz = np.zeros(length, dtype=bool)

        self.starts = fill_left_position(self.hints, self.rpz, 0)

        if known is None:
            self.known = np.zeros(
                length, dtype=np.int8)  # 0: unknown, 1: empty, 2: colored
        else:
            self.known = known

        self.finished = False

        self.poss_positions = []
        self.poss_positions_counter = 0
        self.enumerate_only = enumerate_only

        self.init_enumerate_positions()
        self.conclusion = np.zeros(self.length, dtype=np.int8)
        if not self.enumerate_only:
            self.update_internal_conclusions()

    def next_position(self):
        # E.Z case: last square is free
        if len(self.starts) == 0: # empty case
            return False

        if not self.rpz[-1]:
            self.rpz[self.starts[-1]] = False
            self.rpz[self.starts[-1] + self.hints[-1]] = True
            self.starts[-1] += 1

            return True
        
        # We're gonna need some serious pruning.
        # Prune solution:
        # The first already illegal spot needs to pivot until legal.
        # then we perform a left fill. If all subsequent are legal, then we're good.
        # If any subsequent are illegal, we pivot again.

        pvt = self.n_hints - 2
        while pvt >= 0:
            # Look for a double space
            if not self.rpz[self.starts[pvt] + self.hints[pvt] + 1]:
                self.rpz[self.starts[pvt]] = False
                self.rpz[self.starts[pvt] + self.hints[pvt]] = True
                self.starts[pvt] += 1

                # Re-initialize to the right
                sts = fill_left_position(
                    self.hints[pvt + 1:], self.rpz,
                    self.starts[pvt] + self.hints[pvt] + 1)
                self.starts = self.starts[:pvt + 1] + sts

                return True
            pvt -= 1

        return False

    def init_enumerate_positions(self):
        while True:
            if position_complies(self.rpz, self.known):
                self.poss_positions_counter += 1
                #print(self.poss_positions_counter)
                if not self.enumerate_only:
                    self.poss_positions += [self.rpz.copy()]
            if not self.next_position():
                break

    def update_external_known(self, new_known_pos, new_known_value):
        self.known[new_known_pos] = new_known_value

        self.poss_positions = [
            poss for poss in self.poss_positions
            if position_complies(poss, self.known)
        ]

    def rework_knowns(self):
        # Assuming self.known has been set externally
        self.poss_positions = [
            poss for poss in self.poss_positions
            if position_complies(poss, self.known)
        ]

    def update_internal_conclusions(self):
        # Urgh fuck space
        matrixify = np.asarray(self.poss_positions)
        new_conclusion = self.conclusion * 0
        new_conclusion[np.all(matrixify, axis=0)] = 2
        new_conclusion[np.all(~matrixify, axis=0)] = 1

        new_finds = np.where(new_conclusion != self.conclusion)
        self.conclusion = new_conclusion

        if len(self.poss_positions) == 1:
            self.finished = True

        return new_finds
    

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug
        self.lines = lines

        self.datum = []

        for line in lines:
            split = line.split()
            self.datum += [(tools.make_cmapped_int_matrix([split[0]], MAPPER).squeeze(),
                            [int(s) for s in split[1].split(',')])]
            
        self.presolve()

    def presolve(self) -> None:
        for kk in range(len(self.datum)):
            s, nums = self.datum[kk]
            presolve_datum(s, nums)


    def solve1(self) -> int:
        self.lfrs1 = []
        for known, hints in tqdm(self.datum):
            self.lfrs1 += [LineFillRepresenter(hints, len(known), known, enumerate_only=True)]

        return sum([lfr.poss_positions_counter for lfr in self.lfrs1])
    

    def solve2(self) -> int:
        self.lfrs2 = []
        for known, hints in tqdm(self.datum):
            self.lfrs2 += [LineFillRepresenter(hints * 5, len(known) * 5 + 4,
                            (np.r_[known, Values.UNKNOWN][None,:] * np.ones((5,1), np.int32)).flatten()[:-1], enumerate_only=True)]

        return sum([lfr.poss_positions_counter for lfr in self.lfrs2])


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    #print(f'Real p2: {r.solve2()}')
