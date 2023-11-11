from __future__ import annotations

from y2016.day23 import Interpreter

from tools import get_input

REAL = get_input(25, 2016)
REALWMUL = get_input(250, 2016)

if __name__ == '__main__':
    import time
    a = 175
    a = 8367
    i2 = Interpreter(REALWMUL.copy(), verbose=False)
    s = time.time()
    i2.regz['a'] = a
    print(i2.solve1(ipbreak=24), 1e3*(time.time() - s))

    # Engineering:
    # prints the bits of a + 2555
    # Add 2555 to input, puts it in b.
    # Then there's a loop using c that decrement b and c, resets c to 2 when hits 0
    # Inc a when c == 0 too, so one decrement of b out of 2
    # In the end, c = 1 or 0 dep the parity of original b
    # Then out statement wrapped to set b to 1 if c is 1, b to 0  if c is 2, and out that.

    # Once bits of a + 2555 depleted, start over
    # Ergo, bin(2555) = 0b100111111011
    # Next high alternating is 101010101010 = 2730
    # Remove 2555 = 175