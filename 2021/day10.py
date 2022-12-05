from tools import get_input
import numpy as np

SAMPLE = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]

MATCH = {'(': ')', '{': '}', '[': ']', '<': '>'}
SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORE2 = {'(': 1, '[': 2, '{': 3, '<': 4}
OPENERS = '([{<'

class Day10:

    def __init__(self, lines) -> None:
        self.lines = lines

    def solve(self) -> int:
        score = 0
        score2 = []
        for line in self.lines:
            err = False
            acc = []
            for c in line:
                if c in OPENERS:
                    acc.append(c)
                else:
                    if len(acc) == 0:
                        score += SCORE[c]
                        err = True
                        break
                    else:
                        cc = acc.pop(-1)
                        if c != MATCH[cc]:
                            score += SCORE[c]
                            err = True
                            break
            if not err and len(acc) > 0:
                sc = 0
                bcount = 0
                for cc in acc[::-1]:
                    if cc in OPENERS:
                        if bcount == 0:
                            sc *= 5
                            sc += SCORE2[cc]
                        else:
                            bcount -= 1
                    else:
                        bcount += 1

                score2 += [sc]
        
        score2.sort()
        score22 = score2[(len(score2) - 1) // 2]

        return score, score22


if __name__ == "__main__":
    test = Day10(SAMPLE)
    print(test.solve())
    real = Day10(get_input(10, 2021))
    print(real.solve())