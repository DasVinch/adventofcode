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
                self.fields += [(int(a[0]),int(a[1]), int(b[0]), int(b[1]))]
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
        
        self.tickets = [t for (k,t) in enumerate(self.tickets) if not badticket[k]]


        # This is bullshit

        n_fields = len(self.fields)
        pending_fields = set(range(n_fields))
        field_mapping = {}
        while len(pending_fields) > 0:
            field = pending_fields.pop()
            for ticket_field in range(n_fields):
                good = True
                for t in self.tickets:
                    if not self.valuefvalid(field, t[ticket_field]):
                        good = False
                        break
                if good:
                    field_mapping[field] = ticket_field
                    print(f'Assign field {field} to ticketfield {ticket_field}')
                    break
            else:
                pending_fields.add(field)

        return 0

if __name__ == "__main__":
    t = Day(SAMPLE)
    print(t.solve2())
    r = Day(REAL)
    print(r.solve1())