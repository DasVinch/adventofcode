import os
from tools import get_input
import typing as typ
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])
REAL = get_input(DAYDAY, 2023)

SAMPLE = [
'seeds: 79 14 55 13',
'',
'seed-to-soil map:',
'50 98 2',
'52 50 48',
'',
'soil-to-fertilizer map:',
'0 15 37',
'37 52 2',
'39 0 15',
'',
'fertilizer-to-water map:',
'49 53 8',
'0 11 42',
'42 0 7',
'57 7 4',
'',
'water-to-light map:',
'88 18 7',
'18 25 70',
'',
'light-to-temperature map:',
'45 77 23',
'81 45 19',
'68 64 13',
'',
'temperature-to-humidity map:',
'0 69 1',
'1 0 69',
'',
'humidity-to-location map:',
'60 56 37',
'56 93 4',
]

from dataclasses import dataclass

@dataclass
class RawRange:
    dest: int
    source: int
    extent: int

    def applicable(self, val: int) -> bool:
        if val >= self.source and val < self.source + self.extent:
            return True
        else:
            return False
        
    def apply(self, val: int) -> int:
        return self.dest + (val - self.source)
    
@dataclass
class SeedRange:
    start: int
    extent: int

    def __hash__(self) -> int:
        return (self.start, self.extent).__hash__()


def apply_range_to_range(seed: SeedRange, rule: RawRange) -> tuple[typ.Optional[SeedRange], set[SeedRange]]:
    if seed.start >= rule.source and seed.start + seed.extent <= rule.source + rule.extent:
        # seed inside rule
        return SeedRange(rule.dest + seed.start - rule.source, seed.extent), set()
    
    if seed.start >= rule.source and seed.start <= rule.source + rule.extent:
        # start inside but overshoot to the right
        return (SeedRange(rule.dest + seed.start - rule.source, rule.source + rule.extent - seed.start),
                {SeedRange(rule.source + rule.extent, seed.extent - rule.source - rule.extent + seed.start)})
    
    if seed.start < rule.source and seed.start + seed.extent > rule.source + rule.extent:
        # start at the left and contain entirely
        return SeedRange(rule.dest, rule.extent), {SeedRange(seed.start, rule.source - seed.start), SeedRange(rule.source + rule.extent, seed.extent - rule.extent + seed.start - rule.source)}
    
    if seed.start < rule.source and seed.start + seed.extent > rule.source:
        # start at the left and finish within
        return SeedRange(rule.dest, seed.extent + seed.start - rule.source), {SeedRange(seed.start, rule.source - seed.start)}
    
    # no overlap
    return None, {seed}
    
assert apply_range_to_range(SeedRange(0,10), RawRange(100, 0, 50)) == (SeedRange(100, 10), set())
assert apply_range_to_range(SeedRange(5,10), RawRange(100, 0, 50)) == (SeedRange(105, 10), set())
assert apply_range_to_range(SeedRange(0,10), RawRange(100, 0, 5)) == (SeedRange(100, 5), {SeedRange(5,5)})
assert apply_range_to_range(SeedRange(-5,15), RawRange(100, 0, 8)) == (SeedRange(100, 8), {SeedRange(-5,5), SeedRange(8,2)})
assert apply_range_to_range(SeedRange(-5,15), RawRange(100, 0, 10)) == (SeedRange(100, 10), {SeedRange(-5,5)})
assert apply_range_to_range(SeedRange(-5,13), RawRange(100, 0, 10)) == (SeedRange(100, 8), {SeedRange(-5,5)})


def apply_conversion_p2(seedranges: set[SeedRange], rules: list[RawRange]) -> set[SeedRange]:
    remaining_ranges = seedranges.copy()
    new_ranges: set[SeedRange] = set()
    for rule in rules:
        new_remaining_ranges: set[SeedRange] = set()
        for seedrange in remaining_ranges:
            a, b = apply_range_to_range(seedrange, rule)
            if a is not None:
                new_ranges.add(a)
            new_remaining_ranges.update(b)
        remaining_ranges, new_remaining_ranges = new_remaining_ranges, set()

    new_ranges.update(remaining_ranges)

    return new_ranges


def apply_conversion(val: int, rules: list[RawRange]):
    for rule in rules:
        if rule.applicable(val):
            return rule.apply(val)
    return val

def parse_rules(lines: list[str]) -> list[list[RawRange]]:
    # Let's recurse, mofo
    all_ranges: list[list[RawRange]] = []
    curr_ranges: list[RawRange] = []
    for line in lines:
        if line == '': # Close
            all_ranges += [curr_ranges]
            curr_ranges = []
        elif 'map:' in line:
            continue
        else:
            curr_ranges += [RawRange(*[int(x) for x in line.split()])]

    return all_ranges


class Day:
    def __init__(self, lines: list[str], debug: bool = False):
        self.seeds = [int(x) for x in lines[0].split(':')[1].strip().split()]
        self.seed_ranges = [SeedRange(a,b) for a,b in zip(self.seeds[::2], self.seeds[1::2])]

        self.lines = lines
        self.ranges = parse_rules(self.lines[2:] + [''])
        self.debug = debug

        if self.debug:
            pass

    def solve1(self) -> int:
        self.values = self.seeds.copy() 

        for ruleset in self.ranges:
            self.values = [apply_conversion(x, ruleset) for x in self.values]

        return min(self.values)


    def solve2(self) -> int:
        ranges = self.seed_ranges.copy()
        for k, ruleset in enumerate(self.ranges):
            ranges = apply_conversion_p2(ranges, ruleset)
            if self.debug:
                    print(k, len(ranges))

        return min({r.start for r in ranges})



if __name__ == "__main__":
    t = Day(SAMPLE, debug=True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')
