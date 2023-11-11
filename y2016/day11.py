from __future__ import annotations

import typing as typ

import enum
from enum import Enum
from typing import List, Set, Tuple

import itertools

T = typ.TypeVar('T')


class El(Enum):
    POLONIUM = 0
    THULIUM = 1
    PROMETHIUM = 2
    RUTHENIUM = 3
    COBALT = 4
    HYDROGEN = 5
    LITHIUM = 6
    ELERIUM = 7
    DILITHIUM = 8

class Obj(Enum):
    CHIP = 0
    GEN = 1

Item: typ.TypeAlias = typ.Tuple[El, Obj]
AFloorState: typ.TypeAlias = typ.Set[Item]

class FloorPlanWithElevator:
    def __init__(self, floors: list[AFloorState], elevator: int) -> None:
        self.floors = floors

        self.element_index: dict[El, int]

        self.elevator = elevator

    # We need a hash / repr that's element-permutation agnostic 
    def __repr__(self):
        self.unique_element_indexator()
        fs = self.floor_strings
        return f'{self.elevator}|[{fs[0]}][{fs[1]}][{fs[2]}][{fs[3]}]'

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other: FloorPlanWithElevator) -> bool:
        '''
        Need to hack both hash and eq to make dictionnary believe they're the same.
        '''
        return repr(self) == repr(other)


    def unique_element_indexator(self):
        self.element_index = {}

        self.floor_strings: list[str] = []

        next_key = 0
        for f in range(4):
            floor_str: list[str] = []
            # Begin with Els that are paired
            floor = self.floors[f]
            chips = {p[0] for p in floor if p[1] == Obj.CHIP}
            rtgs = {p[0] for p in floor if p[1] == Obj.GEN}

            both = list(chips.intersection(rtgs))
            both.sort(key = lambda el: el.value)

            only_chip = list(chips.difference(rtgs))
            only_chip.sort(key = lambda el: el.value)
            only_rtg = list(rtgs.difference(chips))
            only_rtg.sort(key = lambda el: el.value)

            for el in itertools.chain(both, only_chip, only_rtg):
                if not el in self.element_index:
                    self.element_index[el] = next_key
                    next_key += 1

            for el in both:
                floor_str += [f'{self.element_index[el]}M', f'{self.element_index[el]}G']
            for el in only_chip:
                floor_str += [f'{self.element_index[el]}M']
            for el in only_rtg:
                floor_str += [f'{self.element_index[el]}G']

            self.floor_strings += [''.join(floor_str)]


TESTFLOORS = FloorPlanWithElevator([
    {(El.HYDROGEN, Obj.CHIP), (El.LITHIUM, Obj.CHIP)},
    {(El.HYDROGEN, Obj.GEN)},
    {(El.LITHIUM, Obj.GEN)},
    set()
], 0)

TESTFLOORS_SUCCESS = FloorPlanWithElevator([set(), set(), set(),
                    {(El.HYDROGEN, Obj.CHIP), (El.LITHIUM, Obj.CHIP),
                     (El.HYDROGEN, Obj.GEN), (El.LITHIUM, Obj.GEN)}], 3)

REALFLOORS = FloorPlanWithElevator([
    {(El.POLONIUM, Obj.GEN), (El.THULIUM, Obj.GEN), (El.THULIUM, Obj.CHIP), (El.PROMETHIUM, Obj.GEN),
     (El.RUTHENIUM, Obj.GEN), (El.RUTHENIUM, Obj.CHIP), (El.COBALT, Obj.GEN), (El.COBALT, Obj.CHIP)},
    {(El.POLONIUM, Obj.CHIP), (El.PROMETHIUM, Obj.CHIP)},
    set(),
    set()
], 0)

REALFLOORS_SUCCESS = FloorPlanWithElevator([set(), set(), set(),
    {(El.POLONIUM, Obj.GEN), (El.THULIUM, Obj.GEN),
     (El.THULIUM, Obj.CHIP), (El.PROMETHIUM, Obj.GEN), 
     (El.RUTHENIUM, Obj.GEN), (El.RUTHENIUM, Obj.CHIP),
     (El.COBALT, Obj.GEN), (El.POLONIUM, Obj.CHIP),
     (El.PROMETHIUM, Obj.CHIP), (El.COBALT, Obj.CHIP)}], 3)

MOREREALFLOORS = FloorPlanWithElevator([
    {(El.POLONIUM, Obj.GEN), (El.THULIUM, Obj.GEN), (El.THULIUM, Obj.CHIP), (El.PROMETHIUM, Obj.GEN),
     (El.RUTHENIUM, Obj.GEN), (El.RUTHENIUM, Obj.CHIP), (El.COBALT, Obj.GEN), (El.COBALT, Obj.CHIP),
     (El.ELERIUM, Obj.CHIP), (El.ELERIUM, Obj.GEN), (El.DILITHIUM, Obj.CHIP), (El.DILITHIUM, Obj.GEN)},
    {(El.POLONIUM, Obj.CHIP), (El.PROMETHIUM, Obj.CHIP)},
    set(),
    set()
], 0)

MOREREALFLOORS_SUCCESS = FloorPlanWithElevator([set(), set(), set(),
    {(El.POLONIUM, Obj.GEN), (El.THULIUM, Obj.GEN),
     (El.THULIUM, Obj.CHIP), (El.PROMETHIUM, Obj.GEN), 
     (El.RUTHENIUM, Obj.GEN), (El.RUTHENIUM, Obj.CHIP),
     (El.COBALT, Obj.GEN), (El.POLONIUM, Obj.CHIP),
     (El.PROMETHIUM, Obj.CHIP), (El.COBALT, Obj.CHIP),
     (El.ELERIUM, Obj.CHIP), (El.ELERIUM, Obj.GEN),
     (El.DILITHIUM, Obj.CHIP), (El.DILITHIUM, Obj.GEN)}], 3)

def floorIsSafe(fstate: AFloorState) -> bool:
    if all((p[1] == Obj.CHIP for p in fstate)):
        return True
    
    chip_el = {p[0] for p in fstate if p[1] == Obj.CHIP}
    rtg_el = {p[0] for p in fstate if p[1] == Obj.GEN}
    return chip_el.issubset(rtg_el)
    
def stateIsSafe(fstate: FloorPlanWithElevator) -> bool:
    return all((floorIsSafe(floor) for floor in fstate.floors))

from tools import AbstractDijkstraer

class FloorDij(AbstractDijkstraer[FloorPlanWithElevator]):
    '''
    def validate_target(self, elem: FloorPlanWithElevator) -> bool:
        floorstate = elem.floors
        return len(floorstate[0]) == 0 and len(floorstate[1]) == 0 and len(floorstate[2]) == 0
    '''
    
    def get_neighbors(self, elem: FloorPlanWithElevator) -> Set[Tuple[FloorPlanWithElevator, int]]:
        neighbors: typ.Set[FloorPlanWithElevator] = set()

        currentfloors, elev = elem.floors, elem.elevator

        can_floors: list[int] = []
        if elev > 0: # can go down
            can_floors += [elev-1]

        if elev < 3: # can go up
            can_floors += [elev+1]


        floor_items_cpy = [currentfloor.copy() for currentfloor in currentfloors]
        current_floor_items = floor_items_cpy[elev]
        
        for item in current_floor_items:
            current_floor_items.remove(item)
            if floorIsSafe(current_floor_items):
                for k in can_floors:
                    floor_items_cpy[k].add(item)
                    if floorIsSafe(floor_items_cpy[k]):
                        neighbors.add(FloorPlanWithElevator([floor.copy() for floor in floor_items_cpy], k))
                    floor_items_cpy[k].remove(item)
            current_floor_items.add(item)

        seen: typ.Set[Tuple[Item, Item]] = set()
        for item1 in current_floor_items:
            for item2 in current_floor_items:
                if item1 == item2:
                    continue
                if (item2, item1) in seen:
                    continue
                seen.add((item1, item2))

                current_floor_items.remove(item1)
                current_floor_items.remove(item2)
                if floorIsSafe(current_floor_items):
                    for k in can_floors:
                        floor_items_cpy[k].add(item1)
                        floor_items_cpy[k].add(item2)
                        if floorIsSafe(floor_items_cpy[k]):
                            neighbors.add(FloorPlanWithElevator([floor.copy() for floor in floor_items_cpy], k))
                        floor_items_cpy[k].remove(item1)
                        floor_items_cpy[k].remove(item2)
                current_floor_items.add(item1)
                current_floor_items.add(item2)

        return {(n, 1) for n in neighbors}
        

        

if __name__ == '__main__':
    import time

    s = time.time()
    dj = FloorDij(TESTFLOORS, {TESTFLOORS_SUCCESS})
    dj.solveWithoutPath()
    print(dj.distanceDict[TESTFLOORS_SUCCESS], '-', time.time() - s)

    s = time.time()
    dj2 = FloorDij(REALFLOORS, {REALFLOORS_SUCCESS})
    dj2.solveWithoutPath()
    print(dj2.distanceDict[REALFLOORS_SUCCESS])
    print(dj2.distanceDict[REALFLOORS_SUCCESS], '-', time.time() - s)


    s = time.time()
    dj3 = FloorDij(MOREREALFLOORS, {MOREREALFLOORS_SUCCESS})
    dj3.solveWithoutPath()
    print(dj3.distanceDict[MOREREALFLOORS_SUCCESS])
    print(dj3.distanceDict[MOREREALFLOORS_SUCCESS], '-', time.time() - s)