from __future__ import annotations

from collections import defaultdict

from anathema.screens.interface.menu_list import MenuList
from anathema.screens.menu_overlay import MenuOverlay


class MenuData(defaultdict):
    def __init__(self, data_source) -> None:
        super().__init__()
        for i, d in enumerate(data_source):
            self[i] = d


class ItemOptions(MenuOverlay):
    name: str = "ITEM OPTIONS"
    menu: MenuList

    def on_enter(self, data) -> None:
        self.menu = MenuList(33, 1, 32, 48, "  ", MenuData(data))

    def on_draw(self, dt) -> None:
        self.menu.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        pass

    def cmd_confirm(self) -> None:
        pass
