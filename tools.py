from __future__ import annotations

import typing as typ

from typing import List, Dict
import numpy as np
import numpy.typing as npt


def get_input(n: int, year: int = 2022) -> List[str]:
    fname = f"inputs/{year}/input{n}.txt"

    with open(fname, 'r') as f:
        l = f.readlines()
        l = [ll.rstrip() for ll in l]

    return l


def make_int_matrix(lines: List[str],
                    splitchar: str | None = None) -> npt.NDArray:
    if splitchar is None:
        return np.asarray([[int(c) for c in line] for line in lines])
    else:
        return np.asarray([[int(c) for c in line.split(splitchar)]
                           for line in lines])


def make_cmapped_int_matrix(lines: List[str], cmap: Dict[str,
                                                         int]) -> npt.NDArray:
    return np.asarray([[cmap[c] for c in line] for line in lines])


def make_char_matrix(lines: List[str]) -> npt.NDArray:
    return np.asarray([[c for c in line] for line in lines])


def make_charint_matrix(lines: List[str]) -> npt.NDArray:
    return np.asarray([[ord(c) for c in line] for line in lines])


def print_bool_matrix(arr: npt.NDArray) -> None:
    for row1, row2 in zip(arr[::2], arr[1::2]):
        for v1, v2 in zip(row1, row2):
            print({
                (True, True): '▉',
                (True, False): '▀',
                (False, True): '▄',
                (False, False): ' ',
            }[(v1, v2)],
                  end='')
        print()
    if len(arr) % 2 == 1:
        for v in arr[-1]:
            print('▀' if v else ' ', end='')

    print()


def print_matrix(mat: npt.NDArray, fmt='%s'):
    m, n = mat.shape
    for i in range(m):
        for j in range(n):
            print(fmt % mat[i, j], end='')
        print()


from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

T = typ.TypeVar('T')


@dataclass(order=True)
class PrioritizedItem(typ.Generic[T]):
    priority: int
    item: T = field(compare=False)


class AbstractDijkstraer(typ.Generic[T]):

    def __init__(self,
                 start: T,
                 targets: typ.Set[T],
                 max_depth: int = -1) -> None:

        self.targets = targets

        self.border: PriorityQueue[PrioritizedItem[T]] = PriorityQueue()
        self.border.put(PrioritizedItem(priority=0, item=start))

        self.distanceDict: dict[T, tuple[int, T | None]] = {start: (0, None)}
        self.multiDistanceDict: dict[T, tuple[int, list[T]]] = {start: (0, [])}
        self.used = False

        self.max_depth = max_depth

        # There must be no zero-score transitions!!
        # Otherwise we can hack it by making transitioning *into* the
        # final target cost 1 more, to sort the queue safely for equal values.

    def solveWithoutPath(self) -> int | None:
        if self.used:
            raise ValueError(
                'AbstractDijkstraer has been used. Make a new one')
        self.used = True

        while not self.border.empty():
            wrappedelem = self.border.get()
            prio = wrappedelem.priority
            elem = wrappedelem.item

            #print(elem)

            if self.validate_target(elem):
                return prio

            self.intercept_elem(elem)

            for nei, cost in self.get_neighbors(elem):
                score = prio + cost
                is_new = nei not in self.distanceDict
                if (self.max_depth < 0 or score <= self.max_depth) and (
                        is_new or score < self.distanceDict[nei][0]):
                    self.distanceDict[nei] = (score, elem)
                    self.border.put(PrioritizedItem(priority=score, item=nei))

    def validate_target(self, elem: T) -> bool:
        return elem in self.targets

    def intercept_elem(self, elem: T) -> None:
        ...

    def get_neighbors(self, elem: T) -> typ.Set[typ.Tuple[T, int]]:
        raise NotImplementedError('Abstract.')

    def show_track(self, elem: T) -> list[T]:

        backtrack: list[T] = []
        our_elem = elem

        while our_elem is not None:
            backtrack.append(our_elem)
            our_elem = self.distanceDict[our_elem][1]

        return backtrack[::-1]

    def solveMultiEqualPath(self) -> int | None:
        if self.used:
            raise ValueError(
                'AbstractDijkstraer has been used. Make a new one')
        self.used = True

        while not self.border.empty():
            wrappedelem = self.border.get()
            prio = wrappedelem.priority
            elem = wrappedelem.item

            #print(elem)

            if self.validate_target(elem):
                return prio

            self.intercept_elem(elem)

            for nei, cost in self.get_neighbors(elem):
                score = prio + cost
                is_new = nei not in self.multiDistanceDict
                if is_new or score < self.multiDistanceDict[nei][0]:
                    self.multiDistanceDict[nei] = (score, [elem])
                    self.border.put(PrioritizedItem(priority=score, item=nei))
                # Add-on!
                elif score == self.multiDistanceDict[nei][0]:
                    score, elem0 = self.multiDistanceDict[nei]
                    self.multiDistanceDict[nei] = (score, elem0 + [elem])


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
        return merge(comparator, mergesort(comparator, l[:n]),
                     mergesort(comparator, l[n:]))
