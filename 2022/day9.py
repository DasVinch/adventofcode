from tools import get_input
import numpy as np

SAMPLE = [
    'R 4',
    'U 4',
    'L 3',
    'D 1',
    'R 4',
    'D 1',
    'L 5',
    'R 2',
]

SAMPLE2 = [
    'R 5',
    'U 8',
    'L 8',
    'D 3',
    'R 17',
    'D 10',
    'L 25',
    'U 20',
]

MOVES = {
    'U': np.array([0, 1]),
    'R': np.array([1, 0]),
    'L': np.array([-1, 0]),
    'D': np.array([0, -1]),
}

REAL = get_input(9, 2022)

class Snek:
    def __init__(self, lines, n) -> None:
        self.moves = [l.split()[0] for l in lines]
        self.count = [int(l.split()[1]) for l in lines]

        self.n = n
        self.T = np.zeros((n, 2), np.int32)

    def singlemove(self, dir):
        self.T[0] += MOVES[dir]
        for ii in range(1, self.n):
            diff = self.T[ii-1] - self.T[ii]
            if (diff[0]**2 + diff[1]**2) > 2:
                self.T[ii] += np.clip(diff, -1, 1)

    def solve(self):
        visited = set()
        visited.add(tuple(self.T[-1]))
        for dir, ctot in zip(self.moves, self.count):
            for c in range(ctot):
                self.singlemove(dir)
                visited.add(tuple(self.T[-1]))

        return len(visited)

if __name__ == "__main__":
    t = Snek(SAMPLE, 2)
    print(t.solve())
    r = Snek(REAL, 2)
    print(r.solve())

    t = Snek(SAMPLE, 10)
    print(t.solve())
    t2 = Snek(SAMPLE2, 10)
    print(t2.solve())
    r = Snek(REAL, 10)
    print(r.solve())