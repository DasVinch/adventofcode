from tools import get_input, make_int_matrix
import numpy as np

SMOL = [
    '11', '13'
]

SAMPLE = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]

MAX_INT = 2**31 - 1

class Day15:

    def __init__(self, lines) -> None:
        self.mat = make_int_matrix(lines)
        self.s0, self.s1 = self.mat.shape

    def solve(self) -> int:
        border = [(0,0,0)] # the start [x,y,dist]
        distanceDict = {(0,0): 0, (self.s0-1, self.s1-1): MAX_INT}

        while len(border) > 0:
            border.sort(key = lambda s: s[2])
            #print(border, distanceDict)
            elem = border.pop(0)
            neis = self.get_nei((elem[0], elem[1]))
            for n in neis:
                new_val =  elem[2] + self.mat[n[0], n[1]]
                if n in distanceDict:
                    old_val = distanceDict[n]
                    if new_val < old_val:
                        distanceDict[n] = min(new_val, distanceDict[n])
                        try:
                            k = border.index((n[0], n[1], old_val))
                            border[k] = (n[0], n[1], new_val)
                        except ValueError:
                            border.append((n[0], n[1], new_val))
                else:
                    distanceDict[n] = new_val
                    border.append((n[0], n[1], new_val))

        return distanceDict[(self.s0-1, self.s1-1)]

    def get_nei(self, abcoord):
        a, b = abcoord
        neis = []
        if a > 0:
            neis += [(a-1, b)]
        if b > 0:
            neis += [(a, b-1)]
        if a < self.s0 - 1:
            neis += [(a+1, b)]
        if b < self.s1 - 1:
            neis += [(a, b+1)]
        
        return neis

class Day15_2(Day15):
    def __init__(self, lines) -> None:

        mat = make_int_matrix(lines)

        matbig = np.concatenate([(mat - 1 + k) % 9 + 1 for k in range(5)], axis=0)
        self.mat = np.concatenate([(matbig - 1 + k) % 9 + 1 for k in range(5)], axis=1)
        self.s0, self.s1 = self.mat.shape

if __name__ == "__main__":
    test = Day15_2(SMOL)
    print(test.solve())
    test = Day15_2(SAMPLE)
    print(test.solve())
    real = Day15_2(get_input(15, 2021))
    print(real.solve())
