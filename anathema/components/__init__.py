from .actor import Actor
from .blocker import Blocker
from .brain import Brain
from .container import Container
from .eyes import Eyes
from .isinteractable import IsInteractable
from .isinventoried import IsInventoried
from .isopaque import IsOpaque
from .isplayer import IsPlayer
from .legs import Legs
from .loot import Loot
from .position import Position
from .renderable import Renderable


def all_components():
    return [
        Actor,
        Blocker,
        Brain,
        Container,
        Eyes,
        IsInteractable,
        IsInventoried,
        IsOpaque,
        IsPlayer,
        Legs,
        Loot,
        Position,
        Renderable,
    ]


# from os import listdir, path
# import importlib
#
#
# def load_component_definitions():
#     modules = listdir(path.dirname(__file__))
#     for module in modules:
#         if module == '__init__.py' or module[-3:] != '.py':
#             continue
#         yield module[:-3]
#
#
# def initialize_class_from_module(module_name: str):
#     if module_name[0:2] == 'is':
#         class_name = 'Is' + module_name[2:].capitalize()
#     else:
#         class_name = module_name.capitalize()
#     module = importlib.import_module('components.' + module_name)
#     print(f"Loading Component {class_name}")
#     return module.__dict__.get(class_name)
#
#
# def all_components():
#     for component in load_component_definitions():
#         component_class = initialize_class_from_module(component)
#         yield component_class
