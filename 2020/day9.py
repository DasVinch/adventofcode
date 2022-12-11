import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [int(n) for n in [
'35',
'20',
'15',
'25',
'47',
'40',
'62',
'55',
'65',
'95',
'102',
'117',
'150',
'182',
'127',
'219',
'299',
'277',
'309',
'576',
]]

REAL = [int(n) for n in get_input(DAYDAY, 2020)]


class Day:
    def __init__(self, numbers, preamb=25) -> None:
        self.numbers = numbers
        self.valids = []
        self.preamb = preamb
        for ii in range(self.preamb):
            v = []
            for jj in range(self.preamb):
                if ii != jj:
                    v += [self.numbers[ii] + self.numbers[jj]]
                else:
                    v += [-1.234]
            self.valids += [v]

    def solve1(self):
        n = len(self.numbers)
        for kk in range(self.preamb, n):
            #import pdb; pdb.set_trace()
            if not any([self.numbers[kk] in v for v in self.valids]):
                return self.numbers[kk]

            self.valids.pop(0)
            for k, v in enumerate(self.valids):
                v.pop(0)
                v.append(self.numbers[kk] + self.numbers[kk - self.preamb + k + 1])
            self.valids.append([self.numbers[kk] + self.numbers[kk - self.preamb + k + 1] for k in range(self.preamb)])
            self.valids[-1][-1] = -1.234



    def solve2(self):
        # No need to be smart. 1000 is OK
        target = self.solve1()
        for ii in range(len(self.numbers)):
            acc = self.numbers[ii]
            minn = self.numbers[ii]
            maxx = self.numbers[ii]
            for jj in range(ii+1, len(self.numbers)):
                acc += self.numbers[jj]
                minn = min(minn, self.numbers[jj])
                maxx = max(maxx, self.numbers[jj])
                if acc == target:
                    return minn + maxx


if __name__ == "__main__":
    t = Day(SAMPLE, 5)
    print(t.solve2())
    r = Day(REAL, 25)
    print(r.solve2())
