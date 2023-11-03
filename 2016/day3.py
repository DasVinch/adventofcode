import typing as typ

from tools import get_input
import numpy as np

DATA = get_input(3, 2016)

parsed_ints = [list(map(int, l.strip().split())) for l in DATA]

part2 = True

if part2:
    n = len(parsed_ints)
    parsed_ints = np.asarray(parsed_ints)
    parsed_ints = np.moveaxis(parsed_ints.reshape(n//3,3,3),2,1).reshape(n,3)

count = 0
for l in parsed_ints:
    if sum(l) > 2*max(l):
        count += 1
print(count)