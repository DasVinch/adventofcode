from __future__ import annotations
import typing as typ

from tools import get_input
import tools

from skimage.morphology import label

import numpy as np

import os
from enum import IntEnum

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a',
]

SAMPLE2 = [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output',
]

import re

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Pulse:
    high: bool
    orig: str
    dest: str


class BaseNode:

    def __init__(self, name: str, verbose: bool = False) -> None:
        self.name = name
        self.verbose = verbose
        self.out = []

    def connect(self, b: BaseNode):
        self.out.append(b)
        b.recv_conn(self)

    def recv_conn(self, b: BaseNode):
        pass

    def __repr__(self) -> str:
        return f'BN {self.name} {[o.name for o in self.out]}'

    def pulse(self, p: Pulse) -> list[Pulse]:
        if self.verbose and not p.high:
            print(f'Node {self.name} recv {p}')
        return [Pulse(p.high, self.name, o.name) for o in self.out]


class FlipFlop(BaseNode):

    def __init__(self, name: str) -> None:
        super().__init__(name)

        self._state: bool = False

    def pulse(self, p: Pulse) -> list[Pulse]:
        if p.high:
            return []
        self._state = not self._state
        return [Pulse(self._state, self.name, o.name) for o in self.out]


class Conj(BaseNode):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._mems: dict[str, bool] = {}
        self.seen_low = False
        self.seen_high = False

    def recv_conn(self, b: BaseNode):
        self._mems[b.name] = False

    def pulse(self, p: Pulse):
        self._mems[p.orig] = p.high
        self.outval = not all(self._mems.values())
        self.seen_low |= not self.outval
        self.seen_high |= self.outval
        
        return [
            Pulse(self.outval, self.name, o.name)
            for o in self.out
        ]


def parse(l: list[str]) -> dict[str, BaseNode]:
    res: dict[str, BaseNode] = {'output': BaseNode('output')}
    connect_map: dict[str, list[str]] = {}
    for line in l:
        h, t = line.split(' -> ')
        outs = t.split(', ')
        if h[0] == '%':
            res[h[1:]] = FlipFlop(h[1:])
            connect_map[h[1:]] = outs
        elif h[0] == '&':
            res[h[1:]] = Conj(h[1:])
            connect_map[h[1:]] = outs
        else:
            res[h] = BaseNode(h)
            connect_map[h] = outs

    for name, outs in connect_map.items():
        for o in outs:
            if not o in res: # Make a sink point
                res[o] = BaseNode(o, verbose=o=='rx')
            
            res[name].connect(res[o])

    return res


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.lines = lines

        self.node_dict = parse(self.lines)

        self.debug = debug

    def solve1(self) -> int:
        h, l = 0, 0
        for _ in range(1000):
            a, b = self.button_push()
            h += a
            l += b

        return h * l

    def button_push(self) -> list[int]:

        pulse_queue: deque[Pulse] = deque()
        pulse_queue.appendleft(Pulse(False, 'button', 'broadcaster'))

        counts = [0, 0]

        cnt = 0

        while len(pulse_queue) > 0:
            cnt += 1
            p = pulse_queue.pop()
            counts[p.high] += 1
            #if self.debug:
            #    print(p)
            for np in self.node_dict[p.dest].pulse(p):
                pulse_queue.appendleft(np)

        return counts

    def solve2(self) -> int:
        # Locate all the NANDS
        nands = [node.name for node in self.node_dict.values() if isinstance(node, Conj)]
        fls = {n: [-1, -1, -1, -1] for n in nands}

        lvnode = self.node_dict['lv']

        for kk in range(10000):
            _ = self.button_push()

            for n in nands:
                node = self.node_dict[n]
                if fls[n][0] == -1 and node.seen_low:
                    fls[n][0] = kk
                    node.seen_low = False
                if fls[n][1] == -1 and fls[n][0] >= 0  and node.seen_low:
                    fls[n][1] = kk
                if fls[n][2] == -1 and node.seen_high:
                    fls[n][2] = kk
                    node.seen_high = False
                if fls[n][3] == -1 and fls[n][2] >= 0 and node.seen_high:
                    fls[n][3] = kk

        return fls


if __name__ == "__main__":

    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')
    t2 = Day(SAMPLE2, True)
    print(f'Test2 p1: {t2.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    r = Day(REAL)
    print(f'Real p2: {r.solve2()}')
