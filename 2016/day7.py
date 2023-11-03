import typing as typ

from tools import get_input
import numpy as np

from collections import Counter

from tqdm import tqdm

SAMPLE = [
    'abba[mnop]qrst',
    'abcd[bddb]xyyx',
    'aaaa[qwer]tyui',
    'ioxxoj[asdfgh]zxcvbn',
]

SAMPLE2 = [
    'aba[bab]xyz',
    'xyx[xyx]xyx',
    'aaa[kek]eke',
    'zazbz[bzb]cdb',
]

REAL = get_input(7, 2016)

def str_is_abba(s: str) -> bool:
    if len(s) < 4:
        return False
    n = len(s)
    for k in range(n-3):
        if s[k] != s[k+1] and s[k] == s[k+3] and s[k+1] == s[k+2]:
            return True
        
    return False

def aba_set(s: str) -> typ.Set[str]:
    out: typ.Set[str] = set()
    for k in range(len(s)-2):
        if s[k] != s[k+1] and s[k] == s[k+2]:
            out.add(s[k:k+3])
    return out

def bab_set(s: str) -> typ.Set[str]:
    aba = aba_set(s)

    return set(map(lambda ss: ss[1:] + ss[1], aba))
    

class Day7:
    def __init__(self, lines: typ.List[str]) -> None:
        self.lines = lines

        self.parsed_lines = [
            [a for b in [s.split(']') for s in l.split('[')] for a in b]
        for l in lines]

    def tlc_can(self, linearr: typ.List[str]) -> bool:
        return any(map(str_is_abba, linearr[::2])) and not any(map(str_is_abba, linearr[1::2]))
    
    def solve1(self) -> int:
        return sum([self.tlc_can(line) for line in self.parsed_lines])
    
    def ssl_can(self, linearr: typ.List[str]) -> bool:
        aba: typ.Set[str] = set()
        bab: typ.Set[str] = set()
        for s in linearr[::2]:
            aba.update(aba_set(s))
        for s in linearr[1::2]:
            bab.update(bab_set(s))

        return len(aba.intersection(bab)) > 0
    
    def solve2(self) -> int:
        return sum([self.ssl_can(line) for line in self.parsed_lines])


if __name__ == '__main__':
    t = Day7(SAMPLE)
    print(f'Sample: {t.solve1()}')
    r = Day7(REAL)
    print(f'Real: {r.solve1()}')


    t2 = Day7(SAMPLE2)
    print(f'Sample: {t2.solve2()}')
    r = Day7(REAL)
    print(f'Real: {r.solve2()}')