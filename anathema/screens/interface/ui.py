from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import EngineAdapter as Engine
from anathema.abstracts import AbstractManager
from anathema.screens.interface.components import all_components

if TYPE_CHECKING:
    from anathema.core.game import Game


class UIManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.engine = Engine(client=game)

        for component in all_components():
            self.engine.components.register(component)

    def create_menu(self, x: int, y: int, width: int, height: int):
        menu = self.engine.create_entity()
        menu.add('Position', {'x': x, 'y': y})
        menu.add('Dimensions', {'width': width, 'height': height})
        return menu.uid

    def apply_clamping(self, menu_uid, vertical, horizontal):
        menu = self.engine.get_entity(menu_uid)
        if menu.has('Position'):
            menu['Position'].vertical = vertical
            menu['Position'].horizontal = horizontal

    def make_listing(self, menu_uid, title, data):
        menu = self.engine.get_entity(menu_uid)
        menu.add('Title', {'text': title})
        menu.add('Listing', {'data': data})
        menu.add('Selector', {})
