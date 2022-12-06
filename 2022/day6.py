from tools import get_input

A = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
B = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
C = 'nppdvjthqldpwncqszvftbrmjlhg'
D = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
E = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
F = get_input(6, 2022)[0]

def findstart(s):
    for k in range(3, len(s)):
        if len(set(s[k-3:k+1])) == 4:
            return k+1

def findstartmess(s):
    for k in range(13, len(s)):
        if len(set(s[k-13:k+1])) == 14:
            return k+1


if __name__ == "__main__":
    assert(findstart(A) == 7)
    assert(findstart(B) == 5)
    assert(findstart(C) == 6)
    assert(findstart(D) == 10)
    assert(findstart(E) == 11)
    print(findstart(F))
    assert(findstartmess(A) == 19)
    assert(findstartmess(B) == 23)
    assert(findstartmess(C) == 23)
    assert(findstartmess(D) == 29)
    assert(findstartmess(E) == 26)
    print(findstartmess(F))