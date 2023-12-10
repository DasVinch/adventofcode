import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])
REAL = get_input(DAYDAY, 2023)


SAMPLE = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet',
]

SAMPLE2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen',
]

subsr = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

class Day:
    def __init__(self, lines: list[str]):
        self.lines = lines

    def solve1(self) -> int:
        total = 0
        for line in self.lines:
            digits = [int(k) for k in line if k.isnumeric()]
            assert len(digits) >= 1
            total += digits[0] * 10 + digits[-1]

        return total

    def solve2(self) -> int:
        # Let's bruteforce the hardcode :D
        total = 0
        for line in self.lines:
            digits: list[int] = []
            for k in range(len(line)):
                subline = line[k:]

                if subline[0].isnumeric():
                    digits += [int(subline[0])]
                    continue

                for diglet, val in subsr.items():
                    if subline.startswith(diglet):
                        digits += [val]

            assert len(digits) >= 1
            total += digits[0] * 10 + digits[-1]

            #print(line, digits)

        return total

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    t2 = Day(SAMPLE2)
    print(f'Test p2: {t2.solve2()}')

    print(f'Real p2: {r.solve2()}')