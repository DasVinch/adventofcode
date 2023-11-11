from tools import get_input

SAMPLE = [
    '1-3 a: abcde',
    '1-3 b: cdefg',
    '2-9 c: ccccccccc',
]

REAL = get_input(2, 2020)


class Day2:
    def __init__(self, lines) -> None:
        splits = [l.split() for l in lines]
        self.lows = [int(s[0].split('-')[0]) for s in splits]
        self.highs = [int(s[0].split('-')[1]) for s in splits]
        self.letter = [s[1][0] for s in splits]
        self.password = [s[2] for s in splits]

    def solve1(self):
        valid = 0
        for l, h, let, pw in zip(self.lows, self.highs, self.letter, self.password):
            k = pw.count(let)
            if k >= l and k <= h:
                valid += 1
        return valid

    def solve2(self):
        valid = 0
        for l, h, let, pw in zip(self.lows, self.highs, self.letter, self.password):
            if (pw[l-1] == let) ^ (pw[h-1] == let):
                valid += 1
        return valid

if __name__ == "__main__":
    t = Day2(SAMPLE)
    print(t.solve2())
    r = Day2(REAL)
    print(r.solve2())