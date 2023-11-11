import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
'light red bags contain 1 bright white bag, 2 muted yellow bags.',
'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
'bright white bags contain 1 shiny gold bag.',
'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
'faded blue bags contain no other bags.',
'dotted black bags contain no other bags.',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.container = []
        self.hash = {}
        self.revhash = {}
        self.hashnext = 0
        self.rules = {}
        self.numericrules = {}

        for line in lines:
            #print(line)
            a, b = line.split(' contain ')
            conter = ''.join(a.split()[:2])
            if not conter in self.hash:
                self.hash[conter] = self.hashnext
                self.revhash[self.hashnext] = conter
                self.hashnext += 1
            hashconter = self.hash[conter]
            self.rules[hashconter] = set()
            self.numericrules[hashconter] = set()

            if b == "no other bags.":
                continue

            contees = [''.join(s.split()[1:3]) for s in b.split(',')]
            conteescount = [int(s.split()[0]) for s in b.split(',')]
            for k in range(len(contees)):
                if not contees[k] in self.hash:
                    self.hash[contees[k]] = self.hashnext
                    self.revhash[self.hashnext] = contees[k]
                    self.hashnext += 1
                    hashcontee = self.hash[contees[k]]
                self.rules[hashconter].add(self.hash[contees[k]])
                self.numericrules[hashconter].add((conteescount[k], self.hash[contees[k]]))


    def solve1(self):
        myhash = self.hash["shinygold"]
        self.allcont = set()
        pending = {myhash}
        while len(pending) > 0:
            workinghash = pending.pop()
            self.allcont.add(workinghash)
            for c in self.rules:
                #print(self.revhash[c])
                if c in self.allcont:
                    continue
                for cc in self.rules[c]:
                    if cc in self.allcont:
                        pending.add(c)
                        break

        return len(self.allcont) - 1

    def solve2(self):
        myhash = self.hash["shinygold"]
        self.howmany = {}
        return self.countsubbags(myhash)

    def countsubbags(self, bag):
        if bag in self.howmany:
            return self.howmany[bag]
        t = 0

        for c, h in self.numericrules[bag]:
            t += c * (self.countsubbags(h) + 1)

        self.howmany[bag] = t
        return t

        

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    #print([t.revhash[tt] for tt in t.allcont])
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())
