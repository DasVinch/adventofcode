from tools import get_input
import numpy as np

SAMPLE = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]


class Day3:

    def __init__(self, lines) -> None:
        bindig = [[int(d) for d in l] for l in lines]
        self.dmat = np.asarray(bindig)

    def solve1(self) -> int:
        r = self.dmat.shape[0]
        res = np.sum(self.dmat, axis=0) >= r // 2
        g, e = 0, 0
        for b in res:
            g *= 2
            g += b
            e *= 2
            e += 1 - b

        return g * e

    def solve2(self) -> int:
        oxy = self.dmat.copy()
        bit = 0
        while oxy.shape[0] > 1:
            r = oxy.shape[0]
            most_common = np.sum(oxy[:, bit]) >= r / 2
            oxy = oxy[oxy[:, bit] == most_common]
            bit += 1
        co2 = self.dmat.copy()
        bit = 0 
        while co2.shape[0] > 1:
            r = co2.shape[0]
            most_common = np.sum(co2[:, bit]) >= r / 2
            co2 = co2[co2[:, bit] == 1 - most_common]
            bit += 1
        o, c = 0, 0
        for kk in range(co2.shape[1]):
            o *= 2
            o += oxy[0, kk]
            c *= 2
            c += co2[0, kk]
        return o * c


if __name__ == "__main__":
    test = Day3(SAMPLE)
    print(test.solve2())
    real = Day3(get_input(3, 2021))
    print(real.solve2())