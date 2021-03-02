from __future__ import annotations
from typing import List, TYPE_CHECKING
from collections import defaultdict

from anathema.data.actions.event_data import EventData
from anathema.screens.interface.menu_list import MenuList
from anathema.screens.menu_overlay import MenuOverlay

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuData(defaultdict):

    def __init__(self, data_source: List) -> None:
        self.data_source = data_source
        for i, d in enumerate(self.data_source):
            self[i] = d


class InventoryMenu(MenuOverlay):

    name: str = "INVENTORY"

    def on_enter(self) -> None:
        data = EventData(success = True,
                         require = {'instigator': self.manager.game.player.entity},
                         expect  = {'inventories': []})
        inventories = self.manager.game.player.entity.fire_event('try_get_inventories', data)
        self.menu = MenuList(33, 1, 32, 48, MenuData(inventories))

    def on_draw(self, dt) -> None:
        self.menu.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.menu.selector.selection += y

    def cmd_confirm(self) -> None:
        print(self.menu.select())

    def cmd_pickup(self) -> None:
        pass
