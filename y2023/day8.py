from __future__ import annotations

import os
from tools import get_input
import typing as typ
import re
import math

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)',
]

SAMPLE2 = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)',
]

SAMPLE3 = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)',
]


def parse_graph(lines: list[str]) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}

    myre = '^([1-9A-Z]+) = \(([1-9A-Z]+), ([1-9A-Z]+)\)$'

    for line in lines:
        m = re.match(myre, line)
        assert m is not None
        g = m.groups()
        out[g[0]] = (g[1], g[2])

    return out


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.instr = lines[0]
        self.n_instr = len(self.instr)

        self.path = parse_graph(lines[2:])

        self.debug = debug

    def solve1(self) -> int:
        p = 0
        node = 'AAA'
        while node != 'ZZZ':
            instr = self.instr[p % len(self.instr)]
            node = self.path[node][0] if instr == 'L' else self.path[node][1]
            p = p + 1

        return p

    def cycle_finder_all(self):
        self.cycle_params = {}

        self.start_nodes = {k for k in self.path if k.endswith('A')}
        self.end_nodes = {k for k in self.path if k.endswith('Z')}

        for sn in self.start_nodes:
            node = sn
            t = 0
            T = 0
            states: dict[tuple[str, int], int] = {}

            while True:
                if (node, t) in states:
                    if self.debug:
                        print(f'Cycle! {node} {t} -- {states[(node,t)]}, {T}')
                        z_members = {s: states[s] for s in states if states[s] >= states[(node,t)] and s[0].endswith('Z')}
                        print(f'    Z members: {z_members}')
                    break

                states[((node,t))] = T

                node = self.path[node][0] if self.instr[t] == 'L' else self.path[node][1]
                T += 1
                t = T % self.n_instr

    def solve2(self) -> int:
        self.cycle_finder_all()
        return 0


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(f'Test p1: {t.solve1()}')
    t2 = Day(SAMPLE2)
    print(f'Test p1: {t2.solve1()}')

    t3 = Day(SAMPLE3, True)
    print(f'T3 p2: {t3.solve2()}')

    r = Day(REAL, True)
    print(f'Real p1: {r.solve1()}')
    print(f'Test p2: {r.solve2()}')
    #print(f'Real p2: {r.solve2()}')
