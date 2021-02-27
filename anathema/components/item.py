from __future__ import annotations

from ecstremity import Component


class Item(Component):
    """Flag component denoting an item."""

    def on_lift(self, evt):
        item = self.entity.clone()
        instigator = evt.data.require['instigator']
        if item['Equippable']:
            slot = item['Equippable'].body_part
            instigator['Body'].equip(slot, item)

        print(instigator['Body'].torso._equip_slots)

        self.entity.destroy()
        print("You lift the item.")
        evt.handle()
