from __future__ import annotations

from ecstremity import Component


class IsInventoried(Component):
    """Flag component denoting an item that has been placed in an inventory."""

    def __init__(self, owner) -> None:
        self.owner = owner

    def is_owned_by(self, entity):
        return self.owner and self.owner.uid == entity.uid

    def on_query_ownership(self, evt):
        evt.data.expect['owners'].append(self.entity)
