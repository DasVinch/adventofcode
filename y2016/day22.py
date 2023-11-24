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

class NodeGrid:
    def __init__(self, all_nodes: list[Node]) -> None:
        self.maxx = max(*(n.x for n in all_nodes)) + 1
        self.maxy = max(*(n.y for n in all_nodes)) + 1
        nodes = all_nodes.copy()
        nodes.sort(key = lambda n: (n.x, n.y), reverse=True)
        
        self.grid: list[list[Node]] = [[nodes.pop() for _ in range(self.maxy)] for _ in range(self.maxx)]

    def __str__(self) -> str:
        s: list[str] = []
        for subg in self.grid:
            ss = ''
            for node in subg:
                s += f' {node.used:3d}/{node.size:3d}'
            s += [ss + '\n']
        return ''.join(s)




if __name__ == '__main__':
    all_nodes = [Node.from_line(line) for line in df_h]

    viable_pairs = 0
    for a in all_nodes:
        for b in all_nodes:
            if viable(a, b):
                viable_pairs += 1

    print(viable_pairs)

    ng = NodeGrid(all_nodes)


