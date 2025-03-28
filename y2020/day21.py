from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2020)

SAMPLE = [
'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
'trh fvjkl sbzzf mxmxvkd (contains dairy)',
'sqjhc fvjkl (contains soy)',
'sqjhc mxmxvkd sbzzf (contains fish)',
]



class Day:
    def __init__(self, lines: list[str]):
        
        self.recipes: list[tuple[set[str], set[str]]] = []

        self.all_ingredients: set[str] = set()
        self.all_allergens: set[str] = set()

        for line in lines:
            l = line.split(' (contains ')
            self.recipes += [(set(l[0].split()), set(l[1][:-1].split(', ')))]

            self.all_ingredients.update(self.recipes[-1][0])
            self.all_allergens.update(self.recipes[-1][1])

    def solve1(self):
        self.allergen_candidates: dict[str, set[str]] = {}

        for ings, allers in self.recipes:
            for allergen in allers:
                if not allergen in self.allergen_candidates:
                    self.allergen_candidates[allergen] = ings.copy()
                else:
                    self.allergen_candidates[allergen].intersection_update(ings)

        no_allergen_sure = self.all_ingredients.copy()
        for candidates in self.allergen_candidates.values():
            no_allergen_sure.difference_update(candidates)

        tot = 0
        for ings, _ in self.recipes:
            tot += len(ings.intersection(no_allergen_sure))

        return tot
        
    def solve2(self):
        return 0

if __name__ == '__main__':
    t = Day(SAMPLE)
    r = Day(REAL)

    print(f'Test p1: {t.solve1()}')

    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)
    '''

'eggs'     : {'dtb'},
'fish'     : {'zgk'},
'nuts'     : {'pxr'}
'peanuts'  : {'cqnl'},
'sesame'   : {'xkclg'},
'shellfish': {'xtzh'},
'soy'      : {'jpnv'},
'wheat'    : {'lsvlx'},

dtb,zgk,pxr,cqnl,xkclg,xtzh,jpnv,lsvlx

    '''