from __future__ import annotations

import typing as typ
import tools as tl
from . import komputer

import numpy as np

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = list[int] # TODO

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(s) for s in input[0].split(',')]
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        matrix = np.zeros((50,50), np.int64)

        for xx in range(50):
            for yy in range(50):
                komp = komputer.Komputer(self.data)

                komp.execute_til_input()
                komp.pending_input = xx
                komp.execute_one_instruction()
                komp.execute_til_input()
                komp.pending_input = yy
                komp.execute_til_output()
                matrix[xx,yy] = komp.outputs[-1]

        tl.print_bool_matrix(matrix > 0)

        print(matrix)
        return np.sum(matrix)


    def solve2(self) -> int:
        cx, cy = 49, 47

        move_x = True

        def is_in_beam(xx: int, yy: int) -> bool:
            komp = komputer.Komputer(self.data)

            komp.execute_til_input()
            komp.pending_input = xx
            komp.execute_one_instruction()
            komp.execute_til_input()
            komp.pending_input = yy
            komp.execute_til_output()
            return komp.outputs[-1] == 1

        while True:
            #print(cx, cy)

            if is_in_beam(cx + 99, cy) and is_in_beam(cx, cy + 99):
                print('Any 100-sq found@ ', cx, cy)
                break

            in_beam_x, in_beam_y = None, None
            if move_x:
                in_beam_x = is_in_beam(cx + 1, cy)
                if in_beam_x:
                    cx += 1
                    continue
            
            if not move_x:
                in_beam_y = is_in_beam(cx, cy + 1)
                if in_beam_y:
                    cy += 1
                    continue

            if move_x:
                in_beam_y = is_in_beam(cx, cy + 1)
                if in_beam_y:
                    move_x = False
                    continue

            if not move_x:
                in_beam_x = is_in_beam(cx + 1, cy)
                if in_beam_x:
                    move_x = True
                    continue
            
            #assert is_in_beam(cx + 1, cy + 1)
            cx += 1
            cy += 1

        while True:
            print(cx, cy)
            if is_in_beam(cx - 1, cy) and is_in_beam(cx - 1, cy + 99):
                cx -= 1
                continue
            if is_in_beam(cx, cy - 1) and is_in_beam(cx + 99, cy - 1):
                cy -= 1
                continue
            if is_in_beam(cx - 1, cy - 1) and is_in_beam(cx + 98, cy - 1) and is_in_beam(cx + 98, cy - 1):
                cx -= 1
                cy -= 1
                continue
            break

        breakpoint()

        return cx * 10000 + cy