from tools import get_input
import numpy as np

SAMPLE = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]


class Day5:

    def __init__(self, lines) -> None:
        self.data = np.zeros((len(lines), 4), np.int32)

        for kk, line in enumerate(lines):
            self.data[kk] = [int(t) for t in line.replace(' -> ', ',').split(',')]



    def solve1(self) -> int:
        mmax = np.max(self.data) + 1
        self.matrix = np.zeros((mmax, mmax), np.int32)
        for a,b,c,d in self.data:
            if a == c:
                x,y = min(b,d), max(b,d)
                self.matrix[a, x:y+1] += 1
            elif b == d:
                x,y = min(a,c), max(a,c)
                self.matrix[x:y+1, b] += 1

        return np.sum(self.matrix > 1)

    def solve2(self) -> int:
        mmax = np.max(self.data) + 1
        self.matrix = np.zeros((mmax, mmax), np.int32)
        for a,b,c,d in self.data:
            if a == c:
                x,y = min(b,d), max(b,d)
                self.matrix[a, x:y+1] += 1
            elif b == d:
                x,y = min(a,c), max(a,c)
                self.matrix[x:y+1, b] += 1
            else: # diagonal
                #print(a,b,c,d)
                for x, y in zip(range(a, c, (1, -1)[c < a]), range(b,d, (1, -1)[d < b])):
                    self.matrix[x,y] += 1
                self.matrix[c,d] += 1


        return np.sum(self.matrix > 1)


if __name__ == "__main__":
    test = Day5(SAMPLE)
    print(test.solve2())
    real = Day5(get_input(5, 2021))
    print(real.solve2())