from tools import get_input

SAMPLE = [
    '$ cd /',
    '14848514 b.txt',
    '8504156 c.dat',
    '$ cd a',
    '29116 f',
    '2557 g',
    '62596 h.lst',
    '$ cd e',
    '584 i',
    '$ cd ..',
    '$ cd ..',
    '$ cd d',
    '4060174 j',
    '8033020 d.log',
    '5626152 d.ext',
    '7214296 k',
]

REAL = get_input(7, 2022)

class Dir:
    def __init__(self, name, parent) -> None:
        self.name = name
        self.subdirs = []
        self.fnames = []
        self.fsizes = []

        self.parent = parent
    def mkdir(self, name):
        d = Dir(name, self)
        self.subdirs += [d]
        return d

    def touch(self, name, size):
        self.fnames += [name]
        self.fsizes += [size]

    def processcommands(self, commands):
        while len(commands) > 0:
            cmd = commands.pop(0)
            clist = cmd.split()
            if clist[1] == 'cd':
                if clist[2] == '..':
                    return commands
                elif clist[2] == '/' and self.name != '/':
                    return [cmd] + commands
                else:
                    if clist[2] in [s.name for s in self.subdirs]:
                        print(f'WARNING @ {clist[2]}')
                    d = self.mkdir(clist[2])
                    commands = d.processcommands(commands)
            elif clist[1] == 'ls':
                pass
            elif clist[0] != 'dir':
                self.touch(clist[1], int(clist[0]))

        return commands

    def __str__(self):
        s = f'{self.name}\t\t\t{self.size()}\n'
        for sf in range(len(self.fsizes)):
            s += f'  {self.fnames[sf]}  {self.fsizes[sf]}\n'
        for sd in self.subdirs:
            s += '  ' + '\n  '.join(sd.__str__().rstrip().split('\n')) + '\n'
        return s


    def size(self):
        tot = 0
        tot += sum(self.fsizes)
        tot += sum([s.size() for s in self.subdirs])
        return tot

    def size_and_subsizes(self):
        tot = [(self.name, self.size())]
        for s in self.subdirs:
            tot += s.size_and_subsizes()

        return tot

def solve1(dir):
    allsizes = dir.size_and_subsizes()
    return sum([a[1] for a in allsizes if a[1] <= 100000])

FSSIZE = 70000000
NEEDED = 30000000

def solve2(dir):
    available = FSSIZE - dir.size()
    needed = NEEDED - available
    allsizes = dir.size_and_subsizes()
    return min([a[1] for a in allsizes if a[1] > needed])

if __name__ == "__main__":
    d = Dir('/', None)
    d.processcommands(REAL)
    print(solve1(d))
    print(solve2(d))

