from __future__ import annotations

import os
import tools
from tools import get_input

import typing as typ
import numpy as np

import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2024)

SAMPLE = [
    '47|53',
    '97|13',
    '97|61',
    '97|47',
    '75|29',
    '61|13',
    '75|53',
    '29|13',
    '97|29',
    '53|29',
    '61|53',
    '97|53',
    '61|29',
    '47|13',
    '75|47',
    '97|75',
    '47|61',
    '75|61',
    '47|29',
    '75|13',
    '53|13',
    '',
    '75,47,61,53,29',
    '97,61,53,29,13',
    '75,29,13',
    '75,97,47,61,53',
    '61,13,29',
    '97,13,75,29,47',
]


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.rules = []
        self.prints = []

        for line in lines:
            if line == '':
                continue
            if '|' in line:
                a,b = line.split('|')
                self.rules += [(int(a), int(b))]
            else:
                self.prints += [[int(t) for t in line.split(',')]]

        self.rules_by_second_member: dict[int, set[int]] = {}

        for rule in self.rules:
            a, b = rule
            if not b in self.rules_by_second_member:
                self.rules_by_second_member[b] = set()
            self.rules_by_second_member[b].add(a)


    def solve1(self) -> int:
        middles = 0
        for print in self.prints:
            print_blacklist = set()
            valid = True
            for page in print:
                if page in print_blacklist:
                    valid = False
                    break
                if page in self.rules_by_second_member:
                    print_blacklist.update(self.rules_by_second_member[page])
            if valid:
                middles += print[len(print) // 2]

        return middles

    def solve2(self) -> int:
        invalid_prints = []
        for print in self.prints:
            print_blacklist = set()
            valid = True
            for page in print:
                if page in print_blacklist:
                    valid = False
                    invalid_prints += [print.copy()]
                    break
                if page in self.rules_by_second_member:
                    print_blacklist.update(self.rules_by_second_member[page])

        middles = 0
        while len(invalid_prints) > 0:
            print = invalid_prints.pop(0)

            print_blacklist = set()
            valid = True
            for k, page in enumerate(print):
                if page in print_blacklist:
                    valid = False
                    print[k], print[k-1] = print[k-1], print[k]
                    invalid_prints.append(print)
                    break
                if page in self.rules_by_second_member:
                    print_blacklist.update(self.rules_by_second_member[page])
            if valid:
                middles += print[len(print) // 2]


        return middles

        return count


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL, False)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
