import os
import numpy as np
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '498,4 -> 498,6 -> 496,6',
    '503,4 -> 502,4 -> 502,9 -> 494,9',
]

REAL = get_input(DAYDAY, 2022)

SAND = 2
ROCK = 1
AIR = 0

class Day:

    def __init__(self, lines) -> None:
        self.pointlists = []
        for l in lines:
            ps = l.split(' -> ')
            pts = np.asarray([(int(p.split(',')[0]),int(p.split(',')[1])) for p in ps])
            self.pointlists += [pts]

        self.gmx = min([np.min(pl[:,0]) for pl in self.pointlists])
        self.gMx = max([np.max(pl[:,0]) for pl in self.pointlists])
        self.gmy = 0
        self.gMy = max([np.max(pl[:,1]) for pl in self.pointlists])

        self.offset_x = self.gmx - 1


        self.matrepr = np.zeros((self.gMy+3, self.gMx - self.gmx + 3), np.int32)

        for ptssublist in self.pointlists:
            prevp = ptssublist[0]
            for p in ptssublist[1:]:
                if prevp[1] == p[1]:
                    sl = (prevp[0]-self.offset_x,p[0]-self.offset_x)
                    self.matrepr[prevp[1], min(sl): max(sl)+1] = ROCK
                else:
                    sl = prevp[1], p[1]
                    self.matrepr[min(sl):max(sl)+1, prevp[0]-self.offset_x] = ROCK
                prevp = p

    def solve1(self, mode=1):
        count = 0
        done = False
        while True:
            x, y = 500 - self.offset_x, 0
            while True:
                if y == self.gMy+2:
                    if mode == 2:
                        count += 1
                    else:
                        done = True
                    break

                if self.matrepr[y+1, x] == 0:
                    y += 1
                elif self.matrepr[y+1, x-1] == 0:
                    y += 1
                    x -= 1
                elif self.matrepr[y+1, x+1] == 0:
                    y += 1
                    x += 1
                else:
                    self.matrepr[y, x] = SAND
                    count += 1
                    if x == 500 - self.offset_x and y == 0:
                        done = True
                    break

            if done:
                break
        return count

    def solve2(self):
        k = self.matrepr.shape[0]
        self.matrepr = np.c_[np.zeros((k ,k), np.int32), self.matrepr, np.zeros((k ,k), np.int32)]
        self.offset_x -= k
        self.matrepr[-1] = ROCK

        self.solve1(mode=2) # this give a subestimated count...

        return np.sum(self.matrepr == 2)

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())