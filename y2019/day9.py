from __future__ import annotations

import typing as typ
import tools as tl

from .komputer import Komputer

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = [
    ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'],
    ['1102,34915192,34915192,7,4,7,99,0'],
    ['104,1125899906842624,99']
]

T_DATA: typ.TypeAlias = list[int] # TODO

class SubKomputer1(Komputer):
    def __init__(self, ribbon: list[int]):
        super().__init__(ribbon)
        self.outputs: list[int] = []

    def output(self, val: int) -> None:
        self.outputs.append(val)

    def get_input(self) -> int:
        return 1 # test mode?

class SubKomputer2(SubKomputer1):
    def get_input(self) -> int:
        return 2 # sensor boost mode!

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(k) for k in input[0].split(',')]
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        comp = SubKomputer1(self.data)

        comp.execute_all()

        return comp.outputs

    def solve2(self) -> int:
        comp = SubKomputer2(self.data)

        comp.execute_all()

        return comp.outputs