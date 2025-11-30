from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = ['1,9,10,3,2,3,11,0,99,30,40,50']

T_DATA: typ.TypeAlias = list[int]  #TODO


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(x) for x in input[0].split(',')]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data_orig = data
        self.debug = debug

    def solve1(self) -> int:
        if self.debug:
            return self.run_computer(None, None)
        else:
            return self.run_computer(12, 2)

    def run_computer(self, noun: int | None, verb: int | None) -> int:
        data = self.data_orig.copy()
        if noun is not None:
            data[1] = noun
        if verb is not None:
            data[2] = verb

        ptr = 0
        while True:
            val = data[ptr]
            if val == 99:
                break
            if val == 1:
                data[data[ptr + 3]] = data[data[ptr + 1]] + data[data[ptr + 2]]
            if val == 2:
                data[data[ptr + 3]] = data[data[ptr + 1]] * data[data[ptr + 2]]
            ptr += 4

        return data[0]

    def solve2(self) -> int:
        if self.debug:
            return -1
        for noun in range(100):
            for verb in range(100):
                t = self.run_computer(noun, verb)
                if t == 19690720:
                    return 100 * noun + verb
        return -1