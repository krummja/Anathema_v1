from __future__ import annotations
from collections import defaultdict

from anathema.screens.interface.menu_list import MenuList
from anathema.screens.menu_overlay import MenuOverlay


class MenuData(defaultdict):
    def __init__(self, data_source) -> None:
        super().__init__()
        for i, d in enumerate(data_source):
            self[i] = d


class InventoryMenu(MenuOverlay):
    name: str = "INVENTORY"
    menu: MenuList
    active = None

    def on_enter(self) -> None:
        data = self.game.player.entity['Inventory'].contents
        self.menu = MenuList(33, 1, 32, 48, " Inventory ", MenuData(data))
        self.active = self.menu

    def on_draw(self, dt) -> None:
        self.menu.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.active.selector.selection += y

    def cmd_confirm(self) -> None:
        selection = self.active.select()
        evt = selection.fire_event('get_interactions',
                                   {'expect': []})

    def cmd_pickup(self) -> None:
        pass
