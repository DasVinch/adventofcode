import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

# We're gonna use 9-bit bitset for this.
ROCKS = [
    (
        0b000111100, ),
    (
        0b000010000,
        0b000111000,
        0b000010000,
    ),
    (
        0b000001000,
        0b000001000,
        0b000111000,
    ),
    (
        0b000100000,
        0b000100000,
        0b000100000,
        0b000100000,
    ),
    (
        0b000110000,
        0b000110000,
    ),
]

BASE = 0b111111111
WALL = 0b100000001
HOLE = 0b011111110

SAMPLE = ['>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>']

REAL = get_input(DAYDAY, 2022)

def dbg(*args, **kwargs):
    #print(*args, **kwargs)
    pass

class Day:

    def __init__(self, lines) -> None:
        self.pushlist = lines[0]
        self.n_push = len(self.pushlist)
        self.next_push = 0

        self.n_rocks = len(ROCKS)
        self.next_rock = 0

        self.stack = [BASE]
        self.true_height = 1

    def push_stone(self, rock_id):
        # Expand the stack so the stone fits.
        rock = ROCKS[rock_id]

        need_add = self.true_height + 3 + len(rock) - len(self.stack)
        if need_add > 0:
            self.stack += [WALL] * need_add
            need_add = 0

        # Set the stone at the top
        rock_height = len(self.stack) - len(rock) + need_add

        while True:
            rock = self.wind(rock, self.pushlist[self.next_push % self.n_push], rock_height)
            self.next_push += 1
            dbg(rock)
            dbg(self)

            if self.drop(rock, rock_height):
                rock_height -= 1
                dbg("Drop")
                dbg(self)
            else:
                self.settle(rock, rock_height)
                dbg("Settle.")
                dbg(self)
                self.true_height = max(self.true_height, rock_height + len(rock))
                dbg(f"True height: {self.true_height}")
                break
    
    def settle(self, rock, height):
        for k, h in enumerate(range(height, height+len(rock))):
            self.stack[h] |= rock[-k-1]

    def drop(self, rock, height):
        return not any([r & s for (r,s) in zip(rock[::-1], self.stack[height-1:height-1+len(rock)])])

    def wind(self, rock, push, height):
        if push == '<':
            if any([(r << 1) & s for (r,s) in zip(rock[::-1], self.stack[height:height+len(rock)])]):
                dbg("NoPush <")
                return rock
            else:
                dbg("Push <")
                return tuple([r << 1 for r in rock])
        else: # '>'
            if any([(r >> 1) & s for (r,s) in zip(rock[::-1], self.stack[height:height+len(rock)])]):
                dbg("NoPush >")
                return rock
            else:
                dbg("Push >")
                return tuple([r >> 1 for r in rock])

    def __str__(self):
        return '\n'.join([bin(x)[2:].replace('0','.') for x in self.stack[::-1]])


    def solve1(self):
        from tqdm import trange
        for i in trange(2022):
            self.push_stone(i % 5)
        return self.true_height - 1

    def solve2(self):



        from tqdm import trange
        for i in trange(50455*7):
            self.push_stone(i % 5)
        a = self.true_height - 1
        for i in trange(50455*7):
            self.push_stone(i % 5)
        b = self.true_height - 1
        
        cychei = b - a
        print(f'cychei: {cychei}')

        n_remains = 1000000000000 - 2 * 50455*7
        n_cycs = n_remains // (50455*7)

        n_extra = n_remains % (50455*7)

        for i in trange(n_extra):
            self.push_stone(i % 5)

        return self.true_height - 1 + cychei * n_cycs


        return 



if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    t2 = Day(SAMPLE)
    print(t2.solve2())
    r = Day(REAL)
    print(r.solve1())
    r2 = Day(REAL)
    print(r2.solve2())
