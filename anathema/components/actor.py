from __future__ import annotations

from typing import *

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Actor(Component):

    def __init__(self) -> None:
        self._energy: int = 0

    def __lt__(self, other: Actor) -> bool:
        return self._energy < other._energy

    def __str__(self) -> str:
        return f"{self._energy}"

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def has_energy(self) -> bool:
        return self._energy >= 0

    def on_energy_consumed(self, evt: EntityEvent) -> None:
        self.reduce_energy(int(evt.data.cost))

    def on_tick(self, evt: EntityEvent) -> None:
        self.add_energy(1)

    def add_energy(self, value: int) -> None:
        self._energy += value
        if self._energy >= 0:
            self._energy = 0

    def reduce_energy(self, value: int) -> None:
        self.add_energy(value * -1)
