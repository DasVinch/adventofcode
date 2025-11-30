from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = ['03036732577212944063491565474664']

ADDITIONAL_SAMPLES: list[list[str]] = [
    ['12345678'],
    ['80871224585914546619083218645595'],
    ['19617804207202209144916044189917'],
    ['69317163492948606335995924319873'],
]

T_DATA: typ.TypeAlias = list[int] # TODO

import numpy as np

def mpow(M: np.ndarray, n: int) -> np.ndarray:
    k = M.shape[0]
    if n == 0:
        return np.eye(k)
    elif n % 2 == 1:
        M2 = mpow(M, n // 2)
        return M @ M2 @ M2
    else:
        M2 = mpow(M, n // 2)
        return M2 @ M2

class PFacRational:
    def __init__(self, n: int) -> None:
        self.pfacs: dict[int, int] = {}

        p = n
        sqrt = (p+1) ** 0.5
        div = 2
        while p > 1 and div < sqrt:
            if p % div == 0:
                p //= div
                self.pfacs[div] = self.pfacs.get(div, 0) + 1
            else:
                div += 1 if div == 2 else 2

        if p > 1:
            self.pfacs[p] = 1

    def __repr__(self) -> str:
        return repr(self.pfacs)

    def __mul__(self, oth: PFacRational) -> PFacRational:
        product = PFacRational(1)

        product.pfacs = self.pfacs.copy()
        for p, c in oth.pfacs.items():
            product.pfacs[p] = product.pfacs.get(p, 0) + c

        return product

    def __truediv__(self, oth: PFacRational) -> PFacRational:
        quotient = PFacRational(1)

        quotient.pfacs = self.pfacs.copy()
        for p, c in oth.pfacs.items():
            quotient.pfacs[p] = quotient.pfacs.get(p, 0) - c
            if quotient.pfacs[p] == 0:
                del quotient.pfacs[p]

        return quotient

    def __mod__(self, mod: int) -> int:
        out = 1
        for k,v in self.pfacs.items():
            for vv in range(v):
                out = (out * k) % mod

        return out

class Day:
    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(x) for x in input[0]]
    
    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        size = len(self.data)

        matrix = np.zeros((size,size), np.int64)

        for ii in range(size):
            matrix[ii] = np.exp(
                +1j * np.pi / 2  * (0+(((np.arange(size) + 1) // (ii + 1)) % 4))
            ).imag


        if self.debug:
            #tl.print_matrix(matrix)
            ...

        v = np.asarray(self.data)
        v0 = v.copy()
        
        for k in range(100):
            v = np.abs(matrix @ v) % 10

        if self.debug:
            print('A: ' + ''.join(str(k) for k in v0))
            print('B: ' + ''.join(str(k) for k in v))

        return ''.join([str(k) for k in v[:8]])


    def solve2(self) -> int:

        # Compute just the post-diag tail of the one critical row.
        # Full size is 10_000 * original_length

        offset = 0
        for k in range(7):
            offset *= 10
            offset += self.data[k]

        full_size = 10_000 * len(self.data)
        post_pivot_size = full_size - offset

        if self.debug:
            print(offset, full_size, post_pivot_size)

        rat_factors: list[PFacRational] = [PFacRational(1)]
        last_rat_factor = PFacRational(1)
        
        rat_factors_10 = np.zeros(post_pivot_size, np.int64)
        rat_factors_10[0] = 1

        for k in range(1, post_pivot_size):
            num, denom = PFacRational(99 + k), PFacRational(k)
            
            last_rat_factor = last_rat_factor * num / denom
            rat_factors_10[k] = last_rat_factor % 10

        matrix = np.zeros((8, len(rat_factors_10)), np.int64)
        matrix[0] = rat_factors_10
        for k in range(1, 8):
            matrix[k, k:] = rat_factors_10[:-k]

        if self.debug:
            breakpoint()

        output = np.zeros(8, np.int64)
        size_remaining = post_pivot_size
        vec_data = np.asarray(self.data, np.int64)
        k = 0
        dlen = len(self.data)
        while size_remaining > dlen:
            if k == 0:
                output = (output + matrix[:, -dlen * (k+1):] @ vec_data) % 10
            else:
                output = (output + matrix[:, -dlen * (k+1):-dlen * k] @ vec_data) % 10
            k += 1
            size_remaining -= dlen
        if size_remaining > 0:
            output = (output + matrix[:, -dlen * k - size_remaining:-dlen * k] @ vec_data[-size_remaining:]) % 10


        return ''.join([str(k) for k in output])
