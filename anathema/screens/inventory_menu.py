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
    menus = []

    @property
    def active(self):
        return self.menus[-1]

    def push_menu(self, menu):
        self.menus.append(menu)

    def pop_menu(self):
        self.menus.pop()

    def on_enter(self) -> None:
        data = self.game.player.entity['Inventory'].contents
        menu = MenuList(33, 1, 32, 48, " Inventory ", MenuData(data))
        self.push_menu(menu)

    def on_draw(self, dt) -> None:
        self.active.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.active.selector.selection += y

    def cmd_confirm(self) -> None:
        selection = self.active.select()
        evt = selection.fire_event('get_interactions',
                                   {'expect': []})
        options = MenuList(33, 1, 32, 48, " Test ", MenuData(evt.data))
        self.push_menu(options)

    def cmd_pickup(self) -> None:
        pass
