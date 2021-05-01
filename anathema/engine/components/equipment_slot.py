from __future__ import annotations
from typing import *

from ecstremity import Component
from anathema.engine.data.equipment_slot_type import *

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class EquipmentSlot(Component):

    def __init__(
            self,
            name: str,
            slot_type: str = EQ_SLOT_BODY,
            content: str = '<Entity>',
            is_primary: bool = False,
            default_weapon_type: str = None
        ) -> None:
        self.name = name
        self.slot_type = slot_type
        self.content = content
        self.is_primary = is_primary
        self.default_weapon_type = default_weapon_type
