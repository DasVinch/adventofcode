from __future__ import annotations

import typing as typ

T = typ.TypeVar('T', covariant=True)
class Day(typ.Protocol, typ.Generic[T]):
    def __init__(self, parse_input: T, debug: bool = False) -> None:
        ...

    @staticmethod
    def parse_input(input: list[str]) -> T:
        ...

    def solve1(self) -> int:
        ...

    def solve2(self) -> int:
        ...

'''
from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = []

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = None # TODO

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        ...
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        ...

    def solve2(self) -> int:
        ...
'''