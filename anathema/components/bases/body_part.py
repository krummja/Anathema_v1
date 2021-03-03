from __future__ import annotations

from ecstremity import Component
from anathema.utils.data_utils import get_first_key

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anathema.components.body import Body


class EquipSlots:

    def __init__(self, dictionary) -> None:
        self._dict = dictionary

    def __setitem__(self, key, item):
        if key not in self._dict:
            pass
        self._dict[key] = item

    def __getitem__(self, key):
        if key not in self._dict:
            pass
        return self._dict[key]

    def __str__(self) -> str:
        return str(self._dict)


class BodyPart(Component):

    _equipped = None

    @property
    def equipped(self):
        return self._equipped

    @property
    def equipped_name(self):
        if self._equipped is not None:
            return self._equipped['Noun'].noun_text
        return None

    @property
    def body(self) -> Body:
        return self._body

    @body.setter
    def body(self, value: Body) -> None:
        self._body = value

    def equip(self, item):
        if item.has('Equippable'):
            item['Equippable'].owner = self.entity
            self._equipped = item

    def on_try_get_equipped(self, evt):
        evt.data.expect['equipped'].append({
            "name": self.equipped_name,
            "uid": self._equipped.uid,
            "evt": "get_equipment_opts"
            })
        return evt

    def on_try_get_inventories(self, evt):
        if self._equipped and self._equipped.has('Container'):
            evt.data.expect['inventories'].append({
                "name": self.equipped_name,
                "uid": self._equipped.uid,
                "evt": "get_inventories"
                })
            # evt.data.expect['inventories'].append({
            #     self.equipped_name: self._equipped['Container']
            #     })
            # return evt
