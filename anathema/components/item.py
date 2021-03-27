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

    def on_drop(self, evt):
        pass

    @staticmethod
    def on_get_interactions(evt):
        evt.data['expect'].append({
            'name': 'Drop',
            'evt': 'try_drop'
            })
        evt.data['expect'].append({
            'name': 'Info',
            'evt': 'get_info'
            })

    def on_get_info(self):
        pass
