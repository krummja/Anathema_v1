from __future__ import annotations

from ecstremity import Component


class Item(Component):
    """Flag component denoting an item."""

    def take(self, new_owner):
        if self.entity.has('Equippable'):
            slot = self.entity['Equippable'].body_part
            new_owner[slot].equip(self.entity)
            self.entity.add('IsInventoried', {'owner': new_owner})

    def on_lift(self, evt):
        instigator = evt.data['instigator']
        self.take(instigator)
        evt.handle()

    def on_try_drop(self, evt):
        if self.entity.has('IsInventoried'):
            owner = self.entity['IsInventoried'].owner
            owner['Inventory'].drop_from(self.entity)
            evt.handle()

    @staticmethod
    def on_get_info(evt):
        pass

    @staticmethod
    def on_get_interactions(evt):
        evt.data['expect'].append({
            'name': 'Drop',
            'evt': 'try_drop'
            })
        evt.data['expect'].append({
            'name': 'Info',
            'evt': 'try_get_info'
            })

    def on_try_get_info(self, evt):
        self.entity.fire_event('get_info', {'expect': []})
