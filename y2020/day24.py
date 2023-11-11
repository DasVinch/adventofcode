import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'sesenwnenenewseeswwswswwnenewsewsw',
    'neeenesenwnwwswnenewnwwsewnenwseswesw',
    'seswneswswsenwwnwse',
    'nwnwneseeswswnenewneswwnewseswneseene',
    'swweswneswnenwsewnwneneseenw',
    'eesenwseswswnenwswnwnwsewwnwsene',
    'sewnenenenesenwsewnenwwwse',
    'wenwwweseeeweswwwnwwe',
    'wsweesenenewnwwnwsenewsenwwsesesenwne',
    'neeswseenwwswnwswswnw',
    'nenwswwsewswnenenewsenwsenwnesesenew',
    'enewnwewneswsewnwswenweswnenwsenwsw',
    'sweneswneswneneenwnewenewwneswswnese',
    'swwesenesewenwneswnwwneseswwne',
    'enesenwswwswneneswsenwnewswseenwsese',
    'wnwnesenesenenwwnenwsewesewsesesew',
    'nenewswnwewswnenesenwnesewesw',
    'eneswnwswnwsenenwnwnwwseeswneewsenese',
    'neswnwewnwnwseenwseesewsenwsweewe',
    'wseweeenwnesenwwwswnew',
]

REAL = get_input(DAYDAY, 2020)


class Day:

    def __init__(self, lines) -> None:
        self.lines = lines
        self.coords = [self.parseline(l) for l in lines]

    def solve1(self):
        self.tiles = {}
        for c in self.coords:
            v = self.tiles.get(c, 0)
            self.tiles[c] = 1 - v

        return sum([self.tiles[c] for c in self.tiles])

    def parseline(self, l):
        p = 0
        x, y = 0, 0
        while p < len(l):
            if l[p] == 'e':
                x += 1
                p += 1
            elif l[p] == 'w':
                x -= 1
                p += 1
            elif l[p:p + 2] == 'ne':
                y += 1
                p += 2
            elif l[p:p + 2] == 'nw':
                x -= 1
                y += 1
                p += 2
            elif l[p:p + 2] == 'se':
                x += 1
                y -= 1
                p += 2
            elif l[p:p + 2] == 'sw':
                y -= 1
                p += 2

        return (x, y)

    # BLACK is 1
    # WHITE is 0
    def expandblackneighbors(self):
        expandedtiles = {}
        for x, y in self.tiles:
            if self.tiles[(x, y)] == 1:
                expandedtiles[(x + 1, y)] = self.tiles.get((x + 1, y), 0)
                expandedtiles[(x - 1, y)] = self.tiles.get((x - 1, y), 0)
                expandedtiles[(x, y + 1)] = self.tiles.get((x, y + 1), 0)
                expandedtiles[(x, y - 1)] = self.tiles.get((x, y - 1), 0)
                expandedtiles[(x + 1, y - 1)] = self.tiles.get((x + 1, y - 1),
                                                               0)
                expandedtiles[(x - 1, y + 1)] = self.tiles.get((x - 1, y + 1),
                                                               0)

        expandedtiles.update(self.tiles)  # existing values supersede.
        self.tiles = expandedtiles

    def update_day(self):
        newstatus = {}
        for x, y in self.tiles:
            this = self.tiles[(x, y)]
            neivals = [
                self.tiles.get((x + 1, y), 0),
                self.tiles.get((x - 1, y), 0),
                self.tiles.get((x, y + 1), 0),
                self.tiles.get((x, y - 1), 0),
                self.tiles.get((x + 1, y - 1), 0),
                self.tiles.get((x - 1, y + 1), 0),
            ]
            snei = sum(neivals)
            if this == 1 and (snei == 0 or snei > 2):
                newstatus[(x, y)] = 0
            elif this == 0 and snei == 2:
                newstatus[(x, y)] = 1
            else:
                newstatus[(x, y)] = this

        self.tiles = newstatus

    def solve2(self):
        # Assume 1 has ran.

        for _ in range(100):
            self.expandblackneighbors()
            self.update_day()

        return sum([self.tiles[c] for c in self.tiles])


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())