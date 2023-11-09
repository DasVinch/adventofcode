import typing as typ

STATE = '10011111011011001'
LEN = 272

def flipchar(c: str):
    return '1' if c == '0' else '0'

def expand(t: list[str]):
    return t + ['0'] + [flipchar(c) for c in t[::-1]]

def contract(t: list[str]):
    checksum: list[str] = []
    for k in range(0, len(t), 2):
        if t[k] == t[k+1]:
            checksum += ['1']
        else:
            checksum += ['0']

    return checksum


def solve(seed: str, length: int):
    lseed = list(seed)
    while len(lseed) <= length:
        lseed = expand(lseed)

    lseed = lseed[:length]

    while len(lseed) % 2 == 0:
        lseed = contract(lseed)

    return ''.join(lseed)

if __name__ == '__main__':
    print(
        solve(STATE, LEN)
    )

    print(
        solve(STATE, 35651584)
    )
