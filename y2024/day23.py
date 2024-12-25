from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    'kh-tc',
    'qp-kh',
    'de-cg',
    'ka-co',
    'yn-aq',
    'qp-ub',
    'cg-tb',
    'vc-aq',
    'tb-ka',
    'wh-tc',
    'yn-cg',
    'kh-ub',
    'ta-co',
    'de-co',
    'tc-td',
    'tb-wq',
    'wh-td',
    'ta-ka',
    'td-qp',
    'aq-cg',
    'wq-ub',
    'ub-vc',
    'de-ta',
    'wq-aq',
    'wq-vc',
    'wh-yn',
    'ka-de',
    'kh-ta',
    'co-tc',
    'wh-qp',
    'tb-vc',
    'td-yn',
]

def make_edge(a: str, b: str) -> tuple[str, str]:
    return (min(a,b), max(a,b))

def make_tri(a: str, b: str, c: str) -> tuple[str, str, str]:
    return tuple(sorted((a,b,c))) # type: ignore

class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.edgeset: set[tuple[str,str]] = set()
        self.nodeset: set[str] = set()

        for l in lines:
            a,b = l.split('-')
            self.edgeset.add(make_edge(a,b))
            self.nodeset.update({a,b})



    def solve1(self) -> int:
        # tuple(sorted())
        
        three_conns: set[tuple[str,str,str]] = set()
        
        for a,b in self.edgeset:
            for n in self.nodeset:
                if n == a or n == b:
                    continue
                if make_edge(a,n) in self.edgeset and make_edge(b,n) in self.edgeset:
                    three_conns.add(make_tri(a,b,n))
        
        count = 0
        for a,b,c in three_conns:
            if a.startswith('t') or b.startswith('t') or c.startswith('t'):
                count += 1

        return count
        

    def solve2(self) -> int:
        n = len(self.nodeset)

        greedy_subgraphs: list[set[str]] = []

        all_nodes = self.nodeset.copy()

        # This should find a "maximal" clique
        # But I'm not sure this works 100% to find the "maximum" clique
        # in pathological subcases.
        # I'm pretty sure it doesn't and I got lucky?
        while len(all_nodes) > 0:
            subgraph: set[str] = set()
            for n in all_nodes:
                if self.all_connected(n, subgraph):
                    subgraph.add(n)
            all_nodes.difference_update(subgraph)
            greedy_subgraphs.append(subgraph)
            pass

        self.greedy_subgraphs = greedy_subgraphs

        self.greedy_subgraphs.sort(key = lambda s: len(s), reverse=True)
        largest_clique = list(self.greedy_subgraphs[0])
        largest_clique.sort()

        return ','.join(largest_clique)

    def solve2_bk(self):
        # Bron-Kerbosch, no idea how it works.
        # From Wikipedia
        # ...


    def all_connected(self, node: str, subgraph: set[str]) -> bool:
        if len(subgraph) == 0:
            return True

        for n in subgraph:
            if not make_edge(n, node) in self.edgeset:
                return False
        
        return True


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)