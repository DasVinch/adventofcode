from typing import List
from tools import get_input


def parse(lines: List[str]) -> List[List[int]]:
    elves_cals = []
    tmp = []
    for line in lines:
        if line == '':
            elves_cals += [tmp]
            tmp = []
        else:
            tmp += [int(line)]

    return elves_cals


def solve_1(dat):
    tots = [sum(l) for l in dat]
    return max(tots)

def solve_2(dat):
    tots = [sum(l) for l in dat]
    tots.sort(reverse=True)
    return sum(tots[:3])


if __name__ == "__main__":
    dat = parse(get_input(1))

    #print(solve_1(dat))
    print(solve_2(dat))
