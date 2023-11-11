import numpy as np
from tools import get_input

INPUT = get_input(19, 2021)
SHORTERINPUT = get_input(190, 2021)

BIN3BIT = np.zeros((8, 3), np.float32)
BIN3BIT[4:, 0] = 1.0
BIN3BIT[2:4, 1] = 1.0
BIN3BIT[6:, 1] = 1.0
BIN3BIT[1::2, 2] = 1.0
BIN3BIT = BIN3BIT * 2 - 1

ROTMATS = [
    np.eye(3),
    np.array([[0., 1, 0], [0, 0, 1], [1, 0, 0]]),
    np.array([[0., 0, 1], [1, 0, 0], [0, 1, 0]]),
    np.array([[1., 0, 0], [0, 0, 1], [0, 1, 0]]),
    np.array([[0., 0, 1], [0, 1, 0], [1, 0, 0]]),
    np.array([[0., 1, 0], [1, 0, 0], [0, 0, 1]])
]

ISOMCUBE = []
for bits in BIN3BIT:
    for mat in ROTMATS:
        m = bits[:, None] * mat
        if np.linalg.det(m) == 1:
            ISOMCUBE.append(m)


class Day19:

    def __init__(self, lines) -> None:
        self.scanners = []
        currentscanner = []
        for l in lines:
            if l.startswith('---'):
                continue
            elif l == '':
                self.scanners.append(currentscanner)
                currentscanner = []
            else:
                currentscanner.append([int(i) for i in l.split(',')])
        self.scanners.append(currentscanner)

        self.scanners = [np.asarray(sc) for sc in self.scanners]

        self.sc_coords = np.zeros((len(self.scanners), 3), np.int32)

    def solve1(self):
        test = []
        hashers = {}

        nscans = len(self.scanners)

        sureQueue = [0]
        scannerQueue = [0]

        while len(scannerQueue) > 0:
            scidx = scannerQueue.pop()
            for j in range(nscans):
                if j in sureQueue:
                    continue

                for k in range(24):
                    mat = ISOMCUBE[k]
                    dist = self.scanners[scidx][:, None, :] - (
                        self.scanners[j] @ mat)[None, :, :]
                    dist = dist.astype(np.int32)
                    test += [dist]
                    hasher = {}
                    for v in dist.reshape(dist.shape[0] * dist.shape[1], 3):
                        t = tuple(v)
                        hasher[t] = hasher.get(t, 0) + 1
                    M = 0
                    V = None
                    for p in hasher:
                        if hasher[p] > M:
                            M = hasher[p]
                            V = p
                    if M >= 12:
                        # Rotate
                        self.scanners[j] = (self.scanners[j] @ mat).astype(
                            np.int32)
                        self.scanners[j] += np.asarray(V)[None, :]
                        self.sc_coords[j] = np.asarray(V)
                        # Queue
                        sureQueue.append(j)
                        scannerQueue.append(j)

                        print(f'Scanner #{j} against #{scidx}, rotation {k}.')

                        break

        # Done realigning the scanners!
        self.all_beacons = set()
        for k in range(nscans):
            for bcn in self.scanners[k]:
                self.all_beacons.add(tuple(bcn))

        return len(self.all_beacons)

    def solve2(self):
        nbcns = len(self.all_beacons)
        return np.max(
            np.sum(np.abs(self.sc_coords[None, :, :] -
                          self.sc_coords[:, None, :]),
                   axis=2))


if __name__ == "__main__":
    d = Day19(INPUT)
    #d = Day19(SHORTERINPUT)
    print(d.solve1())
    print(d.solve2())