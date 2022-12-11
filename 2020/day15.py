import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [0, 3, 6]

REAL = [14,8,16,0,1,17]


class Day:
    def __init__(self, initsequence) -> None:
        self.memory = {v: k for (k,v) in enumerate(initsequence[:-1])}
        self.lastnumber = initsequence[-1]
        self.turns = len(initsequence)-1

    def turn(self):
        if self.lastnumber in self.memory:
            p = self.lastnumber
            self.lastnumber = self.turns - self.memory[p]
            self.memory[p] = self.turns
        else:
            self.memory[self.lastnumber] = self.turns
            self.lastnumber = 0

        self.turns += 1


    def solve1(self):
        while self.turns < 2020 - 1:
            #print(self.lastnumber)
            self.turn()
        return self.lastnumber

    def solve2(self):
        while self.turns < 30000000 - 1:
            #print(self.lastnumber)
            self.turn()
            if self.turns % 100000 == 0:
                print(self.turns)
        return self.lastnumber

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())