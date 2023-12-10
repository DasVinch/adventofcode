from __future__ import annotations

import os
from tools import get_input
import typing as typ
import re
import math

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483',
]

import enum
from collections import Counter
from dataclasses import dataclass

class Val(enum.IntEnum):
    FiOAK = 7
    FoOAK = 6
    FuHou = 5
    ThOAK = 4
    TwoPa = 3
    OnePa = 2
    HCard = 1

    @classmethod
    def findVal(cls, hand) -> Val:
        ctr = Counter(hand)
        lvals = list(ctr.values())
        lvals.sort(reverse=True)

        if lvals[0] == 5:
            return Val.FiOAK
        if lvals[0] == 4:
            return Val.FoOAK
        if lvals[0] == 3:
            if lvals[1] == 2:
                return Val.FuHou
            else:
                return Val.ThOAK
        if lvals[0] == 2:
            if lvals[1] == 2:
                return Val.TwoPa
            else:
                return Val.OnePa
        return Val.HCard
    
    @classmethod
    def findVal_optiJ(cls, hand) -> Val:
        return max([Val.findVal(hand.replace('J', v)) for v in CARDVALS_NOJ])
    
CARDVALS_NOJ = 'AKQT98765432'

def cardify(hand: str) -> list[int]:
    vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
            '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
            '3': 3, '2': 2}
    return [vals[h] for h in hand]

def cardify2(hand: str) -> list[int]:
    vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10,
            '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
            '3': 3, '2': 2}
    return [vals[h] for h in hand]


@dataclass
class Hand:
    hand: str
    bid: int

class Day:
    def __init__(self, lines) -> None:
        split_lines = [line.split() for line in lines]
        self.hands = [Hand(l[0], int(l[1])) for l in split_lines]

    def solve1(self):
        self.hands.sort(key=lambda h: (Val.findVal(h.hand).value, cardify(h.hand)))

        return sum([(k+1) * h.bid for k,h in enumerate(self.hands)])

    def solve2(self):
        self.hands.sort(key=lambda h: (Val.findVal_optiJ(h.hand).value, cardify2(h.hand)))

        return sum([(k+1) * h.bid for k,h in enumerate(self.hands)])

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')