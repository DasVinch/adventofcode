from __future__ import annotations

import os
import tools as tl
import time

import typing as typ

import numpy as np

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

REAL = tl.get_input(DAYDAY, 2024)

SAMPLE = [
    'x00: 1',
    'x01: 0',
    'x02: 1',
    'x03: 1',
    'x04: 0',
    'y00: 1',
    'y01: 1',
    'y02: 1',
    'y03: 1',
    'y04: 1',
    '',
    'ntg XOR fgs -> mjb',
    'y02 OR x01 -> tnw',
    'kwq OR kpj -> z05',
    'x00 OR x03 -> fst',
    'tgd XOR rvg -> z01',
    'vdt OR tnw -> bfw',
    'bfw AND frj -> z10',
    'ffh OR nrd -> bqk',
    'y00 AND y03 -> djm',
    'y03 OR y00 -> psh',
    'bqk OR frj -> z08',
    'tnw OR fst -> frj',
    'gnj AND tgd -> z11',
    'bfw XOR mjb -> z00',
    'x03 OR x00 -> vdt',
    'gnj AND wpb -> z02',
    'x04 AND y00 -> kjc',
    'djm OR pbm -> qhw',
    'nrd AND vdt -> hwm',
    'kjc AND fst -> rvg',
    'y04 OR y02 -> fgs',
    'y01 AND x02 -> pbm',
    'ntg OR kjc -> kwq',
    'psh XOR fgs -> tgd',
    'qhw XOR tgd -> z09',
    'pbm OR djm -> kpj',
    'x03 XOR y03 -> ffh',
    'x00 XOR y04 -> ntg',
    'bfw OR bqk -> z06',
    'nrd XOR fgs -> wpb',
    'frj XOR qhw -> z04',
    'bqk OR frj -> z07',
    'y03 OR x01 -> nrd',
    'hwm AND bqk -> z03',
    'tgd XOR rvg -> z12',
    'tnw OR pbm -> gnj',
]

from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    in1: str
    op: str
    in2: str
    out: str

    def opl(self) -> typ.Callable[[bool, bool], bool]:
        if self.op == 'AND':
            return lambda a, b: a and b
        elif self.op == 'OR':
            return lambda a, b: a or b
        elif self.op == 'XOR':
            return lambda a, b: a ^ b

        raise AssertionError('Nope.')

    def __str__(self) -> str:
        if self.op == 'AND':
            op = 'and'
        elif self.op == 'OR':
            op = 'or'
        elif self.op == 'XOR':
            op = '^'

        if self.in1.startswith('x'):
            return f'{self.out} = {self.in1} {op} {self.in2}'
        if self.in2.startswith('x'):
            return f'{self.out} = {self.in2} {op} {self.in1}'
        if self.in1.startswith('y'):
            return f'{self.out} = {self.in1} {op} {self.in2}'
        if self.in2.startswith('y'):
            return f'{self.out} = {self.in2} {op} {self.in1}'

        return f'{self.out} = {self.in1} {op} {self.in2}'


def bitify(pfix: str, val: int, force_extra_zero) -> dict[str, bool]:
    out = {}
    k = 0
    while val > 0:
        out[f'{pfix}{k:02d}'] = bool(val % 2)
        val //= 2
        k += 1
    if force_extra_zero:
        out[f'{pfix}{k:02d}'] = False

    return out


def extract_number(wires: dict[str, bool], pfix: str):
    zs = [(int(k[1:]), b) for k, b in wires.items() if k[0] == pfix]
    zs.sort(key=lambda t: t[0], reverse=True)

    accum = 0
    for _, b in zs:
        accum = 2 * accum + b

    return accum


class Day:

    def __init__(self, lines: list[str], debug: bool = False) -> None:
        self.debug = debug

        self.inputwires: dict[str, bool] = {}
        self.gates: set[Gate] = set()

        k = lines.index('')

        for l in lines[:k]:
            name, val = l.split(': ')
            self.inputwires[name] = bool(int(val))

        for l in lines[k + 1:]:
            h, t = l.split(' -> ')
            a, b, c = h.split()
            self.gates.add(Gate(a, b, c, t))

    def rename_gates(self):
        renamator: dict[str, str] = {}

        for g in self.gates:
            if g.in1[0] + g.in2[0] in ['xy', 'yx']:
                if g.op == 'XOR':
                    new_out = 'k' + g.in1[1:]
                else:
                    new_out = g.op[0].lower() + g.in1[1:]
                renamator[g.out] = new_out

        new_gates: set[Gate] = set()
        for g in self.gates:
            in1, in2, op, out = g.in1, g.in2, g.op, g.out
            if in1 in renamator:
                in1 = renamator[in1]
            if in2 in renamator:
                in2 = renamator[in2]
            if out in renamator:
                out = renamator[out]

            new_gates.add(Gate(in1, op, in2, out))

        self.gates = new_gates

    def evaluate_expr(self, known_wires: dict[str, bool]):
        # known_wires will be modified.
        remaining_gates = self.gates.copy()
        solved_gates: set[Gate] = set()

        while True:
            solvable_gates = {
                g
                for g in remaining_gates
                if g.in1 in known_wires and g.in2 in known_wires
            }
            if len(solvable_gates) == 0:
                break
            for g in solvable_gates:
                known_wires[g.out] =\
                    g.opl()(known_wires[g.in1], known_wires[g.in2])

            solved_gates.update(solvable_gates)
            remaining_gates -= solvable_gates

        return solved_gates

    def recursive_correctness(self, depth: int):
        pass

    def evaluate(self, x: int, y: int) -> int:
        input_bits = bitify('x', x, True)
        input_bits.update(bitify('y', y, True))
        used_gates = self.evaluate_expr(input_bits)
        z = extract_number(input_bits, 'z')

        return z

    def check_correctness_one_bit(self, depth: int):

        for x in [2**depth - 1, 2**(depth + 1) - 1]:
            for y in [2**depth - 1, 2**(depth + 1) - 1]:
                print(x, y)
                input_bits = bitify('x', x, True)
                input_bits.update(bitify('y', y, True))

                used_gates = self.evaluate_expr(input_bits)

                z_val = extract_number(input_bits, 'z')

                assert z_val == x + y, f'{x=}, {y=}, {z_val=}'

    def check_correctness_add(self, depth: int):
        for x in range(2**(depth + 1)):
            for y in range(2**(depth + 1)):
                print(x, y)
                input_bits = bitify('x', x, True)
                input_bits.update(bitify('y', y, True))

                used_gates = self.evaluate_expr(input_bits)

                z_val = extract_number(input_bits, 'z')

                assert z_val == x + y

    def solve1(self) -> int:
        known_wires = self.inputwires.copy()

        self.evaluate_expr(known_wires)

        self.p1_wires = known_wires

        return extract_number(known_wires, 'z')

    def solve2(self) -> int:

        return 0


if __name__ == "__main__":
    t = Day(SAMPLE, True)
    print(f'Test p1: {t.solve1()}')

    r = Day(REAL)
    print(f'Real p1: {r.solve1()}')

    print(f'Test p2: {t.solve2()}')

    s = time.time()
    print(f'Real p2: {r.solve2()}')
    print(time.time() - s)

    r.rename_gates()
    a = []
    for g in r.gates:
        a += [str(g)]

    b = sorted(a)

x00 = 1
x01 = 1
x02 = 0
x03 = 0
x04 = 0
x05 = 1
x06 = 0
x07 = 1
x08 = 1
x09 = 0
x10 = 1
x11 = 0
x12 = 0
x13 = 0
x14 = 1
x15 = 0
x16 = 1
x17 = 1
x18 = 0
x19 = 1
x20 = 0
x21 = 0
x22 = 1
x23 = 1
x24 = 1
x25 = 1
x26 = 0
x27 = 1
x28 = 1
x29 = 0
x30 = 1
x31 = 0
x32 = 0
x33 = 1
x34 = 1
x35 = 0
x36 = 1
x37 = 1
x38 = 1
x39 = 1
x40 = 1
x41 = 1
x42 = 1
x43 = 1
x44 = 1
y00 = 1
y01 = 0
y02 = 1
y03 = 1
y04 = 0
y05 = 0
y06 = 1
y07 = 1
y08 = 0
y09 = 1
y10 = 1
y11 = 1
y12 = 1
y13 = 0
y14 = 1
y15 = 1
y16 = 1
y17 = 0
y18 = 1
y19 = 0
y20 = 0
y21 = 1
y22 = 0
y23 = 1
y24 = 0
y25 = 1
y26 = 0
y27 = 1
y28 = 0
y29 = 0
y30 = 1
y31 = 1
y32 = 0
y33 = 1
y34 = 0
y35 = 0
y36 = 1
y37 = 0
y38 = 1
y39 = 0
y40 = 0
y41 = 0
y42 = 1
y43 = 0
y44 = 1

# INPUT AND SERIES -- COMPLETE?
a00 = x00 and y00
a01 = x01 and y01
a02 = x02 and y02
a03 = x03 and y03
a04 = x04 and y04
a05 = x05 and y05
a06 = x06 and y06
a07 = x07 and y07
a08 = x08 and y08
a09 = x09 and y09
a10 = x10 and y10
a11 = x11 and y11
a12 = x12 and y12
a13 = x13 and y13
a14 = x14 and y14
a15 = x15 and y15
a16 = x16 and y16
a17 = x17 and y17
a18 = x18 and y18
a19 = x19 and y19
a20 = x20 and y20
a21 = x21 and y21  # SUS!
a22 = x22 and y22
a23 = x23 and y23
a24 = x24 and y24
a25 = x25 and y25
a26 = x26 and y26
a27 = x27 and y27
a28 = x28 and y28
a29 = x29 and y29
a30 = x30 and y30
a31 = x31 and y31
a32 = x32 and y32
a33 = x33 and y33
a34 = x34 and y34
a35 = x35 and y35
a36 = x36 and y36
a37 = x37 and y37
a38 = x38 and y38
a39 = x39 and y39
a40 = x40 and y40
a41 = x41 and y41
a42 = x42 and y42
a43 = x43 and y43
a44 = x44 and y44

# INPUT XOR SERIES
k00 = x00 ^ y00
k01 = x01 ^ y01
k02 = x02 ^ y02
k03 = x03 ^ y03
k04 = x04 ^ y04
k05 = x05 ^ y05
k06 = x06 ^ y06
k07 = x07 ^ y07
k08 = x08 ^ y08
k09 = x09 ^ y09
k10 = x10 ^ y10
k11 = x11 ^ y11
k12 = x12 ^ y12
k13 = x13 ^ y13
k14 = x14 ^ y14
k15 = x15 ^ y15
k16 = x16 ^ y16
k17 = x17 ^ y17
k18 = x18 ^ y18
k19 = x19 ^ y19
k20 = x20 ^ y20
k21 = x21 ^ y21
k22 = x22 ^ y22
k23 = x23 ^ y23
k24 = x24 ^ y24
k25 = x25 ^ y25
k26 = x26 ^ y26
k27 = x27 ^ y27
k28 = x28 ^ y28
k29 = x29 ^ y29
k30 = x30 ^ y30
k31 = x31 ^ y31
k32 = x32 ^ y32
k33 = x33 ^ y33
k34 = x34 ^ y34
k35 = x35 ^ y35
k36 = x36 ^ y36
k37 = x37 ^ y37
k38 = x38 ^ y38
k39 = x39 ^ y39
k40 = x40 ^ y40
k41 = x41 ^ y41
k42 = x42 ^ y42
k43 = x43 ^ y43
k44 = x44 ^ y44

# K AND SERIES
# A OR SERIES
jjp = a00 and k01
cqp = a01 or jjp
trv = k02 and cqp
htm = a02 or trv
kvt = k03 and htm
drd = a03 or kvt
rhr = k04 and drd
qjq = a04 or rhr
jcf = k05 and qjq
frn = a05 or jcf  # FIX
mgg = k06 and frn
fhw = a06 or mgg
mpv = k07 and fhw
grg = a07 or mpv
bbk = k08 and grg
dgj = a08 or bbk
bfb = k09 and dgj
hkf = a09 or bfb
crj = k10 and hkf
shm = a10 or crj
rjm = k11 and shm
tff = a11 or rjm
hfb = k12 and tff
rfq = a12 or hfb
vkk = k13 and rfq
mmr = a13 or vkk
rwf = k14 and mmr
wkq = a14 or rwf
grv = k15 and wkq
rsk = a15 or grv
pjp = k16 and rsk  # SUS!!
smg = a16 or pjp
tqm = k17 and smg
tsn = a17 or tqm
gmf = k18 and tsn
tsf = a18 or gmf
twb = k19 and tsf
qqp = a19 or twb
rss = k20 and qqp
mjj = a20 or rss
nrs = k21 and mjj
kkq = a21 or nrs
fjh = k22 and kkq
gwm = a22 or fjh
qbq = k23 and gwm
kmj = a23 or qbq
gqj = k24 and kmj
dtj = a24 or gqj
frh = k25 and dtj
bhw = a25 or frh
vvt = k26 and bhw
vgs = a26 or vvt
wtd = k27 and vgs
nvq = a27 or wtd
gnp = k28 and nvq
bsb = a28 or gnp
kgw = k29 and bsb
snr = a29 or kgw
htp = k30 and snr
dbv = a30 or htp
gdw = k31 and dbv
jgg = a31 or gdw
fpm = k32 and jgg
kth = a32 or fpm
bqr = k33 and kth
dkh = a33 or bqr
mph = k34 and dkh
stg = a34 or mph
bcc = k35 and stg
hhn = a35 or bcc
qqs = k36 and hhn
mwj = a36 or qqs
qhk = k37 and mwj
vds = a37 or qhk
skn = k38 and vds
jhv = a38 or skn
wtt = k39 and jhv  # FIX
mdn = a39 or wtt
qkq = k40 and mdn
pmn = a40 or qkq
vrq = k41 and pmn
tkc = a41 or vrq
nrr = k42 and tkc
wqr = a42 or nrr
frs = k43 and wqr
kmg = a43 or frs
gkc = k44 and kmg

z01 = k01 ^ a00
z02 = k02 ^ cqp
z03 = k03 ^ htm
z04 = k04 ^ drd
z05 = k05 ^ qjq  # IS FIX
z06 = k06 ^ frn
z07 = k07 ^ fhw
z08 = k08 ^ grg
z09 = k09 ^ dgj
z10 = k10 ^ hkf
z11 = k11 ^ shm
z12 = k12 ^ tff
z13 = k13 ^ rfq
z14 = k14 ^ mmr
z15 = k15 ^ wkq
z16 = a16 ^ rsk  # SUS
z17 = k17 ^ smg
z18 = k18 ^ tsn
z19 = k19 ^ tsf
z20 = k20 ^ qqp
z21 = k21 ^ mjj  # IS FIX
z22 = k22 ^ kkq
z23 = k23 ^ gwm
z24 = k24 ^ kmj
z25 = k25 ^ dtj
z26 = k26 ^ bhw
z27 = k27 ^ vgs
z28 = k28 ^ nvq
z29 = k29 ^ bsb
z30 = k30 ^ snr
z31 = k31 ^ dbv
z32 = k32 ^ jgg
z33 = k33 ^ kth
z34 = k34 ^ dkh
z35 = k35 ^ stg
z36 = k36 ^ hhn
z37 = k37 ^ mwj
z38 = k38 ^ vds
z39 = k39 ^ jhv  # IS FIX
z40 = k40 ^ mdn
z41 = k41 ^ pmn
z42 = k42 ^ tkc
z43 = k43 ^ wqr
z44 = k44 ^ kmg
z45 = a44 or gkc  # SUS

# NOTES
'''
z21 got rewritten as a21! Fixed.

gmq has k21 xor.
So gmq MUST SWAP with z21.

Now I rename gmq to a21.

frn needs swap with z05
wtt with z39

Need to swap k16 and a16
Which were originally... k16: vtj, a16: wnf


gmq, z21, frn, z05, wtt, z39, vtj, wnf
frn,gmq,vtj,wnf,wtt,z05,z21,z39
'''
