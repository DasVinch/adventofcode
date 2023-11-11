from typing import List, Tuple
from tools import get_input

THEIR_RPS = {'A': 0, 'B': 1, 'C': 2}
MY_RPS = {'X': 0, 'Y': 1, 'Z': 2}

def parse(lines: List[str]) -> List[Tuple[int, int]]:
    lsplit = [l.split() for l in lines]
    data = [(THEIR_RPS[d[0]], MY_RPS[d[1]]) for d in lsplit]
    return data


def solve_1(dat: List[Tuple[int, int]]) -> int:
    tot = 0
    for game in  dat:
        tot += game[1] + 1 + ((game[1] - game[0] + 1) % 3) * 3
    return tot

def solve_2(dat: List[Tuple[int, int]]) -> int:
    tot = 0
    for game in  dat:
        tot += 3 * game[1]
        tot += (game[0] + game[1] - 1) % 3 + 1
    return tot


if __name__ == "__main__":
    dat = parse(get_input(2))

    #print(solve_1(parse(['A Y', 'B X', 'C Z'])))
    #print(solve_1(dat))
    print(solve_2(parse(['A Y', 'B X', 'C Z'])))
    print(solve_2(dat))