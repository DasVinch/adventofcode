from tools import get_input
import numpy as np

SAMPLE1 = [
    'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'
]
SAMPLE2 = [
    'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
    'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
    'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
    'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
    'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
    'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
    'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
    'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
    'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
    'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce',
]


class Day8:

    def __init__(self, lines) -> None:
        splits = [line.split(' | ') for line in lines]
        self.seqs = [s[0].split() for s in splits]
        self.outs = [s[1].split() for s in splits]

    def solve1(self) -> int:
        return sum([sum([len(ss) in {2,3,4,7} for ss in s]) for s in self.outs])

    def solve2(self) -> int:
        tot = 0
        for seq, out in zip(self.seqs, self.outs):
            v = [None for _ in range(10)]
            for tt in seq:
                t = set(tt)
                if len(t) == 2:
                    v[1] = set(t)
                elif len(t) == 3:
                    v[7] = set(t)
                elif len(t) == 4:
                    v[4] = set(t)
                elif len(t) == 7:
                    v[8] = set(t)
            for tt in seq:
                t = set(tt)
                if len(t) == 5:
                    if t.issuperset(v[1]):
                        v[3] = t
                    elif t.issuperset(v[4].difference(v[1])):
                        v[5] = t
                    else:
                        v[2] = t
                if len(t) == 6:
                    if t.issuperset(v[4]):
                        v[9] = t
                    elif t.issuperset(v[7]):
                        v[0] = t
                    else:
                        v[6] = t
            stot = 0
            for dig in out:
                stot *= 10
                sdig = set(dig)
                stot += v.index(sdig)

            tot += stot

        return tot



if __name__ == "__main__":
    test = Day8(SAMPLE1)
    print(test.solve2())
    test = Day8(SAMPLE2)
    print(test.solve2())
    real = Day8(get_input(8, 2021))
    print(real.solve2())