import numpy as np
from enum import Enum
from tools import AbstractDijkstraer

REAL = (7, 721, 9171)  # x, y, depth
SAMPLE = (10, 10, 510)


class Day29:

    def __init__(self, a) -> None:
        self.depth = a[2]

        self.target = a[0], a[1]

        self.ero_row_prev = np.zeros(a[1] + 1, np.int64)
        self.ero_row = np.zeros(a[1] + 1, np.int64)

        #self.mat_debug = np.zeros((a[0]+1, a[1]+1), np.int64)

    def solve1(self):
        self.tot_risk = 0

        for x in range(self.target[0] + 1):
            for y in range(self.target[1] + 1):
                if (x, y) == (0, 0) or (x, y) == self.target:
                    gindex = 0
                elif y == 0:
                    gindex = x * 16807
                elif x == 0:
                    gindex = y * 48271
                else:
                    gindex = self.ero_row[y - 1] * self.ero_row_prev[y]

                elevel = (gindex + self.depth) % 20183
                elevel3 = elevel % 3

                self.ero_row[y] = elevel
                self.tot_risk += elevel3
                #self.mat_debug[x,y] = elevel3

            self.ero_row_prev = self.ero_row

        return self.tot_risk


class Gear(Enum):
    NONE = 0
    CLIMB = 1
    TORCH = 2


class Ter(Enum):
    ROCK = 0  # Torch or Climb
    WET = 1  # None or Climb
    NARROW = 2  # None or Torch


def okgear(terrain, gear):
    return ((terrain == Ter.ROCK and gear in (Gear.TORCH, Gear.CLIMB))
            or (terrain == Ter.WET and gear in (Gear.NONE, Gear.CLIMB))
            or (terrain == Ter.NARROW and gear in (Gear.TORCH, Gear.NONE)))


def othergear(terrain, gear):
    return {
        (Ter.ROCK, Gear.TORCH): Gear.CLIMB,
        (Ter.ROCK, Gear.CLIMB): Gear.TORCH,
        (Ter.WET, Gear.NONE): Gear.CLIMB,
        (Ter.WET, Gear.CLIMB): Gear.NONE,
        (Ter.NARROW, Gear.NONE): Gear.TORCH,
        (Ter.NARROW, Gear.TORCH): Gear.NONE,
    }[(terrain, gear)]


class DijkstraSolve(AbstractDijkstraer):

    def __init__(self, target, depth) -> None:
        super().__init__(((0, 0), Gear.TORCH), [(target, Gear.TORCH)])

        self.targetcoord = target

        self.depth = depth

        self.elevel = []

    def get_terrain(self, x, y):
        return Ter(self.get_elevel(x, y) % 3)

    def get_elevel(self, x, y):
        if len(self.elevel) > x and len(self.elevel[x]) > y:
            return self.elevel[x][y]
        else:
            self.expand_elevel(x, y)
            return self.elevel[x][y]

    def expand_elevel(self, x, y):
        if (x, y) == (0, 0) or (x, y) == self.targetcoord:
            gindex = 0
        elif y == 0:
            gindex = x * 16807
        elif x == 0:
            gindex = y * 48271
        else:
            gindex = self.get_elevel(x, y - 1) * self.get_elevel(x - 1, y)

        elevel = (gindex + self.depth) % 20183
        if len(self.elevel) > x:
            self.elevel[x].append(elevel)
        else:
            self.elevel.append([elevel])

        return elevel % 3

    def get_neighbors(self, elem):
        x, y = elem[0]
        gear = elem[1]
        neighbors = [(((x, y), othergear(self.get_terrain(x, y), gear)), 7)]
        if x > 0 and okgear(self.get_terrain(x - 1, y), gear):
            neighbors += [(((x - 1, y), gear), 1)]
        if y > 0 and okgear(self.get_terrain(x, y - 1), gear):
            neighbors += [(((x, y - 1), gear), 1)]
        if okgear(self.get_terrain(x + 1, y), gear):
            neighbors += [(((x + 1, y), gear), 1)]
        if okgear(self.get_terrain(x, y + 1), gear):
            neighbors += [(((x, y + 1), gear), 1)]

        return neighbors


if __name__ == "__main__":
    t = Day29(SAMPLE)
    print(t.solve1())
    r = Day29(REAL)
    print(r.solve1())

    t2 = DijkstraSolve((SAMPLE[0], SAMPLE[1]), SAMPLE[2])
    print(t2.solveWithoutPath())
    r2 = DijkstraSolve((REAL[0], REAL[1]), REAL[2])
    print(r2.solveWithoutPath())