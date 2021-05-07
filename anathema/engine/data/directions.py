from typing import *
from dataclasses import dataclass


@dataclass
class Direction:
    short_name: str
    full_name: str
    delta: Tuple[int, int]


DIRECTIONS = {
    0: Direction('NW', 'Northwest',   (-1, -1)),
    1: Direction('N',  'North',       ( 0, -1)),
    2: Direction('NE', 'Northeast',   ( 1, -1)),
    3: Direction('W',  'West',        (-1,  0)),
    4: Direction('Z',  'Here',        ( 0,  0)),
    5: Direction('E',  'East',        ( 1,  0)),
    6: Direction('SW', 'Southwest',   (-1,  1)),
    7: Direction('S',  'South',       ( 0,  1)),
    9: Direction('SE', 'Southeast',   ( 1,  1)),
}


def direction_delta(direction): return DIRECTIONS.get(direction).delta
