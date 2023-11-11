import typing as typ

from tools import get_input, print_bool_matrix
import numpy as np

from tqdm import tqdm

import re

SAMPLES = [
    'ADVENT',
    'A(1x5)BC',
    '(3x3)XYZ',
    'A(2x2)BCD(2x2)EFG',
    '(6x1)(1x3)A',
    'X(8x2)(3x3)ABCY',
]

SAMPLES2 = [
    '(3x3)XYZ',
    'X(8x2)(3x3)ABCY',
    '(27x12)(20x12)(13x14)(7x10)(1x12)A',
    '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN',
]

REAL = get_input(9, 2016)


RE = '^(?P<HEAD>[A-Z]*)\((?P<A>\d+)x(?P<B>\d+)\)'

def recursiverlength(s: str) -> int:
    if len(s) == 0:
        return 0
    m = re.match(RE, s)
    if m is None:
        return len(s)
    g = m.groupdict()
    
    k = len(g['HEAD'])
    a, b = int(g['A']), int(g['B'])
    substr = s[k+3+len(g['A'])+len(g['B']) + a:]
    return len(g['HEAD']) + a*b + recursiverlength(substr)

def morerecursiverlength(s: str) -> int:
    if len(s) == 0:
        return 0
    m = re.match(RE, s)
    if m is None:
        return len(s)
    g = m.groupdict()

    k = len(g['HEAD'])

    a, b = int(g['A']), int(g['B'])

    expandstr = s[k+3+len(g['A'])+len(g['B']):k+3+len(g['A'])+len(g['B']) + a]
    substr = s[k+3+len(g['A'])+len(g['B']) + a:]

    return len(g['HEAD']) + b*morerecursiverlength(expandstr) + morerecursiverlength(substr)

if __name__ == '__main__':
    for s in SAMPLES:
        print(s, recursiverlength(s))

    print('Real:')
    print(recursiverlength(REAL[0]))


    for s in SAMPLES2:
        print(s, morerecursiverlength(s))

    print('Real, part 2:')
    print(morerecursiverlength(REAL[0]))
