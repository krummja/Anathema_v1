from anathema.components.actor import Actor
from anathema.components.isplayer import IsPlayer
from anathema.components.legs import Legs
from anathema.components.position import Position
from anathema.components.renderable import Renderable

def all_components():
    return [
        Actor,
        IsPlayer,
        Legs,
        Position,
        Renderable,
        ]
