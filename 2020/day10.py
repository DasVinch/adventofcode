import os
import numpy as np
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    '28',
    '33',
    '18',
    '42',
    '31',
    '14',
    '46',
    '20',
    '48',
    '47',
    '24',
    '23',
    '49',
    '45',
    '19',
    '38',
    '39',
    '11',
    '1',
    '32',
    '25',
    '35',
    '8',
    '17',
    '7',
    '9',
    '4',
    '2',
    '34',
    '10',
    '3',
]

REAL = get_input(DAYDAY, 2020)


class Day:

    def __init__(self, lines) -> None:
        self.jrates = [int(t) for t in lines]

    def solve1(self):
        jjrates = self.jrates.copy()
        jjrates.sort()
        jjrates = np.asarray([0] + jjrates + [jjrates[-1] + 3])
        h, v = np.histogram(jjrates[1:] - jjrates[:-1], 3, (0.5, 3.5))

        return h[0] * h[2]

    def solve2(self):
        finalval = max(self.jrates) + 3
        self.arran = {finalval: 1}
        return self.arrangements(0)
        

    def arrangements(self, val):
        #print(val)
        if val in self.arran:
            return self.arran[val]
        if val not in self.jrates and val > 0:
            return 0
        
        tot = self.arrangements(val+1) + self.arrangements(val+2) + self.arrangements(val+3)
        self.arran[val] = tot
        return tot





if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())