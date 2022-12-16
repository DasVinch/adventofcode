import os
import numpy as np
from tools import get_input

DAYDAY = int(os.path.basename(__file__).split('.')[0][3:])

# if hacking with another file-based example
# DAYDAY *= 10

SAMPLE = [
    'class: 1-3 or 5-7',
    'row: 6-11 or 33-44',
    'seat: 13-40 or 45-50',
    '',
    'your ticket:',
    '7,1,14',
    '',
    'nearby tickets:',
    '7,3,47',
    '40,4,50',
    '55,2,20',
    '38,6,12',
]

SAMPLE2 = [
    'class: 0-1 or 4-19',
    'row: 0-5 or 8-19',
    'seat: 0-13 or 16-19',
    '',
    'your ticket:',
    '11,12,13',
    '',
    'nearby tickets:',
    '3,9,18',
    '15,1,5',
    '5,14,9',
]

REAL = get_input(DAYDAY, 2020)


class Day:

    def __init__(self, lines) -> None:
        fields = True
        my_ticket = False
        other_tickets = False

        self.fnames = []
        self.fields = []
        self.mine = []
        self.tickets = []

        for k, l in enumerate(lines):
            if fields:
                if l == '':
                    fields = False
                    my_ticket = True
                    continue
                split = l.split(':')
                self.fnames += [split[0]]
                s1 = split[1].split()[0]
                s2 = split[1].split()[2]
                a = s1.split('-')
                b = s2.split('-')
                self.fields += [(int(a[0]), int(a[1]), int(b[0]), int(b[1]))]
            if my_ticket:
                if l[:4] == 'your':
                    continue
                if l == '':
                    other_tickets = True
                    my_ticket = False
                    continue
                self.mine = [int(t) for t in l.split(',')]
            if other_tickets:
                if l[:4] == 'near':
                    continue
                self.tickets += [[int(t) for t in l.split(',')]]

        self.fields = np.asarray(self.fields)

    def valuefvalid(self, k, n):
        f = self.fields[k]
        if n >= f[0] and n <= f[1]:
            return True
        if n >= f[2] and n <= f[3]:
            return True

    def valuevalid(self, n):
        for f in self.fields:
            if n >= f[0] and n <= f[1]:
                return True
            if n >= f[2] and n <= f[3]:
                return True

        return False

    def solve1(self):
        invalsum = 0
        for ticket in self.tickets:
            for val in ticket:
                if not self.valuevalid(val):
                    invalsum += val

        return invalsum

    def solve2(self):
        invalsum = 0
        badticket = [False for t in self.tickets]
        for k, ticket in enumerate(self.tickets):
            for val in ticket:
                if not self.valuevalid(val):
                    invalsum += val
                    badticket[k] = True
                    break

        # Remove bad tickets
        self.tickets = [
            t for (k, t) in enumerate(self.tickets) if not badticket[k]
        ]
        self.tickets = np.asarray(self.tickets)
        # Build compliance matrix
        self.compl_tensor = (
            ((self.tickets[:, None, :] >= self.fields[:, 0][None, :, None]) &
             (self.tickets[:, None, :] <= self.fields[:, 1][None, :, None])) |
            ((self.tickets[:, None, :] >= self.fields[:, 2][None, :, None]) &
             (self.tickets[:, None, :] <= self.fields[:, 3][None, :, None])))
        self.compl_matrix = np.all(self.compl_tensor, axis=0).astype(np.uint8)

        hit = True
        while hit:
            hit = False
            while np.any(np.sum(self.compl_matrix, axis=0) == 1):
                hit = True
                k = np.argmax(np.sum(self.compl_matrix, axis=0) == 1)
                l = np.argmax(self.compl_matrix[:,k])
                self.compl_matrix[l,:] = 0
                self.compl_matrix[l,k] = 2
            while np.any(np.sum(self.compl_matrix, axis=1) == 1):
                hit = True
                k = np.argmax(np.sum(self.compl_matrix, axis=1) == 1)
                l = np.argmax(self.compl_matrix[k,:])
                self.compl_matrix[:,l] = 0
                self.compl_matrix[k,l] = 2
            
            
            

        self.field_mapping = {k: np.argmax(self.compl_matrix[k,:]) for k in range(len(self.fnames))}

        self.my_ticket_solved = {name: self.mine[self.field_mapping[kk]] for kk, name in enumerate(self.fnames)}
        print(self.my_ticket_solved)

        tot = 1
        for fname in self.fnames:
            if fname.startswith('departure'):
                #print('a')
                tot *= self.my_ticket_solved[fname]

        return tot


if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    t2 = Day(SAMPLE2)
    print(t2.solve2())
    r = Day(REAL)
    print(r.solve2())