from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Actor(Component):

    def __init__(self) -> None:
        self._energy: int = 0

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def has_energy(self) -> bool:
        return self._energy >= 0

    def on_energy_consumed(self, evt: EntityEvent) -> None:
        self.reduce_energy(evt.data)

    def on_try_get_interactions(self, evt: EntityEvent) -> None:
        """Attempt to interact with a target object."""

        target = evt.data['target']
        evt = target.fire_event('get_interactions', evt.data)
        interactions = evt.data['expect']
        print(interactions)
        if interactions:
            if len(interactions) == 1:
                interaction = interactions.pop()
                target.fire_event(interaction["evt"])
            else:
                #! Route to the UI
                pass

    def on_try_pickup(self, evt: EntityEvent) -> None:
        """Try to pick up a target object."""

        target = evt.data['target']
        self.entity['Inventory'].add_to(target)

    def on_try_get_equipped(self, evt: EntityEvent) -> None:
        self.fire_event('get_equipped', evt.data)

    def on_tick(self, evt: EntityEvent) -> None:
        self.add_energy(1)

    def add_energy(self, value: int) -> None:
        self._energy += value
        if self._energy >= 0:
            self._energy = 0

    def reduce_energy(self, value: int) -> None:
        self.add_energy(value * -1)

    def __lt__(self, other: Actor) -> bool:
        return self._energy < other._energy

    def __str__(self) -> str:
        return f"{self._energy}"
