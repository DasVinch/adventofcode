from __future__ import annotations
import typing as typ

import os
import numpy as np

from tools import get_input, make_char_matrix

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = get_input(DAYDAY, 2023)

SAMPLE = [
    'jqt: rhn xhk nvd',
    'rsh: frs pzl lsr',
    'xhk: hfx',
    'cmg: qnr nvd lhk bvb',
    'rhn: xhk bvb hfx',
    'bvb: xhk hfx',
    'pzl: lsr hfx nvd',
    'qnr: nvd',
    'ntq: jqt hfx bvb xhk',
    'nvd: lhk',
    'lsr: lhk',
    'rzs: qnr cmg lsr rsh',
    'frs: qnr lhk lsr',
]

from dataclasses import dataclass

Coord: typ.TypeAlias = tuple[int, int]

@dataclass
class Node:
    x: float
    y: float
    dx: float
    dy: float

    def update(self):
        self.x += self.dx
        self.y += self.dy

class Day():

    def __init__(self, data: list[str]) -> None:
        self.data = data

        self.edges: dict[str, set[str]] = {}
        for line in data:
            head, tail = line.split(': ')
            tails = set(tail.split())
            if not head in self.edges:
                self.edges[head] = set()
            self.edges[head].update(tails)
            for t in tails:
                if not t in self.edges:
                    self.edges[t] = set()
                self.edges[t].add(head)

    def solve1(self) -> int:
        n_nodes = len(self.edges)
        self.node_order = list(self.edges.keys())
        self.node_index_lookup = {s: k for k,s in enumerate(self.node_order)}
        self.adj_matrix = np.zeros((n_nodes, n_nodes), np.int64)
        for k, node in enumerate(self.node_order):
            for neighbor in self.edges[node]:
                self.adj_matrix[k, self.node_index_lookup[neighbor]] = 1


    def _graphics_fun(self):
        self.node_dict = {node: Node(*np.random.randn(2), 0, 0) for node in self.edges.keys()}

    def _movegraph(self, G: float = 1e-4):
        all_nodes = [self.node_dict[name] for name in self.edges]

        rep_pot = lambda x: np.sign(x) * np.abs(1/x)**.5
        attr_pot = lambda x: np.sign(x) * np.abs(1/x + x)**.5

        for nodename in self.edges:
            nodeobj = self.node_dict[nodename]
            neighbs = [self.node_dict[othname] for othname in self.edges[nodename]]

            nodeobj.dx = G * sum([rep_pot(nodeobj.x - oth.x) for oth in neighbs])
            nodeobj.dy = G * sum([rep_pot(nodeobj.y - oth.y) for oth in neighbs])

            nodeobj.dx -= G * sum([attr_pot(nodeobj.x - oth.x) for oth in neighbs])
            nodeobj.dy -= G * sum([attr_pot(nodeobj.y - oth.y) for oth in neighbs])

        for nodeobj in self.node_dict.values():
            nodeobj.update()

    def _graph(self):
        import matplotlib.pyplot as plt; plt.ion()
        plt.cla()
        plt.scatter([n.x for n in self.node_dict.values()], 
                    [n.y for n in self.node_dict.values()])

        for nodename, nodeobj in self.node_dict.items():
            for neighbor_name in self.edges[nodename]:
                neighbor = self.node_dict[neighbor_name]
                plt.plot([nodeobj.x, neighbor.x], [nodeobj.y, neighbor.y], 'k-', lw=1)

        707, 786
        

def mpow(mat: np.ndarray, pow):
    if pow == 0:
        return np.eye(mat.shape[0])
    elif pow == 1:
        return mat
    elif pow % 2 == 0:
        _m = mpow(mat, pow // 2)
        return _m @ _m
    else:
        return mat @ mpow(mat, pow-1)
    

if __name__ == "__main__":
    t = Day(SAMPLE)

    print(f'Test p1: {t.solve1()}')
    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    from tqdm import trange
    import matplotlib.pyplot as plt; plt.ion()
    t._graphics_fun()
    r._graphics_fun()