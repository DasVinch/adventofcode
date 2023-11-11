from tools import make_cmapped_int_matrix, get_input


START_ROW = get_input(18, 2016)[0]

def propagate_row(row: str) -> str:
    new_row = []

    if row[:2] in ['.^', '^^']:
        new_row += ['^']
    else:
        new_row += ['.']


    for k in range(1, len(row) - 1):
        if row[k-1:k+2] in ['^..', '..^','^^.','.^^']:
            new_row += ['^']
        else:
            new_row += ['.']

    if row[-2:] in ['^.', '^^']:
        new_row += '^'
    else:
        new_row += ['.']

    return ''.join(new_row)

if __name__ == '__main__':
    rows = [START_ROW]
    for k in range(39):
        rows += [propagate_row(rows[-1])]

    total = sum([r.count('.') for r in rows])

    print(total)

    from tqdm import trange
    total = START_ROW.count('.')
    row = START_ROW
    for kk in trange(400000-1):
        row = propagate_row(row)
        total += row.count('.')
    
    print(total)
