from .actor import Actor
from .blocker import Blocker
from .brain import Brain
from .equipment_slot import EquipmentSlot
from .goal import Goal
from .isplayer import IsPlayer
from .legs import Legs
from .position import Position
from .renderable import Renderable
from .wandering import Wandering
from .pathing import Pathing


def all_components():
    return [
        Actor,
        Blocker,
        Brain,
        EquipmentSlot,
        Goal,
        IsPlayer,
        Legs,
        Position,
        Renderable,
        Wandering,
        Pathing,
    ]
