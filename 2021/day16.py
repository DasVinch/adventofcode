from tools import get_input, make_int_matrix
import numpy as np

A = '8A004A801A8002F478'
B = '620080001611562C8802118E34'
C = 'C0015000016115A2E0802F182340'
D = 'A0016C880162017C3686B18A3D4780'

def hex2bin(hexstr):
    return ''.join([f'{int("0x" + c, 16):04b}' for c in hexstr])


class Packet:
    def __init__(self) -> None:
        pass

    def init(self, binstr) -> None:
        self.version = int(binstr[:3], 2)
        self.type = int(binstr[3:6], 2)
        self.subpackets = []

        if self.type == 4:
            remainder = binstr[6:]
            self.val = 0
            while remainder[0] == '1':
                self.val *= 16
                self.val += int(remainder[1:5], 2)
                remainder = remainder[5:]
            self.val *= 16
            self.val += int(remainder[1:5], 2)
            remainder = remainder[5:]
            #print(f'Value packet {self.val}, left {remainder}')

        else:
            ibit = binstr[6]
            if ibit == '0':
                lensubpackets = int(binstr[7:22], 2)
                #print(f'Op packet type 0 lensubs {lensubpackets}')
                remainder = binstr[22:22+lensubpackets]
                tail = binstr[22+lensubpackets:]
                while len(remainder) > 0:
                    p = Packet()
                    remainder = p.init(remainder)
                    self.subpackets.append(p)
                remainder = tail
            else: # ibit == '1'
                nsubpackets = int(binstr[7:18], 2)
                remainder = binstr[18:]
                #print(f'Op packet type 1 lensubs {nsubpackets}')
                for k in range(nsubpackets):
                    p = Packet()
                    remainder = p.init(remainder)
                    self.subpackets.append(p)

        return remainder # excess bits

    def version_sum(self):
        return self.version + sum([p.version_sum() for p in self.subpackets])

    def evaluate(self):
        if self.type == 4:
            return self.val

        elif self.type == 0:
            return sum([p.evaluate() for p in self.subpackets])
        elif self.type == 1:
            res = 1
            for p in self.subpackets:
                res *= p.evaluate()
            return res
        elif self.type == 2:
            return min([p.evaluate() for p in self.subpackets])
        elif self.type == 3:
            return max([p.evaluate() for p in self.subpackets])
        elif self.type == 5:
            return int(self.subpackets[0].evaluate() > self.subpackets[1].evaluate())
        elif self.type == 6:
            return int(self.subpackets[0].evaluate() < self.subpackets[1].evaluate())
        elif self.type == 7:
            return int(self.subpackets[0].evaluate() == self.subpackets[1].evaluate())


def evaluate(hexstring):
    p = Packet()
    p.init(hex2bin(hexstring))
    return p.evaluate()

if __name__ == "__main__":
    p = Packet(); p.init(hex2bin(A)); print(p.version_sum())
    p = Packet(); p.init(hex2bin(B)); print(p.version_sum())
    p = Packet(); p.init(hex2bin(C)); print(p.version_sum())
    p = Packet(); p.init(hex2bin(D)); print(p.version_sum())

    print(evaluate('C200B40A82'))
    print(evaluate('04005AC33890'))
    print(evaluate('880086C3E88112'))
    print(evaluate('CE00C43D881120'))
    print(evaluate('D8005AC2A8F0'))
    print(evaluate('F600BC2D8F'))
    print(evaluate('9C005AC2F8F0'))
    print(evaluate('9C0141080250320F1802104A08'))

    print(evaluate(get_input(16,2021)[0]))
    