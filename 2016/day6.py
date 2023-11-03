import typing as typ

from tools import get_input
import numpy as np

from collections import Counter

from tqdm import tqdm

SAMPLE = [
    'eedadn',
    'drvtee',
    'eandsr',
    'raavrd',
    'atevrs',
    'tsrnev',
    'sdttsa',
    'rasrtv',
    'nssdts',
    'ntnada',
    'svetve',
    'tesnvt',
    'vntsnd',
    'vrdear',
    'dvrsen',
    'enarar',
]

REAL = get_input(6, 2016)

class Day6:
    def __init__(self, lines):
        self.len = len(lines[0])
        self.lines = lines

    def solve1(self):
        res = []

        for k in range(self.len):
            res += [
                Counter((s[k] for s in self.lines)).most_common()[0][0]
            ]

        return ''.join(res)

    def solve2(self):
        res = []

        for k in range(self.len):
            res += [
                Counter((s[k] for s in self.lines)).most_common()[-1][0]
            ]

        return ''.join(res)
        
if __name__ == '__main__':
    t = Day6(SAMPLE)
    print(f'Sample: {t.solve1()}')
    r = Day6(REAL)
    print(f'Real: {r.solve1()}')


    t = Day6(SAMPLE)
    print(f'Sample: {t.solve2()}')
    r = Day6(REAL)
    print(f'Real: {r.solve2()}')