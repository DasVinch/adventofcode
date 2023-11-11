from tools import get_input
import numpy as np

SAMPLE8 = [ # Expect 8
    '1,-1,-1,-2',
    '-2,-2,0,1',
    '0,2,1,3',
    '-2,3,-2,1',
    '0,2,3,-2',
    '-1,-1,1,-2',
    '0,-2,-1,0',
    '-2,2,3,-1',
    '1,2,2,0',
    '-1,-2,0,-2',
]

SAMPLE4 = [
    '-1,2,2,0',
    '0,0,2,-2',
    '0,0,0,-2',
    '-1,2,0,0',
    '-2,-2,-2,2',
    '3,0,2,-1',
    '-1,3,2,2',
    '-1,0,-1,0',
    '0,2,1,-2',
    '3,0,0,0',
]

REAL = get_input(25, 2018)

class Day25:
    def __init__(self, lines) -> None:
        self.stars = [tuple([int(t) for t in l.split(',')]) for l in lines]

    def solve1(self):
        const = []
        
        for star in self.stars:
            found = []
            for k, c in enumerate(const):
                for o in c:
                    if abs(star[0] - o[0]) + abs(star[1] - o[1]) + abs(star[2] - o[2]) + abs(star[3] - o[3]) <= 3:
                        found += [k]
                        break
            
            if len(found) > 0:
                const[found[0]].add(star)
            if len(found) > 1:
                for merge in found[1:]:
                    const[found[0]] = const[found[0]].union(const[merge])
                    const[merge] = None
                const = [c for c in const if c != None]
            if len(found) == 0:
                const += [{star}]

        return len(const)

if __name__ == "__main__":
    t4 = Day25(SAMPLE4)
    print(t4.solve1())
    t8 = Day25(SAMPLE8)
    print(t8.solve1())
    r = Day25(REAL)
    print(r.solve1())

