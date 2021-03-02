from anathema.components.actor import Actor
from anathema.components.arms import Arms
from anathema.components.background import Background
from anathema.components.blocker import Blocker
from anathema.components.body import Body
from anathema.components.container import Container
from anathema.components.door import Door
from anathema.components.eyes import Eyes
from anathema.components.equippable import Equippable
from anathema.components.head import Head
from anathema.components.health import Health
from anathema.components.isinteractable import IsInteractable
from anathema.components.isplayer import IsPlayer
from anathema.components.isstatic import IsStatic
from anathema.components.item import Item
from anathema.components.legs import Legs
from anathema.components.back import Back
from anathema.components.hands import Hands
from anathema.components.feet import Feet
from anathema.components.mana import Mana
from anathema.components.noun import Noun
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
        Equippable,
        Head,
        Health,
        Item,
        IsInteractable,
        IsInventoried,
        IsPlayer,
        IsStatic,
        Legs,
        Back,
        Hands,
        Feet,
        Mana,
        Noun,
        Opacity,
        Portal,
        Position,
        Renderable,
        Stamina,
        Torso,
        Unformed,
        ]
