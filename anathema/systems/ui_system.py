from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.abstracts import AbstractSystem

if TYPE_CHECKING:
    from anathema.core import Game


class UISystem(AbstractSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.terminal = game.renderer.terminal
        self.ui = game.ui

    def make_main_menu(self) -> None:
        self.ui.root.split_once(horizontal=True, position=64)
        self.ui.update_node_tree()
        self.ui.make_panel()

    def update(self, dt) -> None:
        for panel in self.ui.panels:
            self.game.renderer.push_to_stack(panel.draw)
