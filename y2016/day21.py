import typing as typ

import re

from tools import get_input

input = get_input(21, 2016)

input_test = [
    'swap position 4 with position 0',
    'swap letter d with letter b',
    'reverse positions 0 through 4',
    'rotate left 1 step',
    'move position 1 to position 4',
    'move position 3 to position 0',
    'rotate based on position of letter b',
    'rotate based on position of letter d',
]

class RE:
    SWAPP = '^swap position (\d+) with position (\d+)$'
    SWAPL = '^swap letter ([a-z]) with letter ([a-z])$'
    ROTL = '^rotate left (\d+) steps?$'
    ROTR = '^rotate right (\d+) steps?$'
    ROTB = '^rotate based on position of letter ([a-z])$'
    REV = '^reverse positions (\d+) through (\d+)$'
    MOV = '^move position (\d+) to position (\d+)$'


def apply_re(instr: str, s: list[str]) -> list[str]:
    if m := re.match(RE.SWAPP, instr):
        a, b = map(int, m.groups())
        s[a], s[b] = s[b], s[a]
        return s
    elif m := re.match(RE.SWAPL, instr):
        a, b = map(s.index, m.groups())
        s[a], s[b] = s[b], s[a]
        return s
    elif m := re.match(RE.ROTL, instr):
        k = int(m.groups()[0]) % len(s)
        return s[k:] + s[:k]
    elif m := re.match(RE.ROTR, instr):
        k = int(m.groups()[0]) % len(s)
        return s[-k:] + s[:-k]
    elif m := re.match(RE.ROTB, instr):
        idx = s.index(m.groups()[0])
        k = (1 + idx + (1 if idx >= 4 else 0)) % len(s)
        return s[-k:] + s[:-k]
    elif m := re.match(RE.REV, instr):
        a, b = map(int, m.groups())
        return s[:a] + s[b:a:-1] + [s[a]] + s[b+1:]
    elif m := re.match(RE.MOV, instr):
        f, t = map(int, m.groups())
        let = s.pop(f)
        s.insert(t, let)
        return s
    else:
        raise ValueError()
    
def reverse_apply_re(instr: str, s: list[str]) -> list[str]:
    if m := re.match(RE.SWAPP, instr):
        a, b = map(int, m.groups())
        s[a], s[b] = s[b], s[a]
        return s
    elif m := re.match(RE.SWAPL, instr):
        a, b = map(s.index, m.groups())
        s[a], s[b] = s[b], s[a]
        return s
    elif m := re.match(RE.ROTL, instr): # Becomes ROTR
        k = int(m.groups()[0]) % len(s)
        return s[-k:] + s[:-k]
    elif m := re.match(RE.ROTR, instr): # Becomes ROTL
        k = int(m.groups()[0]) % len(s)
        return s[k:] + s[:k]
    elif m := re.match(RE.ROTB, instr): # HARD
        for k in range(len(s)):
            ss = s[k:] + s[:k]
            idx = ss.index(m.groups()[0])
            k = (1 + idx + (1 if idx >= 4 else 0)) % len(ss)
            sss = ss[-k:] + ss[:-k]
            if s == sss:
                return ss
        raise AssertionError()
    elif m := re.match(RE.REV, instr):
        a, b = map(int, m.groups())
        return s[:a] + s[b:a:-1] + [s[a]] + s[b+1:]
    elif m := re.match(RE.MOV, instr): # INVERT INDEX
        f, t = map(int, m.groups())
        let = s.pop(t)
        s.insert(f, let)
        return s
    else:
        raise ValueError()
    

if __name__ == "__main__":
    s = list('abcde')
    for instr in input_test:
        print(instr)
        s = apply_re(instr, s)
        print(''.join(s))

    print('-------------')

    s = list('abcdefgh')
    for instr in input:
        print(instr)
        s = apply_re(instr, s)
        print(''.join(s))

    print('-------------')

    s = list('decab')
    for instr in input_test[::-1]:
        print(instr)
        s = reverse_apply_re(instr, s)
        print(''.join(s))

    print('-------------')

    s = list('fdhbcgea')
    for instr in input[::-1]:
        print(instr)
        s = reverse_apply_re(instr, s)
        print(''.join(s))

    print('-------------')   

    s = list('fbgdceah')
    for instr in input[::-1]:
        print(instr)
        s = reverse_apply_re(instr, s)
        print(''.join(s))

        


