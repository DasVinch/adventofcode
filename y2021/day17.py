import numpy as np

# (xmin, xmax, ymin, ymax)
TARGET_TEST = (20, 30, -10, -5)
TARGET_REAL = (209, 238, -86, -59)


class Launch:

    def __init__(self, targetzone, xv, yv):
        self.x = 0
        self.y = 0
        self.maxy = 0
        self.xv = xv
        self.yv = yv

        self.target = targetzone

    def success(self):
        if (self.x >= self.target[0] and self.x <= self.target[1]
                and self.y >= self.target[2] and self.y <= self.target[3]):
            return 1
        elif ((self.x > self.target[1])
              or ((self.xv == 0) and (self.x < self.target[0]))
              or (self.y < self.target[2])):
            return -1
        else:
            return 0

    def next(self):
        self.x += self.xv
        self.y += self.yv
        if self.xv > 0:
            self.xv -= 1
        elif self.xv < 0:
            self.xv += 1
        self.yv -= 1

        if self.y > self.maxy:
            self.maxy = self.y

    def resolve(self):
        while self.success() == 0:
            self.next()
        return self.success()

    def asymptoticx(self):
        while self.xv != 0:
            self.next()
        return self.x


def solve1(TARGET):

    asympt_cand = []
    for xv in range(TARGET[1]):
        t = Launch(TARGET, xv, 0)
        xx = t.asymptoticx()
        if (xx >= TARGET[0]) and (xx <= TARGET[1]):
            asympt_cand += [xv]

    ymax = 0
    for xv in asympt_cand:
        for yv in range(-TARGET[2] + 1):
            t = Launch(TARGET, xv, yv)
            if t.resolve() == 1:
                if t.maxy > ymax:
                    ymax = t.maxy
                    print(ymax, xv, yv)
    
    return ymax

def solve2(TARGET):
    count = 0
    for xv in range(TARGET[1]+1):
        for yv in range(TARGET[2]-1, -TARGET[2]+1):
            t = Launch(TARGET, xv, yv)
            if t.resolve() == 1:
                count += 1

    return count



if __name__ == "__main__":
    #print(solve1(TARGET_REAL))
    print(solve2(TARGET_REAL))
