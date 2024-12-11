from __future__ import annotations

import os
import tools as tl

import typing as typ

import numpy as np, numpy.typing as npt

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.make_char_matrix(tl.get_input(DAYDAY, 2024))

SAMPLE = tl.make_char_matrix([
    '....#.....',
    '.........#',
    '..........',
    '..#.......',
    '.......#..',
    '..........',
    '.#..^.....',
    '........#.',
    '#.........',
    '......#...',
])

import numba

import ctypes
DLL = ctypes.CDLL('./y2024/libday6.so')
DLL.c_bitmask_solve.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_int, ctypes.c_int)
DLL.c_bitmask_solve.restype = ctypes.c_int



@numba.jit
def numbad_mask_solve1(guard: tuple[int, int], mat, detect_cycle: bool = False) -> int:
        
        ii, jj = guard
        matwork = np.zeros_like(mat, np.uint8)
        matwork[ii,jj] = 0x10 | 0b0001

        m, n = mat.shape

        while ii >= 0 and jj >= 0 and ii < m and jj < n:
            c: int = matwork[ii, jj]
            cl = (c & 0xf0) >> 4
            match cl:
                case 0x1: # '^': # 0x1 0b0001
                    if ii > 0 and mat[ii-1, jj] == '#':
                        if detect_cycle and c & 0b0010:
                            return -1
                        matwork[ii,jj] = 0x20 | 0b0010 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0001
                        if ii > 0:
                            matwork[ii-1, jj] = 0x10 | 0b0001 | (matwork[ii-1, jj] & 0x0f)
                        ii -= 1
                case 0x2: # '>': # 0x2 0b0010
                    if jj < n-1 and mat[ii, jj+1] == '#':
                        if detect_cycle and c & 0b0100:
                            return -1
                        matwork[ii,jj] = 0x30 | 0b0100 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0010
                        if jj < n-1:
                            matwork[ii, jj+1] = 0x20 | 0b0010 | (matwork[ii, jj+1] & 0x0f)
                        jj += 1
                case 0x3: # 'v': # 0x3 0b0100
                    if ii < m-1 and mat[ii+1, jj] == '#':
                        if detect_cycle and (c & 0b1000):
                            return -1
                        matwork[ii,jj] = 0x40 | 0b1000 | (c & 0x0f)
                    else:
                        #print(f'else? {ii=} {jj=}')
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0100
                        if ii < m-1:
                            matwork[ii+1, jj] = 0x30 | 0b0100 | (matwork[ii+1, jj] & 0x0f)
                        ii += 1
                case 0x4: # '<': # 0x4 0b1000
                    if jj > 0 and mat[ii, jj-1] == '#':
                        if detect_cycle and c & 0b0001:
                            return -1
                        matwork[ii,jj] = 0x10 | 0b0001 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b1000
                        if jj > 0:
                            matwork[ii, jj-1] = 0x40 | 0b1000 | (matwork[ii, jj-1] & 0x0f)
                        jj -= 1

        return len(np.where(matwork > 0)[0])


class Day:

    def __init__(self, mat: npt.NDArray[np._CharType], debug: bool = False) -> None:
        self.debug = debug

        self.mat = mat

        a,b = np.where(self.mat == '^')
        self.guard = (a[0],b[0])


    def solve1(self) -> int:
        ii, jj = self.guard
        matwork = self.mat.copy()

        m, n = self.mat.shape

        while ii >= 0 and jj >= 0 and ii < m and jj < n:
            c = matwork[ii, jj]
            match c:
                case '^':
                    if ii > 0 and matwork[ii-1, jj] == '#':
                        matwork[ii,jj] = '>'
                    else:
                        matwork[ii,jj] = 'X'
                        if ii > 0:
                            matwork[ii-1, jj] = '^'
                        ii -= 1
                case '>':
                    if jj < n-1 and matwork[ii, jj+1] == '#':
                        matwork[ii,jj] = 'v'
                    else:
                        matwork[ii,jj] = 'X'
                        if jj < n-1:
                            matwork[ii, jj+1] = '>'
                        jj += 1
                case 'v':
                    if ii < m-1 and matwork[ii+1, jj] == '#':
                        matwork[ii,jj] = '<'
                    else:
                        #print(f'else? {ii=} {jj=}')
                        matwork[ii,jj] = 'X'
                        if ii < m-1:
                            matwork[ii+1, jj] = 'v'
                        ii += 1
                case '<':
                    if jj > 0 and matwork[ii, jj-1] == '#':
                        matwork[ii,jj] = '^'
                    else:
                        matwork[ii,jj] = 'X'
                        if jj > 0:
                            matwork[ii, jj-1] = '<'
                        jj -= 1
            if self.debug:
                tl.print_matrix(matwork)
                input(f'{ii=} {jj=} {c=}')

        return len(np.where(matwork == 'X')[0])
            

    def mask_solve1(self, detect_cycle: bool = False) -> int:
        
        ii, jj = self.guard
        matwork = np.zeros_like(self.mat, np.uint8)
        matwork[ii,jj] = 0x10 | 0b0001

        m, n = self.mat.shape

        if self.debug:
            c: int = matwork[ii, jj] # type: ignore
            tl.print_matrix(t.mat_p1, '%-2s ')
            input(f'{ii=} {jj=} {c=}')

        while ii >= 0 and jj >= 0 and ii < m and jj < n:
            c: int = matwork[ii, jj] # type: ignore
            cl = (c & 0xf0) >> 4
            match cl:
                case 0x1: # '^': # 0x1 0b0001
                    if ii > 0 and self.mat[ii-1, jj] == '#':
                        if detect_cycle and c & 0b0010:
                            return -1
                        matwork[ii,jj] = 0x20 | 0b0010 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0001
                        if ii > 0:
                            matwork[ii-1, jj] = 0x10 | 0b001 | (matwork[ii-1, jj] & 0x0f)
                        ii -= 1
                case 0x2: # '>': # 0x2 0b0010
                    if jj < n-1 and self.mat[ii, jj+1] == '#':
                        if detect_cycle and c & 0b0100:
                            return -1
                        matwork[ii,jj] = 0x30 | 0b0100 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0010
                        if jj < n-1:
                            matwork[ii, jj+1] = 0x20 | 0b0010 | (matwork[ii, jj+1] & 0x0f)
                        jj += 1
                case 0x3: # 'v': # 0x3 0b0100
                    if ii < m-1 and self.mat[ii+1, jj] == '#':
                        if detect_cycle and (c & 0b1000):
                            return -1
                        matwork[ii,jj] = 0x40 | 0b1000 | (c & 0x0f)
                    else:
                        #print(f'else? {ii=} {jj=}')
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b0100
                        if ii < m-1:
                            matwork[ii+1, jj] = 0x30 | 0b0100 | (matwork[ii+1, jj] & 0x0f)
                        ii += 1
                case 0x4: # '<': # 0x4 0b1000
                    if jj > 0 and self.mat[ii, jj-1] == '#':
                        if detect_cycle and c & 0b0001:
                            return -1
                        matwork[ii,jj] = 0x10 | 0b0001 | (c & 0x0f)
                    else:
                        matwork[ii,jj] &= 0x0f
                        matwork[ii,jj] |= 0b1000
                        if jj > 0:
                            matwork[ii, jj-1] = 0x40 | 0b1000 | (matwork[ii, jj-1] & 0x0f)
                        jj -= 1

            self.mat_p1 = matwork.copy()
            if self.debug:
                tl.print_matrix(self.mat_p1, '%-2s ')
                input(f'{ii=} {jj=} {c=}')


        return len(np.where(matwork > 0)[0])


    def solve2(self) -> int:
        self.mask_solve1()

        self.trace = list(zip(*np.where(self.mat_p1 > 0)))

        cyclers = 0

        for ii, jj in self.trace:
            matbak = self.mat[ii, jj]
            #print(ii,jj)
            self.mat[ii, jj] = '#'
            if numbad_mask_solve1(self.guard, self.mat, detect_cycle=True) < 0:
                cyclers += 1
                if self.debug:
                    print(f'cycle_inducer: {ii=} {jj=}')
            self.mat[ii, jj] = matbak

        return cyclers

    def cmask_solve1(self) -> int:
        uint8_mat = np.zeros_like(self.mat, dtype=np.uint8)
        uint8_mat[self.mat == '#'] = 1
        mat_ptr = uint8_mat.ctypes.data_as(ctypes.POINTER(ctypes.c_char))

        m, n = self.mat.shape
        return DLL.c_bitmask_solve(self.guard[0], self.guard[1], mat_ptr, m, n)

    def solve2c(self) -> int:
        self.mask_solve1()
        
        uint8_mat = np.zeros_like(self.mat, dtype=np.uint8)
        uint8_mat[self.mat == '#'] = 1
        mat_ptr = uint8_mat.ctypes.data_as(ctypes.POINTER(ctypes.c_char))
        m, n = self.mat.shape

        self.trace = list(zip(*np.where(self.mat_p1 > 0)))

        cyclers = 0

        for ii, jj in self.trace:
            matbak = uint8_mat[ii, jj]
            #print(ii,jj)
            uint8_mat[ii, jj] = 1
            if DLL.c_bitmask_solve(self.guard[0], self.guard[1], mat_ptr, m, n) < 0:
                cyclers += 1
            uint8_mat[ii, jj] = matbak

        return cyclers






if __name__ == "__main__":
    t = Day(SAMPLE, False)
    print(f'Test p1: {t.solve1()}')
    print(f'Test p1_2: {t.mask_solve1()}')
    print(f'Test p1_3: {t.cmask_solve1()}')


    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')
    print(f'Real p1_2: {r.mask_solve1()}')
    print(f'Real p1_3: {r.cmask_solve1()}')

    
    print(f'Test p2: {t.solve2()}')
    #t.debug = True
    print(f'Test p2: {t.solve2()}')
    input('Input...')

    import time
    s = time.time()
    print(f'Real p2 (numba): {r.solve2()}')
    print(time.time() - s)
    
    print(f'Test p2 (C): {t.solve2c()}')
    s = time.time()
    print(f'Real p2 (C): {r.solve2c()}')
    print(time.time() - s)