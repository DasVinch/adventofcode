import os
from tools import get_input
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])
REAL = get_input(DAYDAY, 2023)

SAMPLE = [
'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]

from dataclasses import dataclass

@dataclass
class Card:
    win: set[int]
    numbers: set[int]

    def score(self) -> int:
        intersect = self.numbers.intersection(self.win)
        if len(intersect) == 0:
            return 0
        else:
            return 2**(len(intersect) - 1)
        
    def score2(self) -> int:
        return len(self.numbers.intersection(self.win))

def parse_card(line: str) -> Card:
    a,b = line.split(':')
    c,d = b.split('|')
    win = [int(x) for x in c.strip().split()]
    numbers = [int(x) for x in d.strip().split()]
    return Card(set(win), set(numbers))


class Day:

    def __init__(self, lines: list[str], debug: bool = False):

        self.lines = lines
        self.cards = [parse_card(l) for l in self.lines]
        self.debug = debug

        if self.debug:
            print(self.cards)

    def solve1(self) -> int:
        return sum([c.score() for c in self.cards])


    def solve2(self) -> int:
        card_counts = [1] * len(self.cards)

        for k, c in enumerate(self.cards):
            w = c.score2()
            for kk in range(k+1, min(len(self.cards), k+w+1)):
                card_counts[kk] += card_counts[k]

        return sum(card_counts)


if __name__ == "__main__":
    t = Day(SAMPLE, debug=True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
