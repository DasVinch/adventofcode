from __future__ import annotations

import typing as typ
import tools as tl

SAMPLE: list[str] | None = None

ADDITIONAL_SAMPLES: list[list[str]] = []

T_DATA: typ.TypeAlias = list[int]  # TODO

from .komputer import Komputer
import numpy as np


class Day:

    @staticmethod
    def parse_input(input: list[str]) -> T_DATA:
        return [int(t) for t in input[0].split(',')]

    def __init__(self, data: T_DATA, debug: bool = False) -> None:
        self.data = data
        self.debug = debug
        ...

    def solve1(self) -> int:
        komp = Komputer(self.data)
        komp.execute_all()

        out = np.asarray(komp.outputs, np.uint8)

        str_out = out.tobytes().decode('utf8')
        print(str_out)

        lines = str_out.rstrip().split('\n')

        mm, nn = len(lines), len(lines[0])
        self.mm, self.nn = mm, nn

        crossings: list[tuple[int, int]] = []
        total = 0

        for rr in range(1, mm - 1):
            for cc in range(1, nn - 1):
                if (lines[rr][cc] == '#' and lines[rr - 1][cc] == '#'
                        and lines[rr + 1][cc] == '#'
                        and lines[rr][cc - 1] == '#'
                        and lines[rr][cc + 1] == '#'):
                    crossings += [(rr, cc)]
                    total += rr * cc

        return total

    def solve2(self) -> int:
        # Manual analysis

        PATH_OUT_COM = (
            'R,8,L,12,R,8,'
            'R,8,L,12,R,8,'
            'L,10,L,10,R,8,'
            'L,12,L,12,L,10,R,10,'
            'L,10,L,10,R,8,'
            'L,12,L,12,L,10,R,10,'
            'L,10,L,10,R,8,'
            'R,8,L,12,R,8,'
            'L,12,L,12,L,10,R,10,'
            'R,8,L,12,R,8'
            )
        SEQ = 'A,A,C,B,C,B,C,A,B,A'
        A = 'R,8,L,12,R,8'
        B = 'L,12,L,12,L,10,R,10'
        C = 'L,10,L,10,R,8'

        data2 = self.data.copy()
        data2[0] = 2
        komp = Komputer(data2)


        komp.ascii_input(SEQ)
        komp.ascii_input(A)
        komp.ascii_input(B)
        komp.ascii_input(C)


        komp.ascii_input('y')

        last = 0

        while True:
            komp.execute_one_instruction()
            if len(komp.outputs):
                print(chr(komp.outputs[0]), end='')
                

                if komp.outputs[0] > 255:
                    return komp.outputs[0]

                #if last == 10 and komp.outputs[0] == 10:
                #    import time
                #    time.sleep(0.1)

                last = komp.outputs[0]
                komp.outputs = []

        komp.ascii_input('n')

        komp.outputs = []

        while True:
            komp.execute_one_instruction()
            if len(komp.outputs):
                print(komp.outputs[0], chr(komp.outputs[0]))
                komp.outputs = []

        



def find_all_sublists(l: list[str]) -> dict[tuple[str,...], int]:
            if len(l) == 0:
                return {}

            if len(l) == 1:
                return {tuple(l): 1}

            sub_tail = find_all_sublists(l[1:])
            for k in range(1,len(l)+1):
                tk = tuple(l[:k])
                sub_tail[tk] = sub_tail.get(tk, 0) + 1
            
            return sub_tail

def make_sublist(l: list[str], s: typ.Sequence[str]) -> list[list[str]]:
    substrings = ','.join(l).replace(','.join(s), '#').split('#')
    substringlist = [t.strip(',').split(',') for t in substrings]
    return [ss for ss in substringlist if ss not in ([], [''])]


def can_substitute_in_n(token_list_list:list[list[str]], n_sub: int = 0) -> list[str] | bool:
    token_list_list = [l for l in token_list_list if len(l) > 0]
    
    if n_sub == 0:
        return len(token_list_list) == 0
    if len(token_list_list) == 0:
        return True

    all_sub_lists: dict[tuple[str, ...], int] = {}
    for token_list in token_list_list:
        sub_lists = find_all_sublists(token_list)
        for sub, count in sub_lists.items():
            all_sub_lists[sub] = all_sub_lists.get(sub, 0) + count


    for sub in all_sub_lists:
        if len(','.join(sub)) > 20: # Too long
            continue
        token_sublists: list[list[str]] = []

        candidate_sub_solution = [] # AAAAH NOOOOOO

        for token_list in token_list_list:
            token_sublists += make_sublist(token_list, sub)

            #print(s, token_list, token_sublists)
            #breakpoint()

            res = can_substitute_in_n(token_sublists, n_sub-1)
            
            if res is False:
                ...


            if res is True:
                breakpoint()
                return [','.join(sub)]
            else:
                breakpoint()
                return [','.join(sub)] + res

    return False

        




    return any((can_substitute_in_n))


''