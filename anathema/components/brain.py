from __future__ import annotations

from ecstremity import Component, EntityEvent, Entity, EventData

from anathema.screens.select_from import SelectFrom


class Brain(Component):

    def __init__(self):
        self._is_player = False

    def on_attached(self, entity):
        self._is_player = entity.has('IsPlayer')

    def on_try_interact(self, evt: EntityEvent):
        evt.data.instigator = self.entity
        evt.data.interactions = []

        target: Entity = self.client.interaction_system.get(*evt.data.target)
        routed_evt: EntityEvent = evt.route(new_event='get_interactions', target=target)
        routed_evt.handle()

        self._interact(target, routed_evt.data)

    def _interact(self, target, data: EventData) -> None:
        if len(data.interactions) == 1:
            interaction = data.interactions.pop()
            target.fire_event(interaction['event'], EventData(
                callback=(lambda func: func())
            ))
        else:
            self.client.push_screen(SelectFrom(data))
