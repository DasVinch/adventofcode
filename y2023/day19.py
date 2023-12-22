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


@dataclass(frozen=True)
class Point:
    x: int
    m: int
    a: int
    s: int


@dataclass(frozen=True)
class PointRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def volume(self):
        return (self.x[1] - self.x[0] + 1) * \
        (self.m[1] - self.m[0] + 1) * \
        (self.a[1] - self.a[0] + 1) * \
        (self.s[1] - self.s[0] + 1)



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

    def applyRange(
            self,
            pr: PointRange) -> tuple[PointRange | None, PointRange | None]:
        vmin, vmax = getattr(pr, self.var)
        if vmin < self.val and vmax < self.val and self.op == '<':
            return (pr, None)
        if vmin <= self.val and vmax <= self.val and self.op == '>':
            return (None, pr)
        if vmin > self.val and vmax > self.val and self.op == '>':
            return (pr, None)
        if vmin >= self.val and vmax >= self.val and self.op == '<':
            return (None, pr)

        args_identical = {'x': pr.x, 'm': pr.m, 'a': pr.a, 's': pr.s}
        if self.op == '<':
            args_identical[self.var] = (vmin, self.val - 1)
            prlow = PointRange(**args_identical)
            args_identical[self.var] = (self.val, vmax)
            prhigh = PointRange(**args_identical)
            return (prlow, prhigh)

        elif self.op == '>':
            args_identical[self.var] = (vmin, self.val)
            prlow = PointRange(**args_identical)
            args_identical[self.var] = (self.val + 1, vmax)
            prhigh = PointRange(**args_identical)
            return (prhigh, prlow)

        raise AssertionError('Dafukato.')


@dataclass
class Workflow:
    ops: list[tuple[Clause, str]]
    final: str

    def apply(self, point: Point) -> str:
        for cl, dest in self.ops:
            if cl.apply(point):
                return dest
        return self.final

    def applyRanges(self, spr: PointRange) -> dict[str, set[PointRange]]:
        result: dict[str, set[PointRange]] = {tp[1]: set() for tp in self.ops}
        result[self.final] = set()

        to_do = {spr}
        for cl, dest in self.ops:
            to_remain = set()
            for pr in to_do:
                spass, sfail = cl.applyRange(pr)
                if spass is not None:
                    result[dest].add(spass)
                if sfail is not None:
                    to_remain.add(sfail)
            
            to_do = to_remain

        for pr in to_do:
            result[self.final].add(pr)

        return result


def parser(lines: list[str]) -> tuple[dict[str, Workflow], set[Point]]:

    workflows = {}
    points = set()

    for kk, line in enumerate(lines):
        if line == '':
            break
        name, data = parse_workflow(line)
        workflows[name] = data

    for line in lines[kk + 1:]:
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

    clauses: list[tuple[Clause, str]] = []
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

        return sum((p.x + p.m + p.a + p.s for p in mapped_points
                    if mapped_points[p] == 'A'))

    def solve2(self) -> int:
        
        pending_prs: set[tuple[PointRange, str]] = {(PointRange((1,4000), (1,4000), (1,4000), (1,4000)), 'in')}
        accepted: set[PointRange] = set()
        rejected: set[PointRange] = set()

        while len(pending_prs) > 0:
            pr, flow = pending_prs.pop()
            workflowed_prs = self.workflows[flow].applyRanges(pr)
            for flow, flowed_prs in workflowed_prs.items():
                if flow == 'A':
                    accepted.update(flowed_prs)
                elif flow == 'R':
                    rejected.update(flowed_prs)
                else:
                    for ppr in flowed_prs:
                        pending_prs.add((ppr, flow))

        tot = sum([pr.volume() for pr in accepted])

        return tot


if __name__ == "__main__":

    t = Day(SAMPLE, True)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
