import os
from tools import get_input
import numpy as np
import re
import logging

from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.',
    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.',
]

REAL = get_input(DAYDAY, 2022)

RE = re.compile('Each ore robot costs (\d+) ore. '
                'Each clay robot costs (\d+) ore. '
                'Each obsidian robot costs (\d+) ore and (\d+) clay. '
                'Each geode robot costs (\d+) ore and (\d+) obsidian.')


class M(IntEnum):
    ORE = 0
    CLAY = 1
    OBS = 2
    GEODE = 3


NAMES = ["ORE", "CLAY", "OBSIDIAN", "GEODE"]


class Blueprint:

    def __init__(self, a: int, b: int, c: int, d: int, e: int, f: int) -> None:
        self.costMatrix = np.zeros((4, 4), np.int32)
        self.costMatrix[M.ORE, M.ORE] = a
        self.costMatrix[M.CLAY, M.ORE] = b
        self.costMatrix[M.OBS, M.ORE] = c
        self.costMatrix[M.OBS, M.CLAY] = d
        self.costMatrix[M.GEODE, M.ORE] = e
        self.costMatrix[M.GEODE, M.OBS] = f

        # self.costMatrix[toBuild] = cost[ore, clay, obs, geode]

    def solve(self, time=24):
        self.branches = 0
        self.maxall = 0
        self.max_seen_geodes = 0
        bots = np.array([1, 0, 0, 0])
        loot = np.array([0, 0, 0, 0])

        self.known_max = 0

        return self.solveRec2(time, bots, loot)

    def solveRec2(self, time: int, bots: np.ndarray,
                  supplies: np.ndarray) -> int:
        #print(time, bots, supplies)
        if time == 1:
            ret = supplies[3] + bots[3]
            if ret > self.known_max:
                self.known_max = ret
            return ret

        if supplies[3] + bots[3] * time + (time*(time-1)) // 2 < self.known_max:
            return 0

        turns_to_next_bot_per_resource = (self.costMatrix - supplies[None, :]) // bots[None, :]
        turns_to_next_bot_per_resource[((self.costMatrix - supplies[None, :]) % bots[None, :]) > 0] += 1

        turns_to_next_bot_per_resource = np.clip(turns_to_next_bot_per_resource, 0, None)

        where_nan = (bots[None, :] == 0) & (self.costMatrix > 0)

        turns_to_next_bot_per_resource[where_nan] = 32766

        turns_to_next_bot = np.max(turns_to_next_bot_per_resource, axis=1)

        # Rec calls
        # Add input for no more purchases
        res = [0, 0, 0, 0, supplies[3] + bots[3] * time]
        for k in range(3,-1,-1):
            arr_k = np.array([0, 0, 0, 0])
            arr_k[k] = 1
            if time - turns_to_next_bot[k] - 1 > 0 and (
                    k == 3 or bots[k] < np.max(self.costMatrix[:, k])):
                res[k] = self.solveRec2(
                    time - turns_to_next_bot[k] - 1, bots + arr_k, supplies +
                    bots * (turns_to_next_bot[k] + 1) - self.costMatrix[k])

        return np.max(res)

    def solveRec(self, time: int, bots: np.ndarray, loot: np.ndarray,
                 couldbuild: np.ndarray):

        self.branches += 1
        if time == 0:
            self.max_seen_geodes = max(self.max_seen_geodes, loot[3])
            return loot[3]
        if time == 1:
            ret = loot[3] + bots[3]
            self.max_seen_geodes = max(self.max_seen_geodes, ret)
            return ret

        maxhopefulgeode = loot[3] + time * bots[3] + (time * (time + 1)) // 2
        if maxhopefulgeode <= self.max_seen_geodes:
            return 0  # Hopeless branch

        # Check what I can build
        builds = np.all(loot[None, :] >= self.costMatrix, axis=1)

        newbuildsidx = np.where(builds & ~couldbuild)[0]
        #logging.info(' ' * (26 - time) + f'Builds {builds}')
        #logging.info(' ' * (26 - time) + f'New builds {newbuildsidx}')

        # Increase resources
        new_loot = loot + bots
        #logging.info(' ' * (26 - time) + f'Newloot {new_loot}')

        # We're gonna hope REALLY hard that we can never build two robots
        # all of a sudden on the same turn
        recursive_results = []

        blacklist = np.all(bots[:, None] >= self.costMatrix, axis=0)
        for buildidx in newbuildsidx[::-1]:
            #logging.info(' ' * (26 - time) + f'Time {time} - build {NAMES[buildidx]}...')
            new_bots = bots.copy()
            new_bots[buildidx] += 1
            res = self.solveRec(time - 1, new_bots,
                                new_loot - self.costMatrix[buildidx],
                                blacklist)
            recursive_results += [res]

            #logging.info(' ' * (26 - time) + f'returned a max of {res}')

        # Actually, wait?
        #logging.info(' ' * (26 - time) + f'Time {time} - wait...')
        res = self.solveRec(time - 1, bots, new_loot, builds | blacklist)
        recursive_results += [res]
        #logging.info(' ' * (26 - time) + f'returned a max of {res}')

        # Decide to build for just-unlocked decisions or to wait.
        return max(recursive_results)


class Day:

    def __init__(self, blueprints: list[str]) -> None:
        self.blueprints = [Blueprint(*RE.findall(b)[0]) for b in blueprints]

    def solve1(self):
        tot = 0
        for k, b in enumerate(self.blueprints):
            bb = b.solve()
            print(k+1, bb)
            tot += (k+1) * bb

        return tot

    def solve2(self):
        tot = 1
        for k, b in enumerate(self.blueprints[:3]):
            bb = b.solve(32)
            print(k+1, bb)
            tot *= bb

        return tot


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    b1 = Blueprint(4, 2, 3, 14, 2, 7)
    b2 = Blueprint(2, 3, 3, 8, 3, 12)

    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve2())
