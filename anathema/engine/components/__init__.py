from .actor import Actor
from .blocker import Blocker
from .brain import Brain
from .equipment_slot import EquipmentSlot
from .goal import Goal
from .isplayer import IsPlayer
from .legs import Legs
from .pathing import Pathing
from .position import Position
from .renderable import Renderable
from .stats import Stats
from .wandering import Wandering


def game_object_components():
    return [
        Actor,
        Blocker,
        Brain,
        EquipmentSlot,
        Goal,
        IsPlayer,
        Legs,
        Pathing,
        Position,
        Renderable,
        Stats,
        Wandering,
    ]
