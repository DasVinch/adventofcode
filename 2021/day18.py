from tools import get_input
import ast

REALDEAL = get_input(18, 2021)

INT = 1234
PAIR = 4321

PASS_TO_PREVIOUS = 7987
PASS_TO_NEXT = 1234124


class Pair:

    def __init__(self, pairlist, parent, depth):
        self.parent = parent
        if depth > 4:
            import pdb; pdb.set_trace()
        self.depth = depth

        if isinstance(pairlist[0], int):
            self.lt = INT
            self.l = pairlist[0]
        else:
            self.lt = PAIR
            self.l = Pair(pairlist[0], self, depth + 1)
        if isinstance(pairlist[1], int):
            self.rt = INT
            self.r = pairlist[1]
        else:
            self.rt = PAIR
            self.r = Pair(pairlist[1], self, depth + 1)

    def add(self, other: "Pair"):
        newp = Pair([self.tonestlist(), other.tonestlist()], None, 0)
        something = True
        while something:
            something = False
            _, ex2 = newp.explode()
            while ex2 is not None:
                something = True
                _, ex2 = newp.explode()

            if newp.split():
                something = True

        return newp

    def tonestlist(self):
        if self.lt == INT:
            left = self.l
        else:
            left = self.l.tonestlist()
        if self.rt == INT:
            right = self.r
        else:
            right = self.r.tonestlist()

        return [left, right]

    def split(self) -> bool:
        if self.lt == INT and self.l >= 10:
            self.l = Pair([self.l // 2, (self.l + 1) // 2], self,
                          self.depth + 1)
            self.lt = PAIR
            return True
        if self.lt == PAIR and self.l.split():
            return True
        if self.rt == INT and self.r >= 10:
            self.r = Pair([self.r // 2, (self.r + 1) // 2], self,
                          self.depth + 1)
            self.rt = PAIR
            return True
        if self.rt == PAIR and self.r.split():
            return True
        return False

    def explode(self):
        if self.depth == 3:
            if self.lt == PAIR:  # explodes
                ret = (PASS_TO_PREVIOUS, self.l.l)
                if self.rt == INT:
                    self.r += self.l.r
                else:  # right is also depth 4, so must be integer
                    self.r.l += self.l.r
                self.lt = INT
                self.l = 0
                return ret
            elif self.rt == PAIR:
                ret = (PASS_TO_NEXT, self.r.r)
                if self.lt == INT:
                    self.l += self.r.l
                else:  # right is also depth 4, so must be integer
                    self.l.r += self.r.l
                self.rt = INT
                self.r = 0
                return ret
            else:
                return None, None

        if self.lt == PAIR:
            ex, ex2 = self.l.explode()
            if ex2 is not None:
                if ex is None:
                    return None, ex2
                elif ex == PASS_TO_PREVIOUS:
                    return ex, ex2
                elif ex == PASS_TO_NEXT:
                    if self.rt == INT:
                        self.r += ex2
                    else:
                        self.r.add_to_leftmost(ex2)
                    return None, ex2

        if self.rt == PAIR:
            ex, ex2 = self.r.explode()
            if ex2 is not None:
                if ex is None:
                    return None, ex2
                elif ex == PASS_TO_PREVIOUS:
                    if self.lt == INT:
                        self.l += ex2
                    else:
                        self.l.add_to_rightmost(ex2)
                    return None, ex2
                elif ex == PASS_TO_NEXT:
                    return ex, ex2

        return None, None

    def add_to_leftmost(self, val):
        if self.lt == INT:
            self.l += val
        else:
            self.l.add_to_leftmost(val)

    def add_to_rightmost(self, val):
        if self.rt == INT:
            self.r += val
        else:
            self.r.add_to_rightmost(val)

    def magnitude(self):
        c = 0
        if self.lt == INT:
            c += 3 * self.l
        else:
            c += 3 * self.l.magnitude()
        if self.rt == INT:
            c += 2 * self.r
        else:
            c += 2 * self.r.magnitude()
        return c

EXPLODETESTS = [
    '[[[[[9,8],1],2],3],4]',
    '[7,[6,[5,[4,[3,2]]]]]',
    '[[6,[5,[4,[3,2]]]],1]',
    '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
    '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
]
SPLITTEST = ['[11,1]']

ADDITION_TESTS = [['[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'],
                  [
                      '[1,1]',
                      '[2,2]',
                      '[3,3]',
                      '[4,4]',
                  ], [
                      '[1,1]',
                      '[2,2]',
                      '[3,3]',
                      '[4,4]',
                      '[5,5]',
                  ], [
                      '[1,1]',
                      '[2,2]',
                      '[3,3]',
                      '[4,4]',
                      '[5,5]',
                      '[6,6]',
                  ],
                  [
                      '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                      '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                      '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                      '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                      '[7,[5,[[3,8],[1,4]]]]',
                      '[[2,[2,2]],[8,[8,1]]]',
                      '[2,9]',
                      '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                      '[[[5,[7,4]],7],1]',
                      '[[[[4,2],2],6],[8,7]]',
                  ],
                  REALDEAL]

if __name__ == "__main__":
    print('EXPLODETEST')
    for e in EXPLODETESTS:
        exp = ast.literal_eval(e)
        p = Pair(exp, None, 0)
        p.explode()
        print(p.tonestlist())

    print('SPLITTEST')
    for e in SPLITTEST:
        exp = ast.literal_eval(e)
        p = Pair(exp, None, 0)
        p.split()
        print(p.tonestlist())

    print('ADDITIONTEST')
    for addsequence in ADDITION_TESTS[-2:-1]:
        p = Pair(ast.literal_eval(addsequence[0]), None, 0)
        for number in addsequence[1:]:
            p = p.add(Pair(ast.literal_eval(number), None, 0))
        print(p.tonestlist())

    print(p.magnitude())

    p = Pair(ast.literal_eval(REALDEAL[0]), None, 0)
    for number in REALDEAL[1:]:
        p = p.add(Pair(ast.literal_eval(number), None, 0))
    print(p.tonestlist())
    print(p.magnitude())


    # PART 2
    maxmag = 0
    for ii in range(len(REALDEAL)):
        for jj in range(len(REALDEAL)):
            if ii == jj:
                continue
            p1 = Pair(ast.literal_eval(REALDEAL[ii]), None, 0)
            p2 = Pair(ast.literal_eval(REALDEAL[jj]), None, 0)
            sup = p1.add(p2)
            v = sup.magnitude()
            if v > maxmag:
                maxmag = v

    print(maxmag)