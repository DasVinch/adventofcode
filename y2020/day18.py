import os
from tools import get_input
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

S = ['(1 * 1 + 1) + 1',]

SAMPLE = [
    '1 + 2 * 3 + 4 * 5 + 6',
    '1 + (2 * 3) + (4 * (5 + 6))',
    '2 * 3 + (4 * 5)',
    '5 + (8 * 3 + 9 + 3 * 4 * 3)',
    '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
    '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
]

REAL = get_input(DAYDAY, 2020)

class Literal(int):
    def eval(self):
        return self

class AddExpression:
    def __init__(self, lexpr, rexpr) -> None:
        self.rexpr = rexpr
        self.lexpr = lexpr

    def __str__(self) -> str:
        return fr'<a{self.lexpr} + {self.rexpr}\a>'

    def eval(self):
        return self.lexpr.eval() + self.rexpr.eval()

class MulExpression:
    def __init__(self, lexpr, rexpr) -> None:
        self.lexpr = lexpr
        self.rexpr = rexpr

    def __str__(self) -> str:
        return f'<m{self.lexpr} x {self.rexpr}\m>'


    def eval(self):
        return self.lexpr.eval() * self.rexpr.eval()


def expression_parse(tokens, pending=None, p2=False):
    # print(tokens)
    # print(pending)
    # import pdb; pdb.set_trace()

    if len(tokens) == 0 and pending is not None:
        return pending
    if re.match('\d+', tokens[-1]) and pending is None:
        return expression_parse(tokens[:-1], Literal(tokens[-1]), p2=p2)
    
    
    if tokens[-1] == '+' and pending is not None:
        if not p2:
            return AddExpression(expression_parse(tokens[:-1], p2=p2), pending)
        else:
            l, r = extract_rightmost(tokens[:-1], p2=p2)
            return expression_parse(l, AddExpression(r, pending), p2=p2)


    if tokens[-1] == '*' and pending is not None:
        # This doesn't quite work yet cause we need to check for a
        # precedenting AddExpr to the left of the *
        return MulExpression(expression_parse(tokens[:-1], p2=p2), pending)
    if tokens[-1] == ')' and pending is None:
            parcounter = 1
            for k, t in enumerate(tokens[-2::-1]):
                if t == ')':
                    parcounter += 1
                elif t == '(':
                    parcounter -= 1

                if parcounter == 0:
                    return expression_parse(tokens[:-2-k], pending=expression_parse(tokens[-2-k+1:-1], p2=p2), p2=p2)

    raise AssertionError("Doesn't work bruh")

def extract_rightmost(tokens, p2 :bool):
    if re.match('\d+', tokens[-1]):
        return tokens[:-1], Literal(tokens[-1])

    if tokens[-1] == ')':
            parcounter = 1
            for k, t in enumerate(tokens[-2::-1]):
                if t == ')':
                    parcounter += 1
                elif t == '(':
                    parcounter -= 1

                if parcounter == 0:
                    return tokens[:-2-k], expression_parse(tokens[-2-k+1:-1], p2=p2)

    raise AssertionError("Doesn't work bruh")





class Day:
    def __init__(self, lines) -> None:
        self.exprs = []
        self.exprs2 = []
        self.tokens = []
        for line in lines:
            l = line.replace('(', '( ')
            l = l.replace(')', ' )')
            tokens = l.split()
            self.exprs += [expression_parse(tokens)]
            self.exprs2 += [expression_parse(tokens, p2=True)]
            self.tokens += [tokens]


    def solve1(self):
        return sum([e.eval() for e in self.exprs])

    def solve2(self):
        return sum([e.eval() for e in self.exprs2])

if __name__ == "__main__":
    ts = Day(S)
    t = Day(SAMPLE)
    print(t.solve1())
    r = Day(REAL)
    print(r.solve1())

    print(t.solve2())
    print(r.solve2())