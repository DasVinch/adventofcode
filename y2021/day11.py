from tools import get_input
import numpy as np

SMOL = [
    '11111',
    '19991',
    '19191',
    '19991',
    '11111',
]

SAMPLE = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]


class Day11:

    def __init__(self, lines) -> None:
        self.octopus = np.asarray([[int(t) for t in s] for s in lines])
        self.flashed = np.zeros_like(self.octopus, np.bool)
        self.mo, self.no = self.octopus.shape

    def next(self):
        self.octopus += 1
        self.flashed[:,:] = False
        while True:
            octoready = np.where(self.octopus > 9)
            if len(octoready[0]) == 0 or np.all(self.flashed[octoready]):
                break
            for r, c in zip(octoready[0], octoready[1]):
                if self.flashed[r,c]:
                    continue
                self.flashed[r,c] = True
                self.octopus[r,c] = 0
                for rr in [r-1, r, r+1]:
                    for cc in [c-1, c, c+1]:
                        if rr >= 0 and rr < self.mo and cc >= 0 and cc < self.no:
                            self.octopus[rr,cc] +=  1

        self.octopus[self.flashed] = 0


    def solve1(self) -> int:
        totflash = 0
        for ii in range(100):
            self.next()
            totflash += np.sum(self.flashed)
        return totflash

    def solve2(self) -> int:
        k = 0
        while True:
            self.next()
            k += 1
            if np.all(self.flashed):
                return k

if __name__ == "__main__":
    test = Day11(SAMPLE)
    print(test.solve2())
    real = Day11(get_input(11, 2021))
    print(real.solve2())