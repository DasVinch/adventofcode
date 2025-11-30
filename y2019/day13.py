from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = list[int] # TODO

from .komputer import Komputer

from enum import IntEnum

class Joy(IntEnum):
    Z = 0
    L = -1
    R = 1

class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(t) for t in input[0].split(',')]
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

    def solve1(self) -> int:
        comp = Komputer(self.data)

        comp.execute_all()

        tiles: set[tuple[int, int]] = set()

        for k in range(len(comp.outputs) // 3):
            if comp.outputs[3*k + 2] == Tile.BLOCK: # block
                tiles.add((comp.outputs[3*k], comp.outputs[3*k+1]))

        return len(tiles)

    def solve2(self) -> int:
        comp = Komputer(self.data)
        comp.ribbon[0] = 2
        score = 0
        mark_break = False

        game: dict[tuple[int,int], Tile] = {}

        while True:
            try:
                comp.execute_til_input()
            except ValueError:
                mark_break = True

            for k in range(len(comp.outputs) // 3):
                if comp.outputs[3*k + 2] == Tile.BALL:
                    ball = (comp.outputs[3*k], comp.outputs[3*k+1])
                elif comp.outputs[3*k + 2] == Tile.PADDLE:
                    paddle = (comp.outputs[3*k], comp.outputs[3*k+1])
                
                if comp.outputs[3*k] == -1 and comp.outputs[3*k+1] == 0:
                    score = comp.outputs[3*k + 2]
                else:
                    game[(comp.outputs[3*k], comp.outputs[3*k+1])] = Tile(comp.outputs[3*k+2])
            
            comp.outputs = []
            block_counter = len({t for t,v in game.items() if v == Tile.BLOCK})

            print(ball, paddle, score, block_counter)

            if mark_break:
                break

            if ball[0] < paddle[0]:
                comp.pending_input = Joy.L
            elif ball[0] > paddle[0]:
                comp.pending_input = Joy.R
            else:
                comp.pending_input = Joy.Z
            comp.execute_one_instruction()

        return score
        
        
