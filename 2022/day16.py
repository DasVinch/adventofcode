import os
from tools import get_input
import numpy as np
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
    'Valve HH has flow rate=22; tunnel leads to valve GG',
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
    'Valve JJ has flow rate=21; tunnel leads to valve II',
]

REAL = get_input(DAYDAY, 2022)

RE = re.compile('Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)')

class Day:
    def __init__(self, lines) -> None:
        self.nodes = [] # all the 2-letter nodes

        self.flow = {} # node: flow

        self.neighbors = {} # node: list[node]

        self.nonzerosnodes = [] # list[node] if flow[node] > 0

        for l in lines:
            #print(l)
            #print(RE.findall(l))
            grps = RE.findall(l)[0]
            self.nodes.append(grps[0])
            self.flow[grps[0]] = int(grps[1])
            if self.flow[grps[0]] > 0:
                self.nonzerosnodes.append(grps[0])

            self.neighbors[grps[0]] = grps[2].split(', ')

        self.nodesidx = {node: idx for idx,node in enumerate(self.nodes)}

        # Make non-zeros bitmasks
        self.masks = {} # node: bitmask of node if flow[node] > 0

        b = 1
        for node in self.nonzerosnodes:
            self.masks[node] = b
            b <<= 1

    def computerelease(self, mask):
        return sum([self.flow[node] for node in self.masks if self.masks[node] & mask])


    def solve1(self):
        self.part1memo = {} # (node, mask, time): maxflow
        return self.solve1rec('AA', 0x0, 30)

    def solve1rec(self, node, mask, time):
        if time == 0:
            # Too late bruh
            return 0

        if (node, mask, time) in self.part1memo:
            return self.part1memo[(node, mask, time)]

        
        # What's going anyway
        now = self.computerelease(mask)
        # I open the current valve
        if self.flow[node] > 0 and not mask & self.masks[node]:
            wopen = self.solve1rec(node, mask | self.masks[node], time-1)
        else:
            wopen = 0
        # I move
        wmove = [self.solve1rec(n, mask, time-1) for n in self.neighbors[node]]

        result = now + max(max(wmove), wopen)


        self.part1memo[(node, mask, time)] = result

        return result

    def solve2(self):
        # Mkaaayyy this takes ballpark 2 hours for part 2...
        # It would be much much shorter by popping 0-flow nodes and reducing the graph
        # to a weighted graph with less nodes.
        # Maybe another time!

        import tqdm
        self.part2memo = np.zeros((60,60,2, 2**16, 26), np.uint16) # (node, mask, time): maxflow

        self.trange = tqdm.trange(35000)
        k = self.solve2rec('AA', 'AA', True, 0x0, 26)
        self.trange.close()
        return k

    def solve2rec(self, nodeme, nodeel, meorel: bool, mask: int, time: int):
        if time == 0:
            # Too late bruh
            return 0

        idxme = self.nodesidx[nodeme]
        idxel = self.nodesidx[nodeel]
        if time == 20:
            self.trange.update()

        if time < 26:
            k =  self.part2memo[idxme, idxel, int(meorel), mask, time]
            if k > 0:
                return k

        if meorel:
            now = self.computerelease(mask)
        else:
            now = 0
        
        wopen = 0
        if meorel:
            if self.flow[nodeme] > 0 and not mask & self.masks[nodeme]:
                wopen = self.solve2rec(nodeme, nodeel, False, mask | self.masks[nodeme], time)
        else:
            if self.flow[nodeel] > 0 and not mask & self.masks[nodeel]:
                wopen = self.solve2rec(nodeme, nodeel, True, mask | self.masks[nodeel], time-1)
        if meorel:
            # I move
            wmove = [self.solve2rec(n, nodeel, False, mask, time) for n in self.neighbors[nodeme]]
        else:
            # Elephant moves
            wmove = [self.solve2rec(nodeme, n, True, mask, time-1) for n in self.neighbors[nodeel]]

        result = now + max(max(wmove), wopen)

        if time < 26:
            self.part2memo[idxme, idxel, int(meorel), mask, time] = result

        return result

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    #print(r.solve1())