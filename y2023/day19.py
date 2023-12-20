from __future__ import annotations
import typing as typ

from tools import get_input
import tools

from skimage.morphology import label

import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}',
]

import re

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    m: int
    a: int
    s: int

    def __hash__(self) -> int:
        return hash((self.x, self.m, self.a, self.s))
    
    def __eq__(self, oth: Point) -> bool:
        return self.x == oth.x and self.m == oth.m and self.a == oth.a and self.s == oth.s


@dataclass
class Clause:
    var: str
    op: str
    val: int

    def apply(self, point: Point) -> bool:
        match self.op:
            case '>':
                return getattr(point, self.var) > self.val
            case '<':
                return getattr(point, self.var) < self.val
            case _:
                raise AssertionError('blah.')


@dataclass
class Workflow:
    ops: list[tuple[Clause, str]]
    final: str

    def apply(self, point: Point) -> str:
        for cl, dest in self.ops:
            if cl.apply(point):
                return dest
        return self.final


def parser(lines: list[str]) -> tuple[dict[str, Workflow], set[Point]]:

    workflows = {}
    points = set()

    for kk, line in enumerate(lines):
        if line == '':
            break
        name, data = parse_workflow(line)
        workflows[name] = data

    for line in lines[kk+1:]:
        points.add(parse_point(line))

    return workflows, points


def parse_point(p: str) -> Point:
    point_re = '{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}'
    g = re.match(point_re, p).groups()
    x, m, a, s = (int(pp) for pp in g)
    return Point(x, m, a, s)


def parse_workflow(l: str) -> tuple[str, Workflow]:
    name, core = l[:-1].split('{')
    clauses_str = core.split(',')
    re_clause = '([xmas])(<|>)(\d+):([a-zA-Z]*)'

    clauses: list[tuple[Clause,str]] = []
    for cl in clauses_str[:-1]:
        letter, op, num_str, target = re.match(re_clause, cl).groups()
        clauses.append((Clause(letter, op, int(num_str)), target))

    return (name, Workflow(clauses, clauses_str[-1]))
    


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines
        self.workflows, self.points = parser(self.lines)

        self.debug = debug

    def solve1(self) -> int:
        mapped_points: dict[Point, str] = {p: 'in' for p in self.points}

        for p in mapped_points:
            while mapped_points[p] not in ('A', 'R'):
                mapped_points[p] = self.workflows[mapped_points[p]].apply(p)

        return sum((p.x + p.m + p.a + p.s for p in mapped_points if mapped_points[p] == 'A'))

    def solve2(self) -> int:

        return 0


if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
