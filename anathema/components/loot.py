from __future__ import annotations
from typing import *
from ecstremity import Component

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

    def on_equipped(self, evt):
        pass

    def on_try_pickup(self, evt):
        pass

    def on_try_take(self, evt):
        pass
