from __future__ import annotations

from ecstremity import Component


class Item(Component):
    """Flag component denoting an item."""

    def on_lift(self, evt):
        item = self.entity.clone()
        print(evt.data.require['instigator'])

        self.entity.destroy()
        print("You lift the item.")
        evt.handle()
