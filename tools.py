from typing import List, Dict
import numpy as np

def get_input(n: int, year:int = 2022) -> List[str]:
    fname = f"inputs/{year}/input{n}.txt"

    with open(fname, 'r') as f:
        l = f.readlines()
        l = [ll.rstrip() for ll in l]

    return l

def make_int_matrix(lines: List[str]) -> np.ndarray:
    return np.asarray([[int(c) for c in line] for line in lines])

def make_cmapped_int_matrix(lines: List[str], cmap: Dict[str, int]) -> np.ndarray:
    return np.asarray([[cmap[c] for c in line] for line in lines])