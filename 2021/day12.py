from tools import get_input
import numpy as np

SMOL = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]

SAMPLE = [
    'dc-end',
    'HN-start',
    'start-kj',
    'dc-start',
    'dc-HN',
    'LN-dc',
    'HN-end',
    'kj-sa',
    'kj-HN',
    'kj-dc',
]

RESAMPLE = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW',
]


class Day12:

    def __init__(self, lines) -> None:
        self.nodes = set()
        self.edges = {}
        self.flagged = {}

        for line in lines:
            a, b = line.split('-')
            if not a in self.nodes:
                self.nodes.add(a)
                self.edges[a] = set()
                self.flagged[a] = False
            self.edges[a].add(b)
            if not b in self.nodes:
                self.nodes.add(b)
                self.edges[b] = set()
                self.flagged[b] = False
            self.edges[b].add(a)
            

    def solve1rec(self, path) -> int:
        item = path[-1]
        if item == 'end':
            return 1

        if item.islower():
            self.flagged[item] = True
        
        count = 0
        for nex in self.edges[item]:
            if not self.flagged[nex]:
                count += self.solve1rec(path + [nex])
        
        self.flagged[item] = False
        
        return count



    def solve1(self) -> int:
        return self.solve1rec(['start'])

    def solve2rec(self, path) -> int:
        item = path[-1]
        if item == 'start' and self.flagged['start']:
            return 0
        if item == 'end':
            return 1

        if item.islower():
            if self.flagged[item]:
                self.double = item
            self.flagged[item] = True
        
        count = 0
        for nex in self.edges[item]:
            if (not self.flagged[nex]) or (self.double is None):
                count += self.solve2rec(path + [nex])
        
        if item == self.double:
            self.double = None
        else:
            self.flagged[item] = False
        
        return count



    def solve2(self) -> int:
        self.double = None
        return self.solve2rec(['start'])

if __name__ == "__main__":
    test = Day12(SMOL)
    print(test.solve2())
    test2 = Day12(SAMPLE)
    print(test2.solve2())
    test3 = Day12(RESAMPLE)
    print(test3.solve2())
    real = Day12(get_input(12, 2021))
    print(real.solve2())