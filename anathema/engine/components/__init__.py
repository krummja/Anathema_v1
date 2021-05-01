from .actor import Actor
from .equipment_slot import EquipmentSlot
from .isplayer import IsPlayer
from .legs import Legs
from .position import Position
from .renderable import Renderable


def all_components():
    return [
        Actor,
        EquipmentSlot,
        IsPlayer,
        Legs,
        Position,
        Renderable,
    ]
