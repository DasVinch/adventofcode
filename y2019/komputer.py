from __future__ import annotations

import typing as typ


class Komputer:

    def __init__(self, ribbon: list[int]):
        self.orig_ribbon = ribbon.copy()
        
        self.ribbon: dict[int, int]

        self.reset()

    def reset(self) -> None:
        self.ribbon = {}
        for k, v in enumerate(self.orig_ribbon):
            self.ribbon[k] = v
        self.ip: int = 0
        self.rel_memp: int = 0
        self.outputs: list[int] = []

    def execute_one_instruction(self, ip: int | None = None) -> bool:
        if ip is None:
            ip = self.ip

        full_inst = self.ribbon[ip]

        mode3 = (full_inst // 10000) % 10
        mode2 = (full_inst // 1000) % 10
        mode1 = (full_inst // 100) % 10

        opcode = full_inst % 100

        #print(ip, opcode, self.ribbon[:15])

        if opcode == 1:  # ADD a b c
            self.wra(mode3, ip + 3, self.dfa(mode1, ip + 1) + self.dfa(mode2, ip + 2))
            self.ip += 4
        elif opcode == 2:  # MUL a b c
            self.wra(mode3, ip + 3, self.dfa(mode1, ip + 1) * self.dfa(mode2, ip + 2))
            self.ip += 4
        elif opcode == 3:  # INPUT
            self.wra(mode1, ip + 1, self.get_input())
            self.ip += 2
        elif opcode == 4:  # OUTPUT
            self.output(self.dfa(mode1, ip + 1))
            self.ip += 2
        elif opcode == 5:
            if self.dfa(mode1, ip + 1) != 0:
                self.ip = self.dfa(mode2, ip + 2)
            else:
                self.ip += 3
        elif opcode == 6:
            if self.dfa(mode1, ip + 1) == 0:
                self.ip = self.dfa(mode2, ip + 2)
            else:
                self.ip += 3
        elif opcode == 7:
            if self.dfa(mode1, ip + 1) < self.dfa(mode2, ip + 2):
                self.wra(mode3, ip + 3, 1)
            else:
                self.wra(mode3, ip + 3, 0)
            self.ip += 4
        elif opcode == 8:
            if self.dfa(mode1, ip + 1) == self.dfa(mode2, ip + 2):
                self.wra(mode3, ip + 3, 1)
            else:
                self.wra(mode3, ip + 3, 0)
            self.ip += 4
        elif opcode == 9:
            self.rel_memp += self.dfa(mode1, ip+1)
            self.ip += 2
        elif opcode == 99:
            return False
        else:
            raise ValueError()

        return True

    def execute_all(self):
        self.ip = 0

        while self.execute_one_instruction():
            pass

    def ascii_input(self, s: str):
        for c in s:
            self.execute_til_input()
            self.pending_input = ord(c)
            self.execute_one_instruction()
        self.execute_til_input()
        self.pending_input = ord('\n')
        self.execute_one_instruction()


    def execute_til_input(self):
        while self.ribbon[self.ip] % 100 != 3:
            if self.ribbon[self.ip] == 99:
                raise ValueError
            self.execute_one_instruction()
        # Next instruction will be an input

    def execute_til_output(self) -> int:
        while self.ribbon[self.ip] % 100 != 4:
            if self.ribbon[self.ip] == 99:
                raise ValueError
            self.execute_one_instruction()
        
        if self.ribbon[self.ip] == 99:
                raise ValueError
        self.execute_one_instruction()
        return self.outputs[-1]

    def df(self, mode: int, val: int) -> int:
        if mode == 1:
            return val
        elif mode == 2:
            return self.ribbon.get(val + self.rel_memp, 0)
        else:
            return self.ribbon.get(val, 0)

    def dfa(self, mode: int, addr: int) -> int:
        return self.df(mode, self.ribbon[addr])

    def wr(self, mode_wr: int, addr: int, val: int) -> None:
        offset = 0 if mode_wr == 0 else self.rel_memp
        self.ribbon[addr + offset] = val

    def wra(self, mode_wr: int, addraddr: int, val: int) -> None:
        offset = 0 if mode_wr == 0 else self.rel_memp
        self.ribbon[self.ribbon[addraddr] + offset] = val

    def get_input(self) -> int:
        return self.pending_input

    def output(self, val: int) -> int:
        self.outputs.append(val)
        return val
