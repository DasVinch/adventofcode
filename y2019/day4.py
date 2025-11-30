from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = ['264793-803935']

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = tuple[int, int] # TODO


def has_double(number: int) -> bool:
    n = number
    for k in range(5):
        if n % 10 == (n // 10) % 10:
            return True
        n //= 10
    
    return False

def has_triple(number: int) -> bool:
    n = number
    for k in range(4):
        if n % 10 == (n // 10) % 10 and n % 10 == (n // 100) % 10:
            return True
        n //= 10
    
    return False

def never_decreasing(number: int) -> bool:
    n = number
    val = n % 10
    while n > 0:
        n //= 10
        if n % 10 > val:
            return False
        val = n % 10

    return True

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        a, b = input[0].split('-')
        return int(a), int(b)
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.debug = debug
        self.low, self.high = data

    def solve1(self) -> int:
        count = 0
        for ii in range(self.low, self.high+1):
            if has_double(ii) and never_decreasing(ii):
                count += 1

        return count

    def solve2(self) -> int:
        count = 0
        for ii in range(self.low, self.high+1):
            if has_double(ii) and never_decreasing(ii):
                s = str(ii)
                for d in range(10):
                    if str(d) * 2 in s and not str(d) * 3 in s:
                        count += 1
                        break

        return count