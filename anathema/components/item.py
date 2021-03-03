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
        instigator = evt.data.require['instigator']
        self.take(instigator)
        evt.handle()
