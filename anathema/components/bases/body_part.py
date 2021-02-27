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
            return False
        self._dict[key] = item
        return True

    def __getitem__(self, key):
        return self._dict[key]

    def __str__(self) -> str:
        return str(self._dict)


class BodyPart(Component):

    _equip_slots = EquipSlots({
        'A': None,
        'B': None,
        'C': None
        })

    @property
    def equip_slots(self):
        return self._equip_slots

    @property
    def body(self) -> Body:
        return self._body

    @body.setter
    def body(self, value: Body) -> None:
        self._body = value

    def equip(self, item):
        slot = get_first_key(self._equip_slots._dict, None)
        if item.has('Equippable'):
            item['Equippable'].owner = self.entity
            self._equip_slots[slot] = item
