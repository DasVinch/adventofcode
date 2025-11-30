from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = [
    '<x=-1, y=0, z=2>',
    '<x=2, y=-10, z=-7>',
    '<x=4, y=-8, z=8>',
    '<x=3, y=5, z=-1>',
]

ADDITIONAL_SAMPLES: list[list[str]] = []


import re

RE_POS_PARSE = r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'

from dataclasses import dataclass, replace


@dataclass(frozen=False)
class Moon:
    x: int
    y: int
    z: int

    vx: int = 0
    vy: int = 0
    vz: int = 0


    @staticmethod
    def parse_from(s: str) -> Moon:
        match = re.match(RE_POS_PARSE, s)
        assert match is not None
        xs, ys, zs = match.groups()

        return Moon(int(xs), int(ys), int(zs))

    def compute_vel(self, moons: list[Moon]) -> None:
        #self.vx, self.vy, self.vz = 0,0,0
        for m in moons:
            if m.x > self.x:
                self.vx += 1
            if m.x < self.x:
                self.vx -= 1
            if m.y > self.y:
                self.vy += 1
            if m.y < self.y:
                self.vy -= 1
            if m.z > self.z:
                self.vz += 1
            if m.z < self.z:
                self.vz -= 1

    def apply_vel(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self) -> int:
        return (abs(self.x) + abs(self.y) + abs(self.z)) *\
            (abs(self.vx) + abs(self.vy) + abs(self.vz))


T_DATA: typ.TypeAlias = list[Moon]  # TODO


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [Moon.parse_from(l) for l in input]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.data2 = [replace(m) for m in data]
        self.debug = debug
        ...

    def solve1(self) -> int:
        print(self.data[0])
        for _ in range(1000):
            for m in self.data:
                m.compute_vel(self.data)
            for m in self.data:
                m.apply_vel()

        return sum([m.energy() for m in self.data])


    def solve2(self) -> int:
        orig_state = [replace(m) for m in self.data2]

        px, py, pz = 0, 0, 0
        k = 1
        while True:
            for m in self.data2:
                m.compute_vel(self.data2)
            for m in self.data2:
                m.apply_vel()
            
            if all([m.x == mo.x for m, mo in zip(self.data2, orig_state)]) and \
                    all([m.vx == mo.vx for m, mo in zip(self.data2, orig_state)]) and \
                    px == 0:
                px = k
                print(f'{px=}')
            if all([m.y == mo.y for m, mo in zip(self.data2, orig_state)]) and \
                    all([m.vy == mo.vy for m, mo in zip(self.data2, orig_state)]) and \
                    py == 0:
                py = k
                print(f'{py=}')
            if all([m.z == mo.z for m, mo in zip(self.data2, orig_state)]) and \
                    all([m.vz == mo.vz for m, mo in zip(self.data2, orig_state)]) and \
                    pz == 0:
                pz = k
                print(f'{pz=}')

            if px*py*pz > 0:
                break

            k += 1

        import math
        return math.lcm(px,py,pz)

            

        
