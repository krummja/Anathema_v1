from anathema.components.actor import Actor
from anathema.components.blocker import Blocker
from anathema.components.isplayer import IsPlayer
from anathema.components.legs import Legs
from anathema.components.name import Name
from anathema.components.opaque import Opaque
from anathema.components.position import Position
from anathema.components.renderable import Renderable

def all_components():
    return [
        Actor,
        Blocker,
        IsPlayer,
        Legs,
        Name,
        Opaque,
        Position,
        Renderable,
        ]
