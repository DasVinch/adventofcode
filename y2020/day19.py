import os
from tools import get_input
import re

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
'0: 4 1 5',
'1: 2 3 | 3 2',
'2: 4 4 | 5 5',
'3: 4 5 | 5 4',
'4: "a"',
'5: "b"',
'',
'ababbb',
'bababa',
'abbbab',
'aaabbb',
'aaaabbb',
]

REAL = get_input(DAYDAY, 2020)

import re


class Day:
    def __init__(self, lines: list[str]) -> None:
        
        break_index = lines.index('')

        self.rules = lines[:break_index]

        self.messages = lines[break_index+1:]

        ### Resolve rules into a big regex
        self.rule_dict: dict[int, str] = {}

        for r in self.rules:
            spl = r.split(': ')
            n = int(spl[0])
            rl = spl[1]
            self.rule_dict[n] = rl

        self.prepare_regexes()

    def prepare_regexes(self):

        self.regex_resolution: dict[int, str] = {}

        for n, rule in self.rule_dict.items():
            if n in self.regex_resolution: 
                continue
            self.regex_resolution[n] = self.rec_regex_res(rule, n)

        self.re0 = re.compile(self.regex_resolution[0])

    def rec_regex_res(self, rule: str, n: int | None) -> str:
        if n and n in self.regex_resolution:
            return self.regex_resolution[n]
            
        if rule.startswith('"'):
            if n:
                self.regex_resolution[n] = rule[1:-1]
            return rule[1:-1]

        if "|" in rule:
            sub_rules = rule.split(" | ")
            new_expr = '(' + '|'.join(self.rec_regex_res(sub_rule, None) for sub_rule in sub_rules) + ')'
            if n:
                self.regex_resolution[n] = new_expr
            return new_expr

        sub_rules = rule.split()
        for sub_rule in sub_rules:
            sub_idx = int(sub_rule)
            res = self.rec_regex_res(self.rule_dict[sub_idx], sub_idx)

        new_expr = ''.join(self.regex_resolution[int(n)] for n in sub_rules)
        if n:
            self.regex_resolution[n] = new_expr
        return new_expr


    def solve1(self):
        count = 0
        for msg in self.messages:
            if re.fullmatch(self.re0, msg):
                count += 1
        return count

    def solve2(self):
        pass

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())