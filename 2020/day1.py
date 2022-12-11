from tools import get_input

SAMPLE = [int(t) for t in [
    '1721',
    '979',
    '366',
    '299',
    '675',
    '1456',
]]


REAL = [int(t) for t in get_input(1, 2020)]

class Day1:
    def __init__(self, l) -> None:
        self.l = l

    def solve(self):
        vals = set()
        for t in self.l:
            if 2020-t in vals:
                return t * (2020-t)
            else:
                vals.add(t)

    def solve2(self):
        vals = {}
        for k,t in enumerate(self.l):
            if 2020-t in vals:
                v = vals[2020-t]
                return v[0]*v[1]*t
            else:
                for vv in self.l[:k]:
                    vals[t + vv] = (t, vv)

if __name__ == "__main__":
    t = Day1(SAMPLE)
    print(t.solve2())
    r = Day1(REAL)
    print(r.solve2())