from tools import get_input
import numpy as np

SAMPLE = [
    '199',
    '200',
    '208',
    '210',
    '200',
    '207',
    '240',
    '269',
    '260',
    '263',
]

class Day1:
    def __init__(self, lines) -> None:
        self.data = np.asarray([int(k) for k in lines])

    def solve1(self) -> int:
        return np.sum(self.data[1:] > self.data[:-1])

    def solve2(self) -> int:
        windows = self.data[:-2] + self.data[1:-1] + self.data[2:]
        return np.sum(windows[1:] > windows[:-1])

if __name__ == "__main__":
    test = Day1(SAMPLE)
    print(test.solve2())
    real = Day1(get_input(1, 2021))
    print(real.solve2())