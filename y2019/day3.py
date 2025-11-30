from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = ['R8,U5,L5,D3', 'U7,R6,D4,L4']

ADDITIONAL_SAMPLES: list[list[str]] = [
    [
        'R75,D30,R83,U83,L12,D49,R71,U7,L72',
        'U62,R66,U55,R34,D71,R55,D58,R83',
    ],
    [
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
    ]
]

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


T_DATA: typ.TypeAlias = tuple[list[Point], list[Point]]  # TODO


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        p1, p2 = [Point(0, 0)], [Point(0, 0)]

        for kk, pp in enumerate((p1, p2)):
            for lex in input[kk].split(','):
                if lex[0] == 'U':
                    pp.append(Point(pp[-1].x, pp[-1].y + int(lex[1:])))
                if lex[0] == 'D':
                    pp.append(Point(pp[-1].x, pp[-1].y - int(lex[1:])))
                if lex[0] == 'L':
                    pp.append(Point(pp[-1].x - int(lex[1:]), pp[-1].y))
                if lex[0] == 'R':
                    pp.append(Point(pp[-1].x + int(lex[1:]), pp[-1].y))

        return p1, p2

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.debug = debug
        self.data = data

        if self.debug:
            print(self.data)

    def solve1(self) -> int:

        intersects: list[Point] = []

        for ii in range(len(self.data[0])-1):
            for jj in range(len(self.data[1])-1):
                p1, q1 = self.data[0][ii], self.data[0][ii + 1]
                p2, q2 = self.data[1][jj], self.data[1][jj + 1]
                if (p1.x == q1.x and p2.y == q2.y and p2.y <= max(p1.y, q1.y)
                        and p2.y >= min(p1.y, q1.y)
                        and p1.x >= min(p2.x, q2.x)
                        and p1.x <= max(p2.x, q2.x)):
                    intersects += [Point(p1.x, p2.y)]
                elif (p2.x == q2.x and p1.y == q1.y and p1.y <= max(p2.y, q2.y)
                        and p1.y >= min(p2.y, q2.y)
                        and p2.x >= min(p1.x, q1.x)
                        and p2.x <= max(p1.x, q1.x)):
                    intersects += [Point(p2.x, p1.y)]

        return min([k for k in list(map(lambda p: abs(p.x) + abs(p.y), intersects)) if k > 0])


    def solve2(self) -> int:
        intersects: list[int] = []

        len1 = 0
        for ii in range(len(self.data[0])-1):
            len2 = 0
            for jj in range(len(self.data[1])-1):
                p1, q1 = self.data[0][ii], self.data[0][ii + 1]
                p2, q2 = self.data[1][jj], self.data[1][jj + 1]
                if (p1.x == q1.x and p2.y == q2.y and p2.y <= max(p1.y, q1.y)
                        and p2.y >= min(p1.y, q1.y)
                        and p1.x >= min(p2.x, q2.x)
                        and p1.x <= max(p2.x, q2.x)):
                    if self.debug:
                        print(Point(p1.x, p2.y), len1 + abs(p1.y - p2.y) + len2 + abs(p1.x - p2.x))
                    intersects += [len1 + abs(p1.y - p2.y) + len2 + abs(p1.x - p2.x)]
                elif (p2.x == q2.x and p1.y == q1.y and p1.y <= max(p2.y, q2.y)
                        and p1.y >= min(p2.y, q2.y)
                        and p2.x >= min(p1.x, q1.x)
                        and p2.x <= max(p1.x, q1.x)):
                    if self.debug:
                        print(Point(p2.x, p1.y), len1 + abs(p1.y - p2.y) + len2 + abs(p1.x - p2.x))
                    intersects += [len1 + abs(p1.y - p2.y) + len2 + abs(p1.x - p2.x)]

                len2 += abs(p2.x - q2.x) + abs(p2.y - q2.y)
            len1 += abs(p1.x - q1.x) + abs(p1.y - q1.y)

        return min([k for k in intersects if k > 0])
