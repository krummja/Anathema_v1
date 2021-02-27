from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anathema.core import Game

class UISystem:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.ecs = self.game.ui.engine
        self._query = self.ecs.create_query(
            all_of=[' Position, Dimensions '])

    def draw_elements(self, dt) -> None:
        for element in self._query.result:
            x, y = element['Position']

    def update(self, dt) -> bool:
        menu_items = self._query.result
