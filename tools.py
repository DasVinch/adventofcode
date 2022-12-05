from typing import List

def get_input(n: int) -> List[str]:
    with open(f"inputs/input{n}.txt", 'r') as f:
        l = f.readlines()
        l = [ll.rstrip() for ll in l]

    return l
