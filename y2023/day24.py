from __future__ import annotations
import typing as typ

import os
import numpy as np

from tools import get_input, make_char_matrix
import tools

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3',
]

from dataclasses import dataclass


@dataclass
class HailStone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @staticmethod
    def parse(s: str) -> HailStone:
        p, v = s.split(' @ ')
        ps = p.split(', ')
        vs = v.split(', ')
        return HailStone(int(ps[0]), int(ps[1]), int(ps[2]), int(vs[0]),
                         int(vs[1]), int(vs[2]))

    def __add__(self, other: HailStone) -> HailStone:
        return HailStone(self.x + other.x,
                         self.y + other.y,
                         self.z + other.z,
                         self.vx + other.vx,
                         self.vy + other.vy,
                         self.vz + other.vz)

    def __sub__(self, other: HailStone) -> HailStone:
        return HailStone(self.x - other.x,
                         self.y - other.y,
                         self.z - other.z,
                         self.vx - other.vx,
                         self.vy - other.vy,
                         self.vz - other.vz)

    @property
    def p(self) -> V3:
        return V3(self.x, self.y, self.z)

    @property
    def v(self) -> V3:
        return V3(self.vx, self.vy, self.vz)

@dataclass
class V3:
    x: float
    y: float
    z: float

    def __add__(s, o: V3) -> V3: # Addition
        return V3(s.x + o.x, s.y + o.y, s.z + o.z)

    def __sub__(s, o: V3) -> V3: # Addition
        return V3(s.x - o.x, s.y - o.y, s.z - o.z)

    def __mul__(s, o: V3) -> float: # Dot
        return s.x * o.x + s.y * o.y + s.z * o.z

    def __rmul__(s, o: float) -> V3:
        return V3(s.x * o, s.y * o, s.z * o)

    def __truediv__(s, o: float) -> V3:
        return V3(s.x / o, s.y / o, s.z / o)

    def __pow__(s, o: V3) -> V3: # vectorprod
        return V3(s.y * o.z - o.y * s.z,
                  s.z * o.x - o.z * s.x,
                  s.x * o.y - o.x * s.y)

def intersect_xy(ha: HailStone,
                 hb: HailStone) -> tuple[float, float, float, float] | None:
    discr = ha.vx * hb.vy - hb.vx * ha.vy
    if discr == 0:
        return None

    ta = (hb.vy * (hb.x - ha.x) - hb.vx * (hb.y - ha.y)) / discr
    tb = -(ha.vy * (ha.x - hb.x) - ha.vx * (ha.y - hb.y)) / discr
    x = ha.x + ta * ha.vx
    y = ha.y + ta * ha.vy

    return ta, tb, x, y


class Day:

    def __init__(self, lines):
        self.hailstones = [HailStone.parse(l) for l in lines]

        self.differential_stones = [h - self.hailstones[0] for h in self.hailstones]

    def solve1(self, minval=200000000000000, maxval=400000000000000) -> int:
        count = 0
        for k, ha in enumerate(self.hailstones):
            for hb in self.hailstones[k + 1:]:
                something = intersect_xy(ha, hb)
                if something is not None:
                    ta, tb, x, y = something
                    if (ta >= 0 and tb >= 0 and x >= minval and y >= minval
                            and x <= maxval and y <= maxval):
                        count += 1
                        #print(ha, hb, ta, tb, x, y)

        return count

    def solve2(self) -> int:
        h1, h2 = self.differential_stones[1:3]
        t1: float = - ((h1.p ** h2.p) * h2.v) / ((h1.v ** h2.p) * h2.v)
        t2: float = - ((h1.p ** h2.p) * h1.v) / ((h1.p ** h2.v) * h1.v)

        h1_t1 = h1.p + t1 * h1.v
        h2_t2 = h2.p + t2 * h2.v

        # Speed vector
        habs0, habs1 = self.hailstones[:2]
        v_rock_diff = (h2_t2 - h1_t1) / (t2 - t1)
        v_rock_abs = v_rock_diff + habs0.v

        p_rock_abs = habs1.p + t1 * habs1.v - t1 * v_rock_abs
        
        return p_rock_abs.x + p_rock_abs.y + p_rock_abs.z


if __name__ == "__main__":
    t = Day(SAMPLE)

    print(f'Test p1: {t.solve1(7, 27)}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
