from __future__ import annotations

from ecstremity import Component


class Actor(Component):

    def __init__(self) -> None:
        self._energy: int = 0

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def has_energy(self) -> bool:
        return self._energy >= 0

    def on_energy_consumed(self, event) -> None:
        self.reduce_energy(event.data)

    def on_get_interactions(self, event):
        target = event.data[1][1]
        event = target.fire_event('get_interactions', [])
        interactions = event.data
        # self.entity.fire_event(interactions["evt"])
        for interaction in interactions:
            target.fire_event(interaction["evt"])

    def on_tick(self, event) -> None:
        self.add_energy(1)

    def add_energy(self, value: int) -> None:
        self._energy += value
        if self._energy >= 0:
            self._energy = 0

    def reduce_energy(self, value: int):
        self.add_energy(value * -1)

    def __lt__(self, other: Actor) -> bool:
        return self._energy < other._energy

    def __str__(self) -> str:
        return f"{self._energy}"
