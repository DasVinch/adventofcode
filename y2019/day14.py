from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = [
    '171 ORE => 8 CNZTR',
    '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
    '114 ORE => 4 BHXH',
    '14 VRPVC => 6 BMBT',
    '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
    '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
    '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
    '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
    '5 BMBT => 4 WPTQ',
    '189 ORE => 9 KTJDG',
    '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
    '12 VRPVC, 27 CNZTR => 2 XDBXC',
    '15 KTJDG, 12 BHXH => 5 XCVML',
    '3 BHXH, 2 VRPVC => 7 MZWV',
    '121 ORE => 7 VRPVC',
    '7 XCVML => 6 RJRHP',
    '5 BHXH, 4 VRPVC => 5 LTCX',
]

ADDITIONAL_SAMPLES: list[list[str]] = [
    [
        '2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG',
        '17 NVRVD, 3 JNWZP => 8 VPVL',
        '53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL',
        '22 VJHF, 37 MNCFX => 5 FWMGM',
        '139 ORE => 4 NVRVD',
        '144 ORE => 7 JNWZP',
        '5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC',
        '5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV',
        '145 ORE => 6 MNCFX',
        '1 NVRVD => 8 CXFTF',
        '1 VJHF, 6 MNCFX => 4 RFSQX',
        '176 ORE => 6 VJHF',
    ],
    [
        '9 ORE => 2 A',
        '8 ORE => 3 B',
        '7 ORE => 5 C',
        '3 A, 4 B => 1 AB',
        '5 B, 7 C => 1 BC',
        '4 C, 1 A => 1 CA',
        '2 AB, 3 BC, 4 CA => 1 FUEL',
    ],
    [
        '157 ORE => 5 NZVS',
        '165 ORE => 6 DCFZ',
        '44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL',
        '12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ',
        '179 ORE => 7 PSHF',
        '177 ORE => 5 HKGWZ',
        '7 DCFZ, 7 PSHF => 2 XJWVT',
        '165 ORE => 2 GPVTF',
        '3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT',
    ],
    [
        '10 ORE => 10 A',
        '1 ORE => 1 B',
        '7 A, 1 B => 1 C',
        '7 A, 1 C => 1 D',
        '7 A, 1 D => 1 E',
        '7 A, 1 E => 1 FUEL',
    ],
]

from dataclasses import dataclass


@dataclass(frozen=False)
class Eqn:
    makes: str
    num: int
    how: list[tuple[str, int]]


T_DATA: typ.TypeAlias = list[Eqn]  # TODO


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        eqns: list[Eqn] = []

        for eqn_str in input:
            source, end = eqn_str.split(' => ')
            count, product = end.split(' ')

            makes = source.split(', ')

            eqns += [
                Eqn(product, int(count),
                    [(m.split()[1], int(m.split()[0])) for m in makes])
            ]

        return eqns

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

        self.eqn_dict = {e.makes: e for e in self.data}

    def solve1(self, how_much_fuel: int = 1) -> int:
        self.needs: dict[str, int] = {'FUEL': how_much_fuel}
        needed_ore: int = 0
        self.has_extra: dict[str, int] = {}

        while len(self.needs) > 0:
            make_what, need_how_much = self.needs.popitem()

            assert need_how_much > 0

            make_eqn = self.eqn_dict[make_what]
            if need_how_much - self.has_extra.get(make_what, 0) == 0:
                eqn_coefficient = 0
            else:
                eqn_coefficient = (need_how_much - self.has_extra.get(
                    make_what, 0) - 1) // make_eqn.num + 1

            for prod, cost in make_eqn.how:
                if prod == 'ORE':
                    needed_ore += eqn_coefficient * cost
                else:
                    x = self.needs.get(prod, 0) + eqn_coefficient * cost
                    if x > 0:
                        self.needs[prod] = x

            # del self.needs[make_what] # Already popped!
            self.has_extra[make_what] = self.has_extra.get(
                make_what, 0) + eqn_coefficient * make_eqn.num - need_how_much

            if self.debug:
                print(
                    f'{need_how_much} of {make_what} -- made {eqn_coefficient * make_eqn.num} -- now having extra {self.has_extra[make_what]}'
                )
                print(f'Now needing ORE {needed_ore} and {self.needs}')

        print('-----------------------')
        return needed_ore

    def solve2(self) -> int:
        x = self.solve1(3_687_786)  # (3_687_785, 3_687_787)
        if x <= 1_000_000_000_000:
            print('Can make more.')
        else:
            print('Too ambitious.')
        return x
