from .actor import Actor
from .isplayer import IsPlayer
from .legs import Legs
from .position import Position
from .renderable import Renderable


def all_components():
    return [
        Actor,
        IsPlayer,
        Legs,
        Position,
        Renderable,
    ]
