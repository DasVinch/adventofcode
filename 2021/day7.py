from tools import get_input
import numpy as np

SAMPLE = [
    '16,1,2,0,4,2,7,1,2,14'
]


class Day7:

    def __init__(self, lines) -> None:
        self.data = np.array([int(t) for t in lines[0].split(',')], np.int32)

    def fuel(self,v):
        return np.sum(np.abs(self.data - v))

    def fuel2(self,v):
        t = np.abs(self.data - v)
        return np.sum((t * (t + 1)) // 2)

    def solve1(self) -> int:
        med = int(np.median(self.data))
        return self.fuel(med)

    def solve2(self) -> int:
        target = int(np.median(self.data))
        mmin = self.data.min()
        mmax = self.data.max()
        print(mmin, target, mmax)

        f = self.fuel2(target)
        a, b = self.fuel2(target-1), self.fuel2(target+1)
        while a < f or b < f:
            if a < f:
                mmax = target
                target = (mmin + target) // 2
            else:
                mmin = target
                target = (mmax + target) // 2

            f = self.fuel2(target)
            a, b = self.fuel2(target-1), self.fuel2(target+1)

            if mmin == mmax:
                print('Abort')
                break
        
        return f



if __name__ == "__main__":
    test = Day7(SAMPLE)
    print(test.solve2())
    real = Day7(get_input(7, 2021))
    print(real.solve2())