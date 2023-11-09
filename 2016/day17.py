from __future__ import annotations

import typing as typ

import hashlib

from tools import AbstractDijkstraer

Node: typ.TypeAlias = typ.Tuple[str, complex]

TESTKEYS = [
    'hijkl',
    'ihgpwlah',
    'kglvqrro',
    'ulqzkmiv',
]

REALKEY = 'pxxbnzuo'


class NodeDijkstraer(AbstractDijkstraer[Node]):

    def __init__(self, key: str, start: Node, targets: typ.Set[Node]) -> None:
        self.key = key
        super().__init__(start, targets)

        self.targets_coords: set[complex] = {t[1] for t in targets}

    def validate_target(self, elem: Node) -> bool:
        return elem[1] in self.targets_coords

    def get_neighbors(self, elem: Node) -> typ.Iterable[tuple[Node, int]]:
        path, pos = elem
        hashhead = hashlib.md5(
            (self.key + path).encode('ascii')).hexdigest()[:4]
        
        # Special pruning rule - if you hit the target, no more neighbors.
        if elem[1] == 3-3j:
            return set()

        neighbors: set[Node] = set()
        if hashhead[0] >= 'b' and pos.imag < 0:  # up
            neighbors.add((path + 'U', pos + 1j))
        if hashhead[1] >= 'b' and pos.imag > -3:  # down
            neighbors.add((path + 'D', pos - 1j))
        if hashhead[2] >= 'b' and pos.real > 0:  # up
            neighbors.add((path + 'L', pos - 1))
        if hashhead[3] >= 'b' and pos.real < 3:  # up
            neighbors.add((path + 'R', pos + 1))

        return {(el, 1) for el in neighbors}  # DONT FORGET TO RETURN A COST


if __name__ == '__main__':
    # Part 1
    for testkey in TESTKEYS + [REALKEY]:
        djk = NodeDijkstraer(testkey, ('', 0), {('', 3-3j)})
        djk.solveWithoutPath()
        f = [t for t in djk.distanceDict if t[1] == 3-3j]
        if len(f) > 0:
            print(testkey, ' ', end='')
            print(f[0][0])

    # Part 2 - run dijkstra to exhaustion with no target
    for testkey in TESTKEYS + [REALKEY]:
        djk = NodeDijkstraer(testkey, ('', 0), set())
        djk.solveWithoutPath()
        f = [t for t in djk.distanceDict if t[1] == 3-3j]
        if len(f) > 0:
            print(testkey, ' ', end='')
            print(max(map(lambda t: len(t[0]), f)))