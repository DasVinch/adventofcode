from __future__ import annotations

from tools import get_input

df_h = get_input(22, 2016)[2:]

import re

node_re = re.compile('^/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T')

from dataclasses import dataclass

@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int

    @classmethod
    def from_line(cls, line: str) -> Node:
        return Node(*map(int, node_re.match(line).groups()))


def viable(a: Node, b: Node) -> bool:
    return a.used > 0 and a != b and a.used <= b.avail


if __name__ == '__main__':
    all_nodes = [Node.from_line(line) for line in df_h]

    viable_pairs = 0
    for a in all_nodes:
        for b in all_nodes:
            if viable(a, b):
                viable_pairs += 1

    print(viable_pairs)
