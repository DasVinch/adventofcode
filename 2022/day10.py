from tools import get_input
import numpy as np

SAMPLE = get_input(100, 2022)
REAL = get_input(10, 2022)

class D10:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.x = 1

        self.cumstrength = 0

        self.screen = np.zeros((6, 40), np.uint8)

    def run(self):
        hold = False
        ip = 0
        clock = 1
        while ip < len(self.lines):
            if abs(((clock-1) % 40) - self.x) <= 1:
                self.screen[clock // 40, clock % 40] = 1
            if (clock - 20) % 40 == 0:
                self.cumstrength += self.x * clock
                print(clock, ip, self.x, self.x * clock, self.cumstrength)
            
            ilist = self.lines[ip].split()
            if ilist[0] == 'addx':
                if hold:
                    self.x += int(ilist[1])
                    hold = False
                else:
                    ip -= 1
                    hold = True
            ip += 1
            clock += 1
        
        return self.cumstrength

    def printscreen(self):
        for k in range(6):
            for p in range(40):
                print(('.','#')[self.screen[k,p]], end='')
            print()

if __name__ == "__main__":
    t = D10(SAMPLE)
    print(t.run())
    r = D10(REAL)
    print(r.run())




