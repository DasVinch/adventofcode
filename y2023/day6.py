import os
from tools import get_input
import typing as typ
import re
import math

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

SAMPLE = [
    (7, 9), (15, 40), (30, 200)
]

REAL = [
    (48, 390), (98, 1103), (90, 1112), (83, 1360)
]

SAMPLE2 = (71530, 940200)
REAL2 = (48989083, 390110311121360)

def solve_race(time: int, record: int) -> int:
    '''
        x(time-x) = record
        -x**2 + Tx - record = 0
        x**2 - Tx + record = 0

        == (X-T/2)**2 + V
        solve for X-T/2 == V**.5
    '''
    v = (time**2 / 4 - record)**.5
    
    #print(time, record, is_int)

    if time % 2 == 0:
        return 2*math.ceil(v) - 1
    else:
        return 2*math.ceil(v+1/2) - 2


class Day:
    def __init__(self, races: list[tuple[int, int]], debug: bool = False):
        
        self.races = races
        self.debug = debug

    def solve1(self) -> int:
        tot = 1
        for race in self.races:
            tot *= solve_race(*race)
            if self.debug:
                print(race, solve_race(*race))

        return tot

    def solve2(self) -> int:
        return 0



if __name__ == "__main__":
    t = Day(SAMPLE, debug=True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t2 = Day([SAMPLE2], debug=True)
    print(f'Test p2: {t2.solve1()}')

    r2 = Day([REAL2])
    print(f'Real p2: {r2.solve1()}')