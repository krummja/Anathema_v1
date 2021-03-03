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
        for i, d in enumerate(data_source):
            menu_opts = d.fire_event('get_interactions',
                                     EventData(success = True,
                                               require = {'target': d},
                                               expect  = {'interactions': []}))

            self[i] = { 'name': d['Noun'].noun_text,
                        'menu_opts': menu_opts }


class InventoryMenu(MenuOverlay):

    name: str = "INVENTORY"

    def on_enter(self) -> None:
        self.menu = MenuList(33, 1, 32, 48, " Inventory ", MenuData(self.game.player.entity['Inventory'].contents))

    def on_draw(self, dt) -> None:
        self.menu.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.menu.selector.selection += y

    def cmd_confirm(self) -> None:
        menu_opts = self.menu.select()
        print(menu_opts.data)
        # raise a menu to select opts

    def cmd_pickup(self) -> None:
        pass
