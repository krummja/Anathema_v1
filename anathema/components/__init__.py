from anathema.components.actor import Actor
from anathema.components.background import Background
from anathema.components.blocker import Blocker
from anathema.components.health import Health
from anathema.components.isplayer import IsPlayer
from anathema.components.legs import Legs
from anathema.components.name import Name
from anathema.components.opaque import Opaque
from anathema.components.portal import Portal
from anathema.components.position import Position
from anathema.components.renderable import Renderable
from anathema.components.unformed import Unformed
from anathema.components.mana import Mana
from anathema.components.stamina import Stamina

def all_components():
    return [
        Actor,
        Background,
        Blocker,
        Health,
        IsPlayer,
        Legs,
        Name,
        Opaque,
        Portal,
        Position,
        Renderable,
        Unformed,
        Mana,
        Stamina,
        ]
