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

    def on_energy_consumed(self, evt) -> None:
        self.reduce_energy(evt.data)

    def on_try_get_interactions(self, evt):
        if evt.data.result:
            self.ecs.client.log.report(evt.data.result)

        target = evt.data.require['target']
        evt = target.fire_event('get_interactions', evt.data)
        interactions = evt.data.expect['interactions']

        if len(interactions) == 1:
            interaction = interactions.pop()
            target.fire_event(interaction["evt"])
        else:
            self.ecs.client.ui.data = interactions

    def on_try_pickup(self, evt):
        message = evt.data.result
        self.ecs.client.log.report(message)
        target = evt.data.require['target']
        target.fire_event('lift', evt.data)

    def on_try_get_equipped(self, evt):
        self.fire_event('get_equipped', evt.data)

    def on_try_get_inventories(self, evt):
        self.fire_event('get_inventories', evt.data)

    def on_tick(self, evt) -> None:
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
