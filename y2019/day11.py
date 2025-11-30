from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = list[int]  # TODO

from .komputer import Komputer


class AdHocKomputer(Komputer):

    pending_input: int | None

    def get_input(self) -> int:
        if self.pending_input is None:
            exc = AssertionError('pending_input is None')
            breakpoint()
            raise exc
        return self.pending_input


U, R, D, L = 0, 1, 2, 3


class Robot:

    def __init__(self, ribbon: list[int], start: int = 0):
        self.brain = AdHocKomputer(ribbon)

        self.pos: tuple[int, int] = (0, 0)
        self.paints: dict[tuple[int, int], int] = {}
        self.start = start

        self.dir = U

    def paint_cycle(self):
        self.brain.execute_til_input()
        
        self.brain.pending_input = self.paints.get((self.pos), self.start)
        self.brain.execute_one_instruction()
        self.brain.pending_input = None

        self.paints[self.pos] = self.brain.execute_til_output()

        rot = self.brain.execute_til_output()
        if rot == 0:
            self.dir = (self.dir - 1) % 4
        elif rot == 1:
            self.dir = (self.dir + 1) % 4
        else:
            raise AssertionError

        if self.dir == U:
            self.pos = self.pos[0], self.pos[1] + 1
        elif self.dir == R:
            self.pos = self.pos[0] + 1, self.pos[1]
        elif self.dir == L:
            self.pos = self.pos[0] - 1, self.pos[1]
        elif self.dir == D:
            self.pos = self.pos[0], self.pos[1] - 1
        else:
            raise AssertionError


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(k) for k in input[0].split(',')]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

    def solve1(self) -> int:
        self.robot = Robot(self.data)
        while True:
            try:
                self.robot.paint_cycle()
            except:
                break
        return len(self.robot.paints)

    def solve2(self) -> int:
        self.robot = Robot(self.data, 1)
        while True:
            try:
                self.robot.paint_cycle()
            except:
                break
        
        import numpy as np
        t = np.zeros((100,100))
        for (x,y), p in self.robot.paints.items():
            t[x,y] = p

        tl.print_bool_matrix(np.fft.fftshift(t))
