from tools import get_input
import numpy as np

SAMPLE = [
'7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
'',
'22 13 17 11  0',
' 8  2 23  4 24',
'21  9 14 16  7',
' 6 10  3 18  5',
' 1 12 20 15 19',
'',
' 3 15  0  2 22',
' 9 18 13 17  5',
'19  8  7 25 23',
'20 11 10 24  4',
'14 21 16 12  6',
'',
'14 21 17 24  4',
'10 16 15  9 19',
'18  8 23 26 20',
'22 11 13  6  5',
' 2  0 12  3  7',
]

class Day4:
    def __init__(self, lines) -> None:
        self.draws = [int(k) for k in lines[0].split(',')]
        self.boards = []
        cboard = []
        for line in lines[2:]:
            if line == '':
                self.boards.append(cboard)
                cboard = []
            else:
                cboard += [int(t) for t in line.split()]
        self.boards.append(cboard)
        cboard = []
        
        self.nb = len(self.boards)
        self.bs = len(lines[2].split())

    def solve1(self) -> int:
        rwins = [[0] * 5 for k in range(self.nb)]
        cwins = [[0] * 5 for k in range(self.nb)]

        for d in self.draws:
            for b in range(len(self.boards)):
                if d in self.boards[b]:
                    k = self.boards[b].index(d)
                    rwins[b][k // self.bs] += 1
                    cwins[b][k % self.bs] += 1
                    if (rwins[b][k // self.bs] == self.bs or
                        cwins[b][k % self.bs] == self.bs):
                        return self.scoreboard(b, d)

    def solve2(self) -> int:
        rwins = [[0] * 5 for k in range(self.nb)]
        cwins = [[0] * 5 for k in range(self.nb)]
        bwin = [False for k in range(self.nb)]
        haswon = 0

        for d in self.draws:
            for b in range(self.nb):
                if bwin[b]:
                    continue
                if d in self.boards[b]:
                    k = self.boards[b].index(d)
                    rwins[b][k // self.bs] += 1
                    cwins[b][k % self.bs] += 1
                    if (rwins[b][k // self.bs] == self.bs or
                        cwins[b][k % self.bs] == self.bs):
                        haswon += 1
                        bwin[b] = True
                        lastwin = b, d

        return self.scoreboard(*lastwin)

    def scoreboard(self, bidx, drawn):
        board = self.boards[bidx]
        rwins = [0] * 5
        cwins = [0] * 5
        for d in self.draws:
            if d in board:
                k = board.index(d)
                board[k] = 0
                if d == drawn:
                    break
        return sum(board) * drawn

if __name__ == "__main__":
    test = Day4(SAMPLE)
    print(test.solve2())
    real = Day4(get_input(4, 2021))
    print(real.solve2())