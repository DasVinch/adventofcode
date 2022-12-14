from typing import List, Dict
import numpy as np

def get_input(n: int, year:int = 2022) -> List[str]:
    fname = f"inputs/{year}/input{n}.txt"

    with open(fname, 'r') as f:
        l = f.readlines()
        l = [ll.rstrip() for ll in l]

    return l

def make_int_matrix(lines: List[str], splitchar:str=None) -> np.ndarray:
    if splitchar is None:
        return np.asarray([[int(c) for c in line] for line in lines])
    else:
        return np.asarray([[int(c) for c in line.split(splitchar)] for line in lines])

def make_cmapped_int_matrix(lines: List[str], cmap: Dict[str, int]) -> np.ndarray:
    return np.asarray([[cmap[c] for c in line] for line in lines])

def make_char_matrix(lines: List[str]) -> np.ndarray:
    return np.asarray([[c for c in line] for line in lines])

def make_charint_matrix(lines: List[str]) -> np.ndarray:
    return np.asarray([[ord(c) for c in line] for line in lines])


from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class AbstractDijkstraer:
    def __init__(self, start, targets) -> None:
        self.border = PriorityQueue()
        self.border.put(PrioritizedItem(priority=0, item=start))

        self.targets = targets

        self.distanceDict = {start: 0}

        self.used = False

        # There must be no zero-score transitions!!
        # Otherwise we can hack it by making transitioning *into* the
        # final target cost 1 more, to sort the queue safely for equal values.

    def solveWithoutPath(self):
        if self.used:
            raise ValueError('AbstractDijkstraer has been used. Make a new one')
        self.used = True

        while not self.border.empty():
            wrappedelem = self.border.get()
            prio = wrappedelem.priority
            elem = wrappedelem.item


            if elem in self.targets:
                return prio

            for nei, cost in self.get_neighbors(elem):
                score = prio + cost
                is_new = nei not in self.distanceDict
                if is_new or score < self.distanceDict[nei]:
                    self.distanceDict[nei] = score
                    self.border.put(PrioritizedItem(priority=score, item=nei))

    def get_neighbors(self, elem):
        raise NotImplementedError('Abstract.')

    def solveWithPath(self):
        pass

def compare(l, r):
    #print(l, r)
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return 1
        elif l == r:
            return 0
        else:
            return -1

    elif isinstance(l, list) and isinstance(r, list):
        if l == [] and r == []:
            return 0
        elif l == [] and len(r) > 0:
            return 1
        elif len(l) > 0 and r == []:
            return -1
        else:
            x = compare(l[0], r[0])
            if x != 0:
                return x
            else:
                return compare(l[1:], r[1:])

    elif isinstance(l, list):
        return compare(l, [r])
    else:
        return compare([l], r)



def mergesort(comparator, l):

    def merge(comparator, l1, l2):
        if len(l1) == 0:
            return l2
        elif len(l2) == 0:
            return l1

        if comparator(l1[0], l2[0]) == 1:
            return [l1[0]] + merge(comparator, l1[1:], l2)
        else:
            return [l2[0]] + merge(comparator, l1, l2[1:])

    if len(l) <= 1:
        return l
    else:
        n = len(l) // 2
        return merge(comparator, mergesort(comparator, l[:n]), mergesort(comparator, l[n:]))
    