import typing as typ

from tools import get_input
import numpy as np


SAMPLE =[
    'aaaaa-bbb-z-y-x-123[abxyz]',
    'a-b-c-d-e-f-g-h-987[abcde]',
    'not-a-real-room-404[oarel]',
    'totally-real-room-200[decoy]'
]
DATA = get_input(4, 2016)


import re
from collections import Counter

MYREGEX = '([a-z|-]+)(\d+)\[([a-z]{5})\]'

class Room:
    def __init__(self, descr: str)-> None:

        self.descr = descr

        g = re.match(MYREGEX, descr).groups()

        l = list(g[0].replace('-', '')) # sort here to solve alphabetical later...
        l.sort()
        self.letters = ''.join(l)
        self.id = int(g[1])
        l = list(g[2])
        l.sort()
        self.checksum = ''.join(l)

    def compute_checksum(self):
        c = Counter(self.letters)
        l = [cc[0] for cc in c.most_common(5)]
        l.sort()
        return ''.join(l)
    
    def is_real(self):
        return self.compute_checksum() == self.checksum
    
    def _charrot(self, c):
        shift = self.id % 26
        if c >= 'a' and c <= 'z':
            return chr((ord(c) - 97 + shift) % 26 + 97)
        else:
            return c

    def real_descr(self):
        return ''.join(map(self._charrot, self.descr))


    def __repr__(self):
        return f'{self.letters}|{self.id}[{self.checksum}]'

class Day4:

    def __init__(self, lines):
        self.lines = lines
        self.rooms = [Room(line) for line in lines]

    def solve(self):
        count = 0
        for r in self.rooms:
            if r.is_real():
                count += r.id

        return count
            


if __name__ == "__main__":
    test = Day4(SAMPLE)
    print(f'Test p1: {test.solve()}')
    real = Day4(DATA)
    print(f'Real p1: {real.solve()}')
    
    rr = [r.real_descr() for r in real.rooms]
    [r for r in rr if 'north' in r]