from __future__ import annotations
from typing import *
from ecstremity import Component

from ecstremity.entity_event import EventData

if TYPE_CHECKING:
    from ecstremity.entity_event import EntityEvent


class Loot(Component):

    def take(self, new_owner):
        if self.entity.has('IsInventoried'):
            if self.entity['IsInventoried'].owner == new_owner:
                return True
            owner = self.entity['IsInventoried'].owner
            owner['Inventory'].remove_loot(self.entity)
        new_owner['Inventory'].add_loot(self.entity)
        return True

    def on_get_interactions(self, evt: EntityEvent):
        instigator = evt.data.instigator
        is_inventoried = self.entity.has('IsInventoried')
        if not instigator.has('Inventory'):
            return

        if is_inventoried:
            if instigator['Inventory'].has_loot(self.entity):
                evt.data.interactions.append({
                    'name': 'Drop',
                    'evt': 'try_drop'
                    })
            else:
                evt.data.interactions.append({
                    'name': 'Take',
                    'evt': 'try_take'
                    })
        else:
            evt.data.interactions.append({
                'name': 'Pick Up',
                'evt': 'try_pick_up'
                })

    def on_equipped(self, evt: EntityEvent):
        if not evt.data.instigator.has('Inventory'):
            return
        if evt.data.instigator['Inventory'].has_loot(self.entity):
            return
        evt.data.instigator['Inventory'].add_loot(self.entity)

    def on_try_pickup(self, evt: EntityEvent):
        self.take(evt.data.instigator)
        evt.data.instigator.fire_event('energy_consumed', EventData(cost=100))
        evt.handle()

    def on_try_take(self, evt: EntityEvent):
        self.take(evt.data.instigator)
        evt.data.instigator.fire_event('energy_consumed', EventData(cost=100))
        evt.handle()
