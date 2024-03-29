from .actor import Actor
from .blocker import Blocker
from .brain import Brain
from .equipment_slot import EquipmentSlot
from .eyes import Eyes
from .goal import Goal
from .isplayer import IsPlayer
from .legs import Legs
from .moniker import Moniker
from .pathing import Pathing
from .position import Position
from .renderable import Renderable
from .species import Species
from .stats import Stats
from .wandering import Wandering


def game_object_components():
    return [
        Actor,
        Blocker,
        Brain,
        EquipmentSlot,
        Eyes,
        Goal,
        IsPlayer,
        Legs,
        Moniker,
        Pathing,
        Position,
        Renderable,
        Stats,
        Species,
        Wandering,
    ]
