from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

#REAL = tl.get_input(DAYDAY, 2024)[0]

SAMPLE = ['729,0,0', '0,1,5,4,3,0']
SAMPLE2 = ['2024,0,0', '0,3,5,4,3,0']
REAL = ['32916674,0,0', '2,4,1,1,7,5,0,3,1,4,4,0,5,5,3,0']

'''
2 4 <-- B = A % 8 # b last octal digit of a 0 <= B < 8
1 1 <-- B = B ^ 1 # b = 3 bits of a flip last bit 0 <= B < 8
7 5 <-- C = A // 2**B # c = a / 1 up to a / 128 
# Only the last 3 bits of C matter since they eventually lead to OUT B % 8
since A drops 0 to 7 bits... at most 10 bits of A matter? Which generate... 4 outs?



1 4 <-- B = B ^ 4 # 3 bits of a flip first and last
4 0 <-- B = B ^ C # b xor c last 3 bits
5 5 <-- OUT B % 8
0 3 <-- A = A // 8 # A drop an octal digit
3 0 <-- JMP 0 (if A > 0)
'''

def common_prefix(l1: list[int], l2: list[int]) -> list[int]:
    if len(l1) == 0 or len(l2) == 0:
        return []
    if l1[0] == l2[0]:
        return [l1[0]] + common_prefix(l1[1:], l2[1:])
    else:
        return []

class Computer:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.ip = 0

    def find_combo(self, combo: int) -> int:
        if combo <= 3:
            return combo
        if combo == 4:
            return self.a
        if combo == 5:
            return self.b
        if combo == 6:
            return self.c

        raise

    def instruction(self, ins: int, ope: int) -> int | None:
        if ins == 0:
            self.a = self.a // 2**self.find_combo(ope)
        elif ins == 1:
            self.b = self.b ^ ope
        elif ins == 2:
            self.b = self.find_combo(ope) % 8
        elif ins == 3 and self.a != 0:
            self.ip = ope - 2
        elif ins == 4:
            self.b = self.b ^ self.c
        elif ins == 5:
            return self.find_combo(ope) % 8
        elif ins == 6:
            self.b = self.a // 2**self.find_combo(ope)
        elif ins == 7:
            self.c = self.a // 2**self.find_combo(ope)

        return None

from dataclasses import dataclass

@dataclass
class PrefixableMatch:
    a: int
    tail_match: list[int]

def insert_sorted(l: list[PrefixableMatch], p: PrefixableMatch):
    if len(l) == 0:
        l.insert(0, p)
    for i in range(len(l)):
        pp = l[i]
        if len(p.tail_match) > len(pp.tail_match) or (len(p.tail_match) == len(pp.tail_match) and p.a < pp.a):
            l.insert(i, p)
            return
    l.append(p)

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.abc = [int(c) for c in lines[0].split(',')]
        self.strip = [int(c) for c in lines[1].split(',')]

    def solve1(self) -> str:
        self.comp1 = Computer(*self.abc)
        output = []
        while self.comp1.ip < len(self.strip):
            k = self.comp1.instruction(self.strip[self.comp1.ip], self.strip[self.comp1.ip+1])
            self.comp1.ip += 2
            if isinstance(k, int):
                output += [k]

        return ','.join([str(k) for k in output])

    def run_comp(self, a: int) -> list[int]:
        comp = Computer(a, 0, 0)
        output = []
        while comp.ip < len(self.strip):
            k = comp.instruction(self.strip[comp.ip], self.strip[comp.ip+1])
            comp.ip += 2
            if isinstance(k, int):
                output += [k]

        return output

    def solve2(self) -> int:
        candidate_prefixes: list[PrefixableMatch] = [PrefixableMatch(0, [])]

        while len(candidate_prefixes) > 0:
            pfix = candidate_prefixes.pop(0)
            if pfix.tail_match == self.strip:
                return pfix.a
            
            print(pfix)

            for aa in range(8):
                val = pfix.a * 8 + aa
                out = self.run_comp(val)
                if self.strip[-len(out):] == out:
                    insert_sorted(candidate_prefixes, PrefixableMatch(val, out))
        

if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t2 = Day(SAMPLE2, True)
    #print(f'Test p2: {t2.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
