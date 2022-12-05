from typing import List, Tuple, Set
from tools import get_input

SAMPLE = [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw',
]

def prio(x: str) -> int:
    v = ord(x)
    if v < 64 + 32: # upper
        return v - 64 + 26
    else:
        return v - 96


def setify(lines: List[str]) -> List[Tuple[Set[int], Set[int]]]:
    out = []
    for line in lines:
        k = len(line)
        s1 = set()
        s2 = set()
        for let in line[:k//2]:
            s1.add(prio(let))
        for let in line[k // 2:]:
            s2.add(prio(let))

        out += [(s1, s2)]
    
    return out



def solve_1(dat: List[Tuple[Set[int], Set[int]]]) -> int:
    tot = 0
    for s1, s2 in dat:
        tot += s1.intersection(s2).pop()

    return tot


def solve_2(dat: List[Tuple[Set[int], Set[int]]]) -> int:
    tot = 0
    for kk in range(len(dat) // 3):
        sa = dat[3*kk][0].union(dat[3*kk][1])
        sb = dat[3*kk+1][0].union(dat[3*kk+1][1])
        sc = dat[3*kk+2][0].union(dat[3*kk+2][1])
        tot += sa.intersection(sb).intersection(sc).pop()

    return tot



if __name__ == "__main__":
    #dat = setify(SAMPLE)
    dat = setify(get_input(3))

    #print(solve_1(dat))
    print(solve_2(dat))