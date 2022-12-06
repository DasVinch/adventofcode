from tools import get_input
import numpy as np

SAMPLE = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]


class SubPolymer:

    def __init__(self, string) -> None:
        self.start = string[0]
        self.end = string[-1]
        self.length = len(string)

        self.values = {}
        for c in string:
            self.values[c] = self.values.get(c, 0) + 1

    def merge_after(self, p2):
        if self.end != p2.start:
            raise ValueError('Merge continuity error')

        self.end = p2.end
        self.length = self.length + p2.length - 1
        for k in p2.values:
            self.values[k] = self.values.get(k, 0) + p2.values[k]
        self.values[p2.start] -= 1

        return self

    def copy(self):
        p = SubPolymer('xx')
        p.start = self.start
        p.end = self.end
        p.length = self.length
        p.values = self.values.copy()

        return p


class Day14:

    def __init__(self, lines) -> None:
        self.polymer = lines[0]
        self.rules = {}
        for l in lines[2:]:
            pair, add = l.split(' -> ')
            self.rules[pair] = add

        self.recurseMemoizer = {}

    def solve1(self) -> int:
        p = self.recursivator(self.polymer, 10)
        values = [p.values[k] for k in p.values]
        values.sort()
        return values[-1] - values[0]

    def solve2(self) -> int:
        p = self.recursivator(self.polymer, 40)
        values = [p.values[k] for k in p.values]
        values.sort()
        return values[-1] - values[0]

    def recursivator(self, polymer: str, depth: int) -> SubPolymer:
        #print(polymer, depth)
        if (polymer, depth) in self.recurseMemoizer:
            return self.recurseMemoizer[(polymer, depth)].copy()
        
        if depth == 0:
            p = SubPolymer(polymer)
        elif len(polymer) > 2:
            p = self.recursivator(polymer[:2], depth).merge_after(
                self.recursivator(polymer[1:], depth))
        elif len(polymer) == 2:
            if polymer in self.rules:
                r = self.rules[polymer]
                p = self.recursivator(polymer[0] + r,
                                         depth - 1).merge_after(
                                             self.recursivator(
                                                 r + polymer[1], depth - 1))
        self.recurseMemoizer[(polymer, depth)] = p.copy()
        return p


if __name__ == "__main__":
    test = Day14(SAMPLE)
    print(test.solve2())
    real = Day14(get_input(14, 2021))
    print(real.solve2())