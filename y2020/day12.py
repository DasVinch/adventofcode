import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.ns = 0
        self.ew = 0
        self.nsw = 1
        self.eww = 10
        self.dir = 90

    def solve1(self):
        for l in self.lines:
            n = int(l[1:])
            if l[0] == 'N':
                self.ns += n
            elif l[0] == 'S':
                self.ns -= n
            elif l[0] == 'E':
                self.ew += n
            elif l[0] == 'W':
                self.ew -= n
            elif l[0] == 'R':
                self.dir = (self.dir + n) % 360
            elif l[0] == 'L':
                self.dir = (self.dir - n) % 360
            elif l[0] == 'F':
                if self.dir == 0:
                    self.ns += n
                elif self.dir == 90:
                    self.ew += n
                elif self.dir == 180:
                    self.ns -= n
                elif self.dir == 270:
                    self.ew -= n
        return abs(self.ns) + abs(self.ew)

    def rotatewp(self, ang):
        if ang == 90:
            self.nsw, self.eww = -self.eww, self.nsw
        elif ang == 180:
            self.nsw, self.eww = -self.nsw, -self.eww
        elif ang == 270:
            self.nsw, self.eww = self.eww, -self.nsw

    def solve2(self):
        for l in self.lines:
            n = int(l[1:])
            if l[0] == 'N':
                self.nsw += n
            elif l[0] == 'S':
                self.nsw -= n
            elif l[0] == 'E':
                self.eww += n
            elif l[0] == 'W':
                self.eww -= n
            elif l[0] == 'R':
                self.rotatewp(n)
            elif l[0] == 'L':
                self.rotatewp(360-n)
            elif l[0] == 'F':
                self.ns += n * self.nsw
                self.ew += n * self.eww
        return abs(self.ns) + abs(self.ew)

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())