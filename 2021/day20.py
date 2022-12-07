from tools import get_input
import numpy as np

SAMPLE = [
    '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#',
    '',
    '#..#.',
    '#....',
    '##..#',
    '..#..',
    '..###',
]

REAL = get_input(20, 2021)

def assemble_bits(mat33):
    acc = 0
    for b in mat33.flatten():
        acc *= 2
        acc += b
    return acc

class Day20:

    def __init__(self, lines, padding=20):
        self.code = lines[0].replace('.', '0').replace('#', '1')

        self.image = []
        for line in lines[2:]:
            l = line.replace('.', '0').replace('#', '1')
            self.image += [[int(c) for c in l]]
        self.image = np.asarray(self.image, np.int8)
        r, c = self.image.shape

        # Pad by a lot (because infinite might flip on and off)
        n = padding
        self.image = np.r_[np.zeros((n, c + 2*n), np.int8),
                           np.c_[np.zeros((r, n), np.int8), self.image,
                                 np.zeros((r, n), np.int8)],
                           np.zeros((n, c + 2*n), np.int8)]
        self.imr, self.imc = self.image.shape

    def enhance(self):
        newimage = self.image * 0
        for ii in range(1, self.imr-1):
            for jj in range(1,self.imc-1):
                bitcode = assemble_bits(self.image[ii-1:ii+2, jj-1:jj+2])
                newimage[ii,jj] = int(self.code[bitcode])

        self.image = newimage

    def solve1(self):
        self.enhance()
        self.enhance()
        return np.sum(self.image[3:-3, 3:-3])

    def solve2(self):
        # Ensure padding is at least... 102?
        from tqdm import trange
        for i in trange(50):
            self.enhance()
        return np.sum(self.image[51:-51, 51:-51])
        


if __name__ == "__main__":
    test = Day20(SAMPLE, 102)
    print(test.solve2())
    real = Day20(REAL, 102)
    #print(real.solve2())