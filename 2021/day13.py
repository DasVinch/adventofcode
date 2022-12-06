from tools import get_input
import numpy as np

SAMPLE = [
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5',
]


class Day13:

    def __init__(self, lines) -> None:
        blank = lines.index('')
        points = [[int(t) for t in l.split(',')] for l in lines[:blank]]

        folds = [l.split()[-1] for l in lines[blank+1:]]
        # x fold True, y fold False
        self.dirfold = np.asarray([l.split('=')[0] == 'x' for l in folds])
        self.idxfold = np.asarray([int(l.split('=')[1]) for l in folds])
        maxx = max(self.idxfold[self.dirfold])
        maxy = max(self.idxfold[~self.dirfold])

        self.paper = np.zeros((2 * maxx + 1, 2 * maxy + 1), np.bool)

        for p in points:
            self.paper[p[0], p[1]] = True

    def fold(self, dir, idx):
        if dir: # x fold
            self.paper = self.paper[:idx, :] | self.paper[:-idx-1:-1, :]
        else:
            self.paper = self.paper[:, :idx] | self.paper[:, :-idx-1:-1]

    def solve1(self) -> int:
        self.fold(self.dirfold[0], self.idxfold[0])
        return np.sum(self.paper)


    def solve2(self) -> int:
        for d, i in zip(self.dirfold, self.idxfold):
            self.fold(d,i)

    def __str__(self):
        s = ''
        for row in self.paper.T:
            for char in row:
                s += (' ', '#')[bool(char)]
            s += '\n'

        return s


if __name__ == "__main__":
    test = Day13(SAMPLE)
    test.solve2()
    print(test)
    real = Day13(get_input(13, 2021))
    real.solve2()