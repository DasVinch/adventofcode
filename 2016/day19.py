ELFCOUNT = 5
ELFCOUNT2 = 3005290

import typing as typ

from collections import deque
from tqdm import tqdm, trange

class DoubleDeque:
    '''
    A near-deque that is actually two balanced deques, so
    as to keep a live pointer smack in the middle.
    '''
    pass
class SqrtList:
    def __init__(self, iter: typ.Iterator[int], length: int):
        n = round(length**.5)

        self.sqrtn = n
        self.len = 0

        self.outer_arr: list[list[int]] = []
        inner: list[int] = []

        while True:
            try:
                x = next(iter)
            except StopIteration:
                if len(inner) > 0:
                    self.outer_arr.append(inner)
                inner = []
                break

            inner.append(x)
            self.len += 1

            if len(inner) == n:
                self.outer_arr.append(inner)
                inner = []

    def _recompute_sqrtn(self) -> None:
        self.sqrtn = round(self.len**.5)

    def popleft(self) -> int:
        el = self.outer_arr[0].pop(0)
        if len(self.outer_arr[0]) == 0:
            self.outer_arr.pop(0)
            print(f'Reducing outer to len({len(self.outer_arr)}) | {len(self)} | {self.sqrtn}')
        self.len -= 1
        self._recompute_sqrtn()
        return el
    
    def pop(self) -> int:
        el = self.outer_arr[-1].pop(-1)
        if len(self.outer_arr[-1]) == 0:
            self.outer_arr.pop()
            print(f'Reducing outer to len({len(self.outer_arr)}) | {len(self)} | {len(self)} | {self.sqrtn}')
        self.len -= 1
        self._recompute_sqrtn()
        return el
    
    def append(self, val: int) -> None:
        llast = self.outer_arr[-1]
        if len(llast) >= self.sqrtn:
            self.outer_arr += [[val]]
        else:
            llast += [val]
        self.len += 1
        self._recompute_sqrtn()

    def __len__(self):
        return self.len

    def pop_by_index(self, idx: int) -> int:
        c = 0
        k = 0
        while c <= idx:
            c += len(self.outer_arr[k])
            k += 1
        
        el = self.outer_arr[k-1].pop(idx - c)
        if len(self.outer_arr[k-1]) == 0:
            self.outer_arr.pop(k-1)
            print(f'Reducing outer to len({len(self.outer_arr)}) | {len(self)}  | {len(self)} | {self.sqrtn}')
        self._recompute_sqrtn()
        self.len -= 1

        return el


        

            


if __name__ == "__main__":

    elves = deque()
    for t in trange(ELFCOUNT2):
        elves.append(t)

    while len(elves) > 1:
        elves.append(elves.popleft())
        del elves[0]

    print(elves)
    print(elves.pop() + 1)

    from time import time

    s = time()

    elves = SqrtList(iter(range(ELFCOUNT2)), ELFCOUNT2)

    while len(elves) > 1:
        elves.append(elves.popleft())
        elves.pop_by_index(len(elves) // 2 - 1)

    print(elves)
    print(elves.pop() + 1)

    print(time() - s)
