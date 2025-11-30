from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = ['100756']

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> list[int]:
        return [int(s) for s in input]
    
    def __init__(self, data: list[int], debug: bool = False) -> None:
        self.weights = data

    def solve1(self) -> int:
        return sum([w // 3 - 2 for w in self.weights])

    def solve2(self) -> int:
        def rec_fuel(f: int) -> int:
            if f <= 0:
                return 0
            else:
                return f + rec_fuel(f // 3 - 2)

        return sum([rec_fuel(w) for w in self.weights]) - sum([w for w in self.weights])