from tools import get_input

SAMPLE = [
    '2-4,6-8',
    '2-3,4-5',
    '5-7,7-9',
    '2-8,3-7',
    '6-6,4-6',
    '2-6,4-8',
]


class Day4:

    def __init__(self, inputlines):
        # parse pairs
        ranges = [l.split(',') for l in inputlines]
        edgeschar = [r0.split('-') + r1.split('-') for r0, r1 in ranges]
        self.edgesint = [[int(c) for c in r] for r in edgeschar]

    def solve1(self) -> int:
        tot = 0
        for pair in self.edgesint:
            if ((pair[0] <= pair[2] and pair[1] >= pair[3])
                    or (pair[0] >= pair[2] and pair[1] <= pair[3])):
                tot += 1
        return tot

    def solve2(self) -> int:
        tot = 0
        for pair in self.edgesint:
            if ((pair[2] >= pair[0] and pair[2] <= pair[1])
                    or (pair[3] >= pair[0] and pair[3] <= pair[1])
                    or (pair[0] >= pair[2] and pair[1] <= pair[3])
                    or (pair[0] >= pair[2] and pair[1] <= pair[3])):
                tot += 1
        return tot


if __name__ == "__main__":
    test = Day4(SAMPLE)
    #print(test.solve1())
    print(test.solve2())
    real = Day4(get_input(4))
    #print(real.solve1())
    print(real.solve2())
