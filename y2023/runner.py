'''
    2023 Runner

    Usage:
        runner <n>
'''
from __future__ import annotations

import os
import importlib

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)

    n = int(args['<n>'])

    fold_2023 = os.path.dirname(__file__)
    if not os.path.isfile(f'{fold_2023}/day{n}.py'):
        raise FileNotFoundError(f'No can find day{n}.py')
    
    mod = importlib.import_module(f'y2023.day{n}')
    mod = importlib.reload(mod)


    t = mod.Day(mod.SAMPLE, debug=True)



