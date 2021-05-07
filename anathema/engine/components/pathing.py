from typing import *
from ecstremity import Component


class Pathing(Component):

    def __init__(self, dest_xy: Tuple[int, int]) -> None:
        self.dest_xy = dest_xy
        self._path = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
