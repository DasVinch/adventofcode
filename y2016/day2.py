import typing as typ

from tools import get_input
import numpy as np

SAMPLE = [
'ULL',
'RRDDD',
'LURDL',
'UUUUD'
]


class Day2:

    def __init__(self, lines: typ.List[str]) -> None:

        self.lines = lines

        self.pos_r = 1
        self.pos_c = 1

        self.out_buff: typ.List[int] = []
        self.out_buff2: typ.List[str] = []

    def init_part2(self):
        self.pos_r = 2
        self.pos_c = 0
    
    def get_digit(self) -> int:
        return self.pos_r*3 + self.pos_c + 1
    
    def get_digit2(self) -> str:
        match self.pos_r:
            case 0:
                return '1'
            case 1:
                return str(self.pos_c + 1)
            case 2:
                return str(self.pos_c + 5)
            case 3:
                return chr(64 + self.pos_c)
            case 4:
                return 'D'
            case _:
                raise ValueError('asdf')

    def solve1(self) -> str:
        self.out_buff = []
        for line in self.lines:
            self.move_line(line)
            self.out_buff.append(self.get_digit())

        return ''.join(map(str, self.out_buff))

    def move_line(self, line):
        for char in line:
            match char:
                case 'U':
                    self.pos_r = max(0, self.pos_r - 1)
                case 'D':
                    self.pos_r = min(2, self.pos_r + 1)
                case 'L':
                    self.pos_c = max(0, self.pos_c - 1)
                case 'R':
                    self.pos_c = min(2, self.pos_c + 1)
                case _:
                    raise ValueError('Burk')

    def move_line_2(self, line) -> None:
        for char in line:
            self.move_char_2(char)
        

    def move_char_2(self, char) -> None:
        match char:
            case 'U':
                r, c = self.pos_r - 1, self.pos_c
            case 'D':
                r, c = self.pos_r + 1, self.pos_c
            case 'L':
                r, c = self.pos_r, self.pos_c - 1
            case 'R':
                r, c = self.pos_r, self.pos_c + 1
            case _:
                raise ValueError('Burk')
            
        if abs(r-2) + abs(c-2) <= 2:
            self.pos_r, self.pos_c = r, c


    def solve2(self) -> str:
        self.init_part2()
        self.out_buff2 = []
        for line in self.lines:
            self.move_line_2(line)
            self.out_buff2.append(self.get_digit2())
        return ''.join(self.out_buff2)



if __name__ == "__main__":
    test = Day2(SAMPLE)
    print(test.solve1())
    real = Day2(get_input(2, 2016))
    print(real.solve1())

    print(test.solve2())
    print(real.solve2())