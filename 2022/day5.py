from tools import get_input

SAMPLE = [
    '    [D]    ',
    '[N] [C]    ',
    '[Z] [M] [P]',
    ' 1   2   3 ',
    '',
    'move 1 from 2 to 1',
    'move 3 from 1 to 3',
    'move 2 from 2 to 1',
    'move 1 from 1 to 2 ',
]


class Day5:

    def __init__(self, inputlines):
        self.lines = inputlines

        prefixlen = -1

        for ii in range(len(self.lines)):
            if self.lines[ii] == '':
                prefixlen = ii - 1
                break

        self.n = int(self.lines[prefixlen].split()[-1])

        self.stacks = {k: [] for k in range(self.n)}

        for line in self.lines[:prefixlen][::-1]:
            for kk in range(self.n):
                if 4 * kk + 1 >= len(line):
                    break
                if line[4 * kk + 1] != ' ':
                    self.moveinto(line[4 * kk + 1], kk)

        self.moves = []
        self.bigmove = []
        for line in self.lines[prefixlen+2:]:
            _, a, _, b, _, c = line.split()
            self.bigmove += [(int(b)-1, int(c)-1, int(a))]
            for kk in range(int(a)):
                self.moves += [(int(b)-1, int(c)-1)]

    def moveinto(self, crate, n: int):
        self.stacks[n].append(crate)

    def movemany(self, n, fro: int, to: int):
        self.stacks[to] += self.stacks[fro][-n:]
        self.stacks[fro] = self.stacks[fro][:-n]

    def solve1(self) -> str:
        for a,b in self.moves:
            self.moveinto(self.stacks[a].pop(-1), b)
        return ''.join([self.stacks[n][-1] for n in range(self.n)])

    def solve2(self) -> str:
        for a, b, n in self.bigmove:
            self.movemany(n,a,b)
        return ''.join([self.stacks[n][-1] for n in range(self.n)])


if __name__ == "__main__":
    test = Day5(SAMPLE)
    print(test.stacks)
    #print(test.solve1())
    print(test.solve2())
    real = Day5(get_input(5))
    print(real.stacks)
    #print(real.solve1())
    print(real.solve2())
