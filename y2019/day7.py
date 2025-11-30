from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] = ['3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0']

SAMPLE_P2: list[str] = ['3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5']

ADDITIONAL_SAMPLES: list[list[str]] = [
    ['3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'],
    ['3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0']
]

T_DATA: typ.TypeAlias = list[int] # TODO

import itertools

import importlib
from . import komputer
importlib.reload(komputer)
from .komputer import Komputer

class SubKomputer(Komputer):
    def __init__(self, ribbon: list[int]):
        super().__init__(ribbon)

        self.input_ctr: int = 0
        self.inputs: list[int] = []

        self.outputs: list[int] = []

    def get_input(self) -> int:
        val = self.inputs[self.input_ctr % len(self.inputs)]
        self.input_ctr += 1
        return val

    def output(self, val: int) -> None:
        self.outputs.append(val)

    def reset(self) -> None:
        super().reset()
        self.input_ctr = 0
        self.inputs = []



class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(t) for t in input[0].split(',')]
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        
        comp = SubKomputer(self.data)

        best_val = 0
        best_seq = ()
        for phases in itertools.permutations(range(5)):
            val = 0
            for ph in phases:
                comp.reset()
                comp.inputs = [ph, val]
                comp.execute_all()
                val = comp.outputs[0]

            if val > best_val:
                best_val = val
                best_seq = phases

        return best_val, best_seq

    def solve2(self) -> int:
        amplifiers = [SubKomputer(self.data) for _ in range(5)]

        best_val = 0
        best_seq = ()
        for phases in itertools.permutations(range(5,10)):
            val = 0
            for ph, comp in zip(phases, amplifiers):
                comp.reset()
                comp.inputs = [ph]

            comp_ptr = 0
            amplifiers[0].inputs.append(val)
            while True:
                comp = amplifiers[comp_ptr]
                #print(comp_ptr, comp.ip, comp.ribbon[comp.ip])

                while comp.ribbon[comp.ip] not in (4,99):
                    comp.execute_one_instruction()
                
                if comp_ptr == 0 and comp.ribbon[comp.ip] == 99:
                    break

                comp.execute_one_instruction() # 4
                
                val = comp.outputs[-1]
                #print(comp_ptr, val)
                #import pdb;pdb.set_trace()
                comp_ptr = (comp_ptr + 1) % 5 # incr
                amplifiers[comp_ptr].inputs.append(val)


            if val > best_val:
                best_val = val
                best_seq = phases
        
        return best_val, best_seq