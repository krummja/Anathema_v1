from __future__ import annotations
from typing import *
import logging

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Actor(Component):

    def __init__(self, energy: int = 0) -> None:
        self.energy: int = energy
        self._dest_xy = None
        self._path = None
        self._can_take_turn = False
        self._is_pathing = False

    def __lt__(self, other: Actor) -> bool:
        return self.energy < other.energy

    def __str__(self) -> str:
        return f"Energy: {self.energy}"

    @property
    def is_pathing(self):
        return self._is_pathing

    @property
    def dest_xy(self):
        return self._dest_xy

    @dest_xy.setter
    def dest_xy(self, value):
        self._dest_xy = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def can_take_turn(self):
        return self._can_take_turn

    @can_take_turn.setter
    def can_take_turn(self, value):
        self._can_take_turn = value

    @property
    def has_energy(self) -> bool:
        return self.energy >= 0

    def on_energy_consumed(self, evt: EntityEvent) -> None:
        self.reduce_energy(int(evt.data.cost))

    def on_tick(self, _: EntityEvent) -> None:
        self.add_energy(1)

    def add_energy(self, value: int) -> None:
        self.energy += value
        if self.energy >= 0:
            self.energy = 0

    def reduce_energy(self, value: int) -> None:
        self.add_energy(value * -1)
