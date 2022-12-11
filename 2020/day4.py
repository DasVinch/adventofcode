import os
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
    'byr:1937 iyr:2017 cid:147 hgt:183cm',
    '',
    'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
    'hcl:#cfa07d byr:1929',
    '',
    'hcl:#ae17e1 iyr:2013',
    'eyr:2024',
    'ecl:brn pid:760753108 byr:1931',
    'hgt:179cm',
    '',
    'hcl:#cfa07d eyr:2025 pid:166559648',
    'iyr:2011 ecl:brn hgt:59in',
]

REAL = get_input(DAYDAY, 2020)


class Day:
    def __init__(self, lines) -> None:
        self.passports = []
        p = {}
        for l in lines + ['']:
            if l == '':
                self.passports += [p]
                p = {}
                continue
            for ss in l.split():
                f, v = ss.split(':')
                p[f] = v


    def isnumber(self, s, digits = None):
        if digits is not None:
            return len(s) == digits and all([c in '0123456789' for c in s])
        else:
            return all([c in '0123456789' for c in s])

    def solve1(self):
        tot = 0
        for p in self.passports:
            if ('byr' in p and 'iyr' in p and 'eyr' in p and 'hgt' in p and
            'hcl' in p and 'ecl' in p and 'pid' in p):
                tot += 1
        return tot

    def solve2(self):
        tot = 0
        for p in self.passports:
            if ('byr' in p and 'iyr' in p and 'eyr' in p and 'hgt' in p and
            'hcl' in p and 'ecl' in p and 'pid' in p):
                valid = True
                valid &= self.isnumber(p['byr'], 4)
                if valid:
                    b = int(p['byr'])
                    valid &= b >= 1920 and b <= 2002

                valid &= self.isnumber(p['iyr'], 4)
                if valid:
                    b = int(p['iyr'])
                    valid &= b >= 2010 and b <= 2020

                valid &= self.isnumber(p['eyr'], 4)
                if valid:
                    b = int(p['eyr'])
                    valid &= b >= 2020 and b <= 2030

                valid &= self.isnumber(p['hgt'][:-2]) and p['hgt'][-2:] in ['in', 'cm']
                if valid:
                    h = int(p['hgt'][:-2])
                    if p['hgt'][-2:] == 'in':
                        valid &= h >= 59 and h <= 76
                    else:
                        valid &= h >= 150 and h <= 193
                
                valid &= p['hcl'][0] == '#' and all([c in '0123456789abcdef' for c in p['hcl'][1:]]) and len(p['hcl']) == 7
                valid &= p['ecl'] in ['amb','blu','brn','gry','grn','hzl','oth']
                valid &= self.isnumber(p['pid'], 9)

                if valid:
                    tot += 1

        return tot

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve1())
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())
    print(r.solve2())