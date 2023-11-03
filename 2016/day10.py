import typing as typ

from tools import get_input, print_bool_matrix
import numpy as np

from tqdm import tqdm

import re

SAMPLES = [
    'value 5 goes to bot 2',
    'bot 2 gives low to bot 1 and high to bot 0',
    'value 3 goes to bot 1',
    'bot 1 gives low to output 1 and high to bot 0',
    'bot 0 gives low to output 2 and high to output 0',
    'value 2 goes to bot 2',
]

REAL = get_input(10, 2016)

re_value = re.compile('^value (\d+) goes to bot (\d+)$')
re_botrule = re.compile('^bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)')

class Day10:
    def __init__(self, lines: typ.List[str]) -> None:
        self.lines = lines

        self.bots: typ.Dict[int, typ.List[int]] = {} # With outputs as negatives - 1.
        self.botrules: typ.Dict[int, typ.Tuple[int,int]] = {}

        for line in self.lines:
            if m := re_value.match(line):
                g = m.groups()
                self.bots[int(g[1])] = self.bots.get(int(g[1]), []) + [int(g[0])]
            elif m := re_botrule.match(line):
                g = m.groups()
                self.botrules[int(g[0])] = (
                    int(g[2]) if g[1] == 'bot' else -1 * int(g[2]) - 1,
                    int(g[4]) if g[3] == 'bot' else -1 * int(g[4]) - 1
                )
            else:
                raise AssertionError("Dafuko?")
            
    def resolve_for_61_17(self, stop_at_compare: typ.Optional[typ.Tuple[int, int]] = None):
        while True:
            made_action = False

            # Could be more efficient... find A bot with lenght 2.
            found = False
            for bot, chips in self.bots.items():
                if bot >= 0 and len(chips) == 2:
                    found = True
                    break # good bot!
            if not found:
                break
            
            if stop_at_compare:
                if stop_at_compare[0] in chips and stop_at_compare[1] in chips:
                    print(bot, chips, '!!')
                    break
            
            made_action = True
            m, mm = min(chips), max(chips)
            self.bots[self.botrules[bot][0]] = self.bots.get(self.botrules[bot][0], []) + [m]
            self.bots[self.botrules[bot][1]] = self.bots.get(self.botrules[bot][1], []) + [mm]
            self.bots[bot] = []

            if not made_action:
                break
    

if __name__ == '__main__':
    t = Day10(SAMPLES)
    t.resolve_for_61_17((2,5))
    r = Day10(REAL)
    r.resolve_for_61_17((17,61))
    r = Day10(REAL)
    r.resolve_for_61_17(None)
    print(r.bots[-1], r.bots[-2], r.bots[-3])
    print(r.bots[-1][0]* r.bots[-2][0]* r.bots[-3][0])

