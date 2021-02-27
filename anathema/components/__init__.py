from anathema.components.actor import Actor
from anathema.components.arms import Arms
from anathema.components.background import Background
from anathema.components.blocker import Blocker
from anathema.components.body import Body
from anathema.components.container import Container
from anathema.components.door import Door
from anathema.components.eyes import Eyes
from anathema.components.head import Head
from anathema.components.health import Health
from anathema.components.isinteractable import IsInteractable
from anathema.components.isplayer import IsPlayer
from anathema.components.isstatic import IsStatic
from anathema.components.item import Item
from anathema.components.legs import Legs
from anathema.components.mana import Mana
from anathema.components.name import Name
from anathema.components.opacity import Opacity
from anathema.components.portal import Portal
from anathema.components.position import Position
from anathema.components.renderable import Renderable
from anathema.components.stamina import Stamina
from anathema.components.torso import Torso
from anathema.components.unformed import Unformed
from anathema.components.isinventoried import IsInventoried


def all_components():
    return [
        Actor,
        Arms,
        Background,
        Blocker,
        Body,
        Container,
        Door,
        Eyes,
        Head,
        Health,
        Item,
        IsInteractable,
        IsInventoried,
        IsPlayer,
        IsStatic,
        Legs,
        Mana,
        Name,
        Opacity,
        Portal,
        Position,
        Renderable,
        Stamina,
        Torso,
        Unformed,
        ]
