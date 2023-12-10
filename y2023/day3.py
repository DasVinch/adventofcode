import os
from tools import get_input
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])
REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..',
]

from dataclasses import dataclass


@dataclass
class PartNumber:
    line: int
    start: int
    end: int
    value: int

@dataclass
class Star:
    line: int
    col: int

    def __hash__(self) -> int:
        return (self.line, self.col).__hash__()


RE_PARTNUM = '\d+'
RE_SYMBOL = '[#\$%&\*\+\-/=@]'
SYMBOLS = '#$%&*+-/=@'

def blablacount(s: str) -> int:
    assert len(s) == 3

    if re.match('\d[^0-9]\d', s):
        return 2
    if re.search('\d', s):
        return 1
    return 0


class Day:

    def __init__(self, lines: list[str], debug: bool = False):

        self.partnums: list[PartNumber] = []
        self.lines = lines
        self.n_lines = len(self.lines)
        self.line_len = len(self.lines[0])
        self.debug = debug
        self.stars: list[Star] = []

        # Find the numbers
        for ll, line in enumerate(lines):
            idx = 0
            while (match := re.search(RE_PARTNUM, line[idx:])) is not None:
                if self.debug:
                    print(line[idx:], match)
                start = idx + match.span()[0]
                idx += match.span()[1]
                self.partnums += [
                    PartNumber(ll, start, idx, int(match.group()))
                ]
                if self.debug:
                    print(self.partnums[-1])

        # Find the stars
        for ll, line in enumerate(lines):
            indexes = [x.start() for x in re.finditer('\*', line)]
            for k in indexes:
                self.stars += [Star(ll, k)]

    def solve1(self) -> int:
        total = 0

        for p in self.partnums:

            is_part = False
            # above number
            if p.line > 0 and re.search(RE_SYMBOL, self.lines[p.line - 1][p.start:p.end]):
                is_part = True
            # below number
            if p.line < self.n_lines-1 and re.search(RE_SYMBOL, self.lines[p.line+1][p.start:p.end]):
                is_part = True
            # left
            if p.start > 0:
                if (self.lines[p.line][p.start - 1] in SYMBOLS
                        or (p.line > 0
                            and self.lines[p.line - 1][p.start - 1] in SYMBOLS)
                        or
                    (p.line < self.n_lines - 1
                     and self.lines[p.line + 1][p.start - 1] in SYMBOLS)):
                    is_part = True
            # right
            if p.end < self.line_len:
                if (self.lines[p.line][p.end] in SYMBOLS or
                    (p.line > 0 and self.lines[p.line - 1][p.end] in SYMBOLS) or
                    (p.line < self.n_lines - 1 and self.lines[p.line + 1][p.end] in SYMBOLS)):
                    is_part = True

            if is_part:
                if self.debug:
                    print(f'{p} has char match.')
                total += p.value

        return total


    def solve2(self) -> int:
        total = 0
        
        star_dict: dict[Star, list[PartNumber]] = {}

        for s in self.stars:
            for p in self.partnums:
                if s.col >= p.start - 1 and s.col <= p.end and abs(s.line - p.line) <= 1:
                    if s in star_dict:
                        star_dict[s].append(p)
                    else:
                        star_dict[s] = [p]

            if len(star_dict[s]) == 2:
                if self.debug:
                    print(f'{s} is gear - with {star_dict[s]}')

                value = star_dict[s][0].value * star_dict[s][1].value

                total += value

        return total


if __name__ == "__main__":
    t = Day(SAMPLE, debug=True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
