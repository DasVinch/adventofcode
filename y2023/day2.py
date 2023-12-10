import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])
REAL = get_input(DAYDAY, 2023)


SAMPLE = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]

from dataclasses import dataclass

@dataclass
class Draw:
    val: int
    col: str

@dataclass
class Game:
    id: int
    draws: list[list[Draw]]

def parse_draw(draw_line: str) -> Draw:
    val_s, color = draw_line.strip().split()
    return Draw(int(val_s), color)

def parse_game(game_line: str) -> Game:
    head, draws = game_line.split(': ')
    return Game(id = int(head.split()[-1]),
                draws = [[parse_draw(sd) for sd in d.split(',')] for d in draws.split(';')])

CAN_DO = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def can_set(set: list[Draw], can_do: dict[str, int]):
    for draw in set:
        if draw.val > can_do.get(draw.col, 0):
            return False
        
    return True

def game_minimum_set_power(game: Game) -> int:
    min_needed: dict[str, int] = {}
    for set in game.draws:
        for draw in set:
            if draw.val > min_needed.get(draw.col, 0):
                min_needed[draw.col] = draw.val

    power = 1
    for t in min_needed.values():
        power *= t

    return power

        

class Day:
    def __init__(self, lines: list[str]):
        self.games = [parse_game(line) for line in lines]

    def solve1(self, can_do: dict[str, int] = CAN_DO) -> int:
        sum_ids = 0
        for game in self.games:
            can = all([can_set(set, can_do) for set in game.draws])
            
            if can:
                sum_ids += game.id

        return sum_ids

    def solve2(self) -> int:
        return sum([game_minimum_set_power(g) for g in self.games])

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')
    print(f'Real p2: {r.solve2()}')