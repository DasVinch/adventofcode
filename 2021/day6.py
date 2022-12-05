from tools import get_input
import numpy as np

SAMPLE = [
    '3,4,3,1,2'
]


class Day6:

    def __init__(self, lines) -> None:
        self.data = [int(t) for t in lines[0].split(',')]

        self.values = {k: 0 for k in range(9)}

        for d in self.data:
            self.values[d] += 1

    def nextday(self):
        nrep = self.values[0]

        for k in range(1,9):
            self.values[k-1] = self.values[k]
        self.values[6] += nrep
        self.values[8] = nrep

    def solve1(self) -> int:
        for k in range(80):
            self.nextday()

        return sum((self.values[k] for k in self.values))


    def solve2(self) -> int:
        for k in range(256):
            self.nextday()

        return sum((self.values[k] for k in self.values))


if __name__ == "__main__":
    test = Day6(SAMPLE)
    print(test.solve2())
    real = Day6(get_input(6, 2021))
    print(real.solve2())