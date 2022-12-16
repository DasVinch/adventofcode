import os
from tools import get_input
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
]

REAL = get_input(DAYDAY, 2022)


class Day:
    def __init__(self, lines) -> None:
        pass

    def solve1(self):
        pass

    def solve2(self):
        pass

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())