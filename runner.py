'''
    Any year Runner
'''
from __future__ import annotations

import typing as typ

import os
import importlib
import click

import tools
import template

@click.command('runner')
@click.argument('year', type=click.IntRange(15,24))
@click.argument('day', type=click.IntRange(1,25))
def main(year: int, day: int, real: bool = True, p1_only: bool = False) -> None:

    if not os.path.isfile(f'y20{year}/day{day}.py'):
        raise FileNotFoundError(f'y20{year}/day{day}.py')
    
    mod = importlib.import_module(f'y20{year}.day{day}')
    mod = importlib.reload(mod)

    Day: template.Day = mod.Day
    

    # if more samples, run more samples

    if mod.SAMPLE is not None:
        sample_input = Day.parse_input(mod.SAMPLE)
        t = Day(sample_input, True)
        print(f'Test p1: {t.solve1()}')

    if len(mod.ADDITIONAL_SAMPLES) > 0:
        for sample in mod.ADDITIONAL_SAMPLES:
            tt = Day(Day.parse_input(sample), True)
            print(f'Additional test p1: {tt.solve1()}')


    real_input = Day.parse_input(tools.get_input(day, 2000 + year))
    r = Day(real_input, False)
    print(f'Real p1: {r.solve1()}')

    if hasattr(mod, 'SAMPLE_P2'): # Sample is invalid for P2 and another is provided.
        t = Day(Day.parse_input(mod.SAMPLE_P2))
        print(f'Test p2: {t.solve2()}')
    elif mod.SAMPLE is not None:
        print(f'Test p2: {t.solve2()}')

    print(f'Real p2: {r.solve2()}')

    globals().update(locals())

if __name__ == '__main__':
    main()



