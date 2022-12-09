# Let's solve the first star bruteforce.

from tools import get_input
import numpy as np

SAMPLE = [
    'on x=-20..26,y=-36..17,z=-47..7',
    'on x=-20..33,y=-21..23,z=-26..28',
    'on x=-22..28,y=-29..23,z=-38..16',
    'on x=-46..7,y=-6..46,z=-50..-1',
    'on x=-49..1,y=-3..46,z=-24..28',
    'on x=2..47,y=-22..22,z=-23..27',
    'on x=-27..23,y=-28..26,z=-21..29',
    'on x=-39..5,y=-6..47,z=-3..44',
    'on x=-30..21,y=-8..43,z=-13..34',
    'on x=-22..26,y=-27..20,z=-29..19',
    'off x=-48..-32,y=26..41,z=-47..-37',
    'on x=-12..35,y=6..50,z=-50..-2',
    'off x=-48..-32,y=-32..-16,z=-15..-5',
    'on x=-18..26,y=-33..15,z=-7..46',
    'off x=-40..-22,y=-38..-28,z=23..41',
    'on x=-16..35,y=-41..10,z=-47..6',
    'off x=-32..-23,y=11..30,z=-14..3',
    'on x=-49..-5,y=-3..45,z=-29..18',
    'off x=18..30,y=-20..-8,z=-3..13',
    'on x=-41..9,y=-7..43,z=-33..15',
]

REAL = get_input(22,2021)

class Day22:

    def __init__(self, lines, shortonly: bool = True):
        self.onoff = []
        self.slices = []

        for line in lines:
            onoff = line.split()[0] == 'on'
            right = line.split()[1]
            xyz = [(int(s.split('=')[1].split('..')[0]),
                    int(s.split('=')[1].split('..')[1]))
                   for s in right.split(',')]
            if shortonly and np.any(np.abs(np.asarray(xyz)) > 50):
                break
            self.onoff += [onoff]
            self.slices += [
                np.s_[xyz[0][0] + 50:xyz[0][1] + 51,
                      xyz[1][0] + 50:xyz[1][1] + 51,
                      xyz[2][0] + 50:xyz[2][1] + 51]
            ]

    def solve1(self):
        cubezone = np.zeros((101, 101, 101), np.bool)
        for k in range(len(self.onoff)):
            cubezone[self.slices[k]] = self.onoff[k]

        return np.sum(cubezone)
