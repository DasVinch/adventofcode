import os
from tools import get_input

from tqdm import trange

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

    def __str__(self, n = None):
        if n is None:
            return '\n'.join([bin(x)[2:].replace('0','.') for x in self.stack[::-1]])
        else:
            return '\n'.join([bin(x)[2:].replace('0','.') for x in self.stack[:-n:-1]])


    def solve1(self):
        for i in trange(2022):
            self.push_stone(i % 5)
        return self.true_height - 1

    def solve2(self):
        import math
        lcm = math.lcm(self.n_push, self.n_rocks)
        
        height_o_stacks: list[int] = []
        step_o_stacks: list[int] = []
        stack_o_stacks: list[list[int]] = []

        ctr = 0
        while True:
            ctr += 1
            for ii in trange(lcm):
                self.push_stone(ii % 5)
            stack_b = self.stack[-30:].copy()
            b = self.true_height - 1
            b_s = ctr * lcm
            if stack_b in stack_o_stacks:
                k = stack_o_stacks.index(stack_b)
                stack_a = stack_o_stacks[k]
                a = height_o_stacks[k]
                a_s = step_o_stacks[k]
                break
            height_o_stacks.append(b)
            step_o_stacks.append(b_s)
            stack_o_stacks.append(stack_b)

        assert stack_a == stack_b
        cyc_hei = b - a
        cyc_len = b_s - a_s
        
        print(f'cyc_hei: {cyc_hei}')
        print(f'cyc_len: {cyc_len}')

        n_remains = 1_000_000_000_000 - b_s
        n_cycs = n_remains // cyc_len

        n_extra = n_remains % cyc_len

        for ii in trange(n_extra):
            self.push_stone(ii % 5)

        return self.true_height - 1 + cyc_hei * n_cycs



if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    
    t2 = Day(SAMPLE)
    print(t2.solve2())

    r = Day(REAL)
    print(r.solve1())
    r2 = Day(REAL)
    print(r2.solve2())
