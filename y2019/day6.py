from __future__ import annotations

import typing as typ
import tools as tl

import functools

SAMPLE: list[str] = [
'COM)B',
'B)C',
'C)D',
'D)E',
'E)F',
'B)G',
'G)H',
'D)I',
'E)J',
'J)K',
'K)L',
]

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = dict[str, str] # TODO

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        orbits: T_DATA = {}
        for line in input:
            a,b = line.split(')')
            orbits[b] = a

        return orbits
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

    def solve1(self) -> int:

        @functools.cache
        def count(node: str) -> int:
            if node == 'COM':
                return 0
            return count(self.data[node]) + 1

        return sum([count(a) for a in self.data])


    def solve2(self) -> int:
        
        def parentage(node: str) -> list[str]:
            if node == 'COM':
                return []
            s = parentage(self.data[node])
            s.append(self.data[node])
            return s
        
        if 'YOU' in self.data:
            a,b = 'YOU', 'SAN'
        else:
            a,b = 'J', 'K'
        p1 = parentage(a)
        p2 = parentage(b)

        pp1 = set(p1).difference(set(p2))
        pp2 = set(p2).difference(set(p1))
        
        import pdb; pdb.set_trace()

        if b in p1 or a in p2:
            return len(pp1) + len(pp2) - 2

        return len(pp1) + len(pp2)