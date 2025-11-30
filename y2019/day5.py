from __future__ import annotations

import typing as typ
import tools as tl

import importlib
from . import komputer

importlib.reload(komputer)

from .komputer import Komputer

SAMPLE: list[str] = ['3,0,4,0,99']

ADDITIONAL_SAMPLES: list[list[str]] = [
    ['3,9,8,9,10,9,4,9,99,-1,8'],
    [
        '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    ],
]

T_DATA: typ.TypeAlias = list[int]  # TODO


class SubKomputer(Komputer):

    def __init__(self, ribbon: list[int], what_input: int = 1):
        super().__init__(ribbon)

        self.outputs: list[int] = []
        self.input_value = what_input

    def get_input(self) -> int:
        return self.input_value

    def output(self, val: int) -> None:
        self.outputs.append(val)


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(x) for x in input[0].split(',')]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        print(self.data[:15])

    def solve1(self) -> int:
        komp = SubKomputer(self.data)

        komp.execute_all()

        print(komp.outputs)

        return komp.outputs[-1] if len(komp.outputs) > 0 else komp.ribbon[0]

    def solve2(self) -> int:
        komp = SubKomputer(self.data, 5)

        komp.execute_all()

        print(komp.outputs)

        return komp.outputs[-1] if len(komp.outputs) > 0 else komp.ribbon[0]
