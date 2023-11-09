from __future__ import annotations

import typing as typ

from tools import get_input

SAMPLES = [
    '^WNE$', # 3
    '^ENWWW(NEEE|SSE(EE|N))$', # 10
    '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', # 18
    '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', # 23
    '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', # 31
]

REAL = get_input(20, 2018)[0]


Node: typ.TypeAlias = typ.Tuple[int, int]
Graph: typ.TypeAlias = typ.Dict[Node, typ.Set[Node]]

# Basically, one first DFS path to construct the graph
# Then a second pass to resolve it.

def graphiphy(g: Graph, current_node: Node, regex: Regex) -> set[Node]:
    node = graphiphy_simple(g, current_node, regex.base)

    if len(regex.subexps) == 0:
        return {node}

    sub_endnodes: set[Node] = set()
    for subregex in regex.subexps:
        sub_endnodes.update(graphiphy(g, node, subregex))

    if regex.nextregex is None:
        return sub_endnodes
    
    final_endnodes: set[Node] = set()
    for end_node in sub_endnodes:
        final_endnodes.update(graphiphy(g, end_node, regex.nextregex))

    return final_endnodes

def graphiphy_simple(g: Graph, current_node: Node, simple_nesw: str) -> Node:
    cnode = current_node
    for c in simple_nesw:
        if c == 'N':
            ccnode = (cnode[0], cnode[1] + 1)
        elif c == 'E':
            ccnode = (cnode[0] + 1, cnode[1])
        elif c == 'S':
            ccnode = (cnode[0], cnode[1] - 1)
        elif c == 'W':
            ccnode = (cnode[0] - 1, cnode[1])
        else:
            raise AssertionError('Wut.')
        
        if not cnode in g:
            g[cnode] = set()
        if not ccnode in g:
            g[ccnode] = set()

        g[cnode].add(ccnode)
        g[ccnode].add(cnode)

        cnode = ccnode

    return cnode


from tools import AbstractDijkstraer

class ConcreteDijkstraer(AbstractDijkstraer):
    def __init__(self, graph: Graph, start, targets) -> None:
        super().__init__(start, targets)
        self.graph = graph

    def get_neighbors(self, elem: Node) -> typ.Iterable[tuple[Node, int]]:
        return {(el, 1) for el in self.graph[elem]} # DONT FORGET TO RETURN A COST


class Regex:

    NODES = 0

    def __init__(self) -> None:
        self.base: str = ''
        self.subexps: list[Regex] = []
        self.nextregex: Regex | None = None
        self.thisnode: int = Regex.NODES
        Regex.NODES += 1

    def __str__(self) -> str:
        s =  f'[{self.thisnode}]'
        s += f'{self.base}'
        if len(self.subexps) > 0:
            s += '('
            for sub in self.subexps[:-1]:
                s += sub.__str__()
                s += '|'
            s += self.subexps[-1].__str__()
            s += ')'
        if self.nextregex is not None:
            s += self.nextregex.__str__()
        return s

    def process(self, regex: str) -> str:
        #print(regex, '-------', self)
        k = 0
        while k < len(regex) and regex[k] in 'NWSE':
            k += 1
        self.base = regex[:k]

        if k == len(regex):
            return ''

        r = regex[k:]
        if r[0] in ')|':
            return r
        elif r[0] == '(':
            c = '|'
            while c == '|':
                self.subexps += [Regex()]
                r = self.subexps[-1].process(r[1:])
                c = r[0]
            assert r[0] == ')'
            r = r[1:] # pop the ')'

        if len(r) > 0:
            if r[0] in ')|':
                return r
            else:
                self.nextregex = Regex()
                return self.nextregex.process(r)

        else:
            return ''

    def countminimax(self) -> int:
        tot = len(self.base)
        if len(self.subexps):
            sublens = [sub.countminimax() for sub in self.subexps]
            if 0 not in sublens:
                tot += max(sublens)
        if self.nextregex is not None:
            tot += self.nextregex.countminimax()

        return tot

    def countbydistance(self) -> dict[int, int]:
        distcount = {}
        for c in range(len(self.base)):
            distcount[c+1] = 1
        k = len(distcount)

        subdists = [sub.countbydistance() for sub in self.subexps]
        sublens = [sub.countminimax() for sub in self.subexps]

        if 0 not in sublens:
            for s in subdists:
                for kk in s:
                    distcount[k + kk] = distcount.get(k+kk, 0) + s[kk]
        else:
            for s in subdists:
                if len(s) > 0:
                    mm = max(s)
                    for kk in range(1, mm//2 + 1):
                        distcount[k + kk] = distcount.get(k+kk, 0) + s[kk]

        if self.nextregex is not None:
            if not 0 in sublens:
                print(f'Assumption fails: {sublens} {[s.base for s in self.subexps]}')
                print(f'    Followed by {self.nextregex.base}')
                #import pdb; pdb.set_trace()
            sback = self.nextregex.countbydistance()
            for kk in sback:
                distcount[k + kk] = distcount.get(k+kk, 0) + sback[kk]

        return distcount




if __name__ == "__main__":
    for k in range(5):
        t = Regex()
        t.process(SAMPLES[k][1:-1])
        print(t)
        #print(t.countminimax())
        #print(t.countbydistance())
        gt = {}
        graphiphy(gt, (0,0), t)

        djk = ConcreteDijkstraer(gt, (0,0), set())
        djk.solveWithoutPath()
        print(max(djk.distanceDict.values()))



    r = Regex()
    r.process(REAL[1:-1])

    gr = {}
    graphiphy(gr, (0,0), r)

    djk = ConcreteDijkstraer(gr, (0,0), set())
    djk.solveWithoutPath()
    print(max(djk.distanceDict.values()))
    # Part 2
    print(len([k for k in djk.distanceDict.values() if k >= 1000]))


# GRAPHIPHY A REGEX
# graphiphy the mainline
# graphiphy all of the parenthesized branches AND RETURN ALL THE TAIL NODES.
# process the tail FROM EACH OF THE SET OF THE TAIL NODES.
