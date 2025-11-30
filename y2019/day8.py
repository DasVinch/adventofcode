from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

import numpy as np

T_DATA: typ.TypeAlias = np.ndarray  # TODO


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return tl.make_int_matrix(input)

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug

    def solve1(self) -> int:
        tot_px = self.data.size

        layers = tot_px // (25 * 6)

        dat = self.data.reshape((layers, 6, 25))

        layer = np.argmin(np.sum(dat == 0, axis=(1, 2)))
        return np.sum(dat[layer] == 1) * np.sum(dat[layer] == 2)

    def solve2(self) -> int:
        tot_px = self.data.size

        layers = tot_px // (25 * 6)

        dat = self.data.reshape((layers, 6, 25))

        collapsed = dat[0].copy()

        for layer in range(1, dat.shape[0]):
            collapsed[collapsed == 2] = dat[layer][collapsed == 2]

        tl.print_bool_matrix(collapsed.astype(bool))

        return 0