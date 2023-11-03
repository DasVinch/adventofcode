from tools import AbstractDijkstraer

import typing as typ

TEST = 10
TARGET_TEST = (7, 4)

REAL = 1364
TARGET_REAL = (31, 39)


def polyOpen(x: int,y: int,c: int) -> bool:
    val = x*x + 3*x + 2*x*y + y + y*y + c
    return val.bit_count() % 2 == 0

class Day13Dijk(AbstractDijkstraer):

    def __init__(self, start, targets, magicnumber) -> None:
        super().__init__(start, targets)

        self.magic = magicnumber

    def get_neighbors(
        self, elem: typ.Tuple[int, int]
    ) -> typ.Iterable[typ.Tuple[typ.Tuple[int, int], int]]:
        x, y = elem
        neighbors = []
        if x > 0 and polyOpen(x - 1, y, self.magic):
            neighbors += [((x - 1, y), 1)]
        if y > 0 and polyOpen(x, y - 1, self.magic):
            neighbors += [((x, y - 1), 1)]
        if polyOpen(x + 1, y, self.magic):
            neighbors += [((x + 1, y), 1)]
        if polyOpen(x, y + 1, self.magic):
            neighbors += [((x, y + 1), 1)]
        
        return neighbors


if __name__ == '__main__':
    t = Day13Dijk((1, 1), [TARGET_TEST], TEST)
    print(t.solveWithoutPath())
    r = Day13Dijk((1, 1), [TARGET_REAL], REAL)
    print(r.solveWithoutPath())
    
    # Part 2:
    print(len([d for d in r.distanceDict.values() if d <= 50]))