from functools import lru_cache

SAMPLE = [4, 8]
REAL = [10, 6]


class Die:

    def __init__(self):
        self.k = 99
        self.rolls = 0

    def roll(self):
        self.k = (self.k + 1) % 100
        self.rolls += 1
        return self.k + 1


def game(start_a, start_b):
    d = Die()
    pos_a, pos_b = start_a, start_b
    score_a, score_b = 0, 0

    while True:
        die_a = d.roll() + d.roll() + d.roll()
        pos_a = (pos_a + die_a - 1) % 10 + 1
        score_a += pos_a
        if score_a >= 1000:
            return d.rolls * score_b

        die_b = d.roll() + d.roll() + d.roll()
        pos_b = (pos_b + die_b - 1) % 10 + 1
        score_b += pos_b
        if score_b >= 1000:
            return d.rolls * score_a



@lru_cache(maxsize=None)
def diraccer(start_a, start_b, score_a, score_b, a_plays):

    print(start_a, start_b, score_a, score_b, a_plays)
    #input()
    if score_a >= 21:
        if not a_plays:
            return 1, 0
        else:
            1/0
    if score_b >= 21:
        if a_plays:
            return 0, 1
        else:
            1/0


    a_wins, b_wins = 0, 0
    rolls = [3, 4, 5, 6, 7, 8, 9]
    weight_rolls = [1, 3, 6, 7, 6, 3, 1]
    for d in range(7):
        die = rolls[d]
        wr = weight_rolls[d]
        if a_plays:  # A_plays
            pos_a = (start_a + die - 1) % 10 + 1
            aa, bb = diraccer(pos_a, start_b, score_a + pos_a, score_b, False)
            a_wins += wr * aa
            b_wins += wr * bb

        else:  # B plays
            pos_b = (start_b + die - 1) % 10 + 1
            aa, bb = diraccer(start_a, pos_b, score_a, score_b + pos_b, True)
            a_wins += wr * aa
            b_wins += wr * bb

    return a_wins, b_wins


if __name__ == "__main__":

    print(game(*SAMPLE))
    print(max(diraccer(*REAL, 0, 0, True)))
