import os
from tools import get_input, make_cmapped_int_matrix

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#',
]

REAL = get_input(DAYDAY, 2020)


class Day:

    def __init__(self, lines) -> None:
        self.data = make_cmapped_int_matrix(lines, {'.': 0, '#': 1})
        self.r, self.c = self.data.shape

        self.dirr = 1
        self.dirc = 3

    def solve1(self):
        treehit = 0
        posr = 0
        posc = 0
        while posr < self.r:
            if self.data[posr, posc % self.c]:
                treehit += 1
            posr += self.dirr
            posc += self.dirc

        return treehit


    def solve2(self):
        tot = 1
        for cc, rr in zip([1,3,5,7,1], [1,1,1,1,2]):
            self.dirr = rr
            self.dirc = cc
            print(self.solve1(), end= ' ')
            tot *= self.solve1()
        print()
        return tot


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())