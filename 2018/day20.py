from tools import get_input

SAMPLES = [
    '^WNE$', # 3
    '^ENWWW(NEEE|SSE(EE|N))$', # 10
    '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', # 18
    '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', # 23
    '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', # 31
]

REAL = get_input(200, 2018)[0]


class Regex:

    NODES = 0

    def __init__(self) -> None:
        self.base = ''
        self.subexps = []
        self.nextregex = None
        self.thisnode = Regex.NODES
        Regex.NODES += 1

    def __str__(self):
        s =  f'[{self.thisnode}]'
        s += f'{self.base}'
        if len(self.subexps) > 0:
            s += '('
            for sub in self.subexps[:-1]:
                s += sub.__str__()
                s += '|'
            s += self.subexps[-1].__str__()
            s += ')'
        if self.nextregex is not None:
            s += self.nextregex.__str__()
        return s

    def process(self, regex):
        #print(regex, '-------', self)
        k = 0
        while k < len(regex) and regex[k] in 'NWSE':
            k += 1
        self.base = regex[:k]

        if k == len(regex):
            return ''

        r = regex[k:]
        if r[0] in ')|':
            return r
        elif r[0] == '(':
            c = '|'
            while c == '|':
                self.subexps += [Regex()]
                r = self.subexps[-1].process(r[1:])
                c = r[0]
            r = r[1:] # pop the ')'

        if len(r) > 0:
            if r[0] in ')|':
                return r
            else:
                self.nextregex = Regex()
                rr = self.nextregex.process(r)
                return rr

        else:
            return ''

    def countminimax(self):
        tot = len(self.base)
        if len(self.subexps):
            sublens = [sub.countminimax() for sub in self.subexps]
            if 0 not in sublens:
                tot += max(sublens)
        if self.nextregex is not None:
            tot += self.nextregex.countminimax()

        return tot

    def countbydistance(self):
        distcount = {}
        for c in range(len(self.base)):
            distcount[c+1] = 1
        k = len(distcount)

        subdists = [sub.countbydistance() for sub in self.subexps]
        sublens = [sub.countminimax() for sub in self.subexps]

        if 0 not in sublens:
            for s in subdists:
                for kk in s:
                    distcount[k + kk] = distcount.get(k+kk, 0) + s[kk]
        else:
            for s in subdists:
                if len(s) > 0:
                    mm = max(s)
                    for kk in range(1, mm//2 + 1):
                        distcount[k + kk] = distcount.get(k+kk, 0) + s[kk]

        if self.nextregex is not None:
            if not 0 in sublens:
                print(f'Assumption fails: {sublens} {[s.base for s in self.subexps]}')
                print(f'    Followed by {self.nextregex.base}')
                #import pdb; pdb.set_trace()
            sback = self.nextregex.countbydistance()
            for kk in sback:
                distcount[k + kk] = distcount.get(k+kk, 0) + sback[kk]

        return distcount




if __name__ == "__main__":
    for k in range(5):
        t = Regex()
        t.process(SAMPLES[k][1:-1])
        print(t)
        print(t.countminimax())
        print(t.countbydistance())

    r = Regex()
    r.process(REAL[1:-1])
    print(r.countminimax())
    D = r.countbydistance()
    print(sum([D[k] for k in D if k >= 1000]))

    # 9448 too high
    # 9000 too high