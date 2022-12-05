from tools import get_input
import numpy as np

SAMPLE = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
]



class Day2:

    def __init__(self, lines) -> None:
        self.vmove = []
        self.hmove = []

        self.seq_act = []
        self.seq_val = []

        for l in lines:
            m, n = l.split()
            self.seq_act += [m[0]]
            self.seq_val += [int(n)]
            if m[0] == 'f':
                self.hmove += [int(n)]
            elif m[0] == 'u':
                self.vmove += [-int(n)]
            elif m[0] == 'd':
                self.vmove += [int(n)]

    def solve1(self) -> int:
        return sum(self.vmove) * sum(self.hmove)

    def solve2(self) -> int:
        horz = 0
        depth = 0
        aim = 0
        for act, val in zip(self.seq_act, self.seq_val):
            if act == 'u':
                aim -= val
            if act == 'd':
                aim += val
            if act == 'f':
                horz += val
                depth += aim * val

        return depth * horz



if __name__ == "__main__":
    test = Day2(SAMPLE)
    print(test.solve2())
    real = Day2(get_input(2, 2021))
    print(real.solve2())