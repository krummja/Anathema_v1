from __future__ import annotations
from typing import List
from collections import defaultdict

from anathema.data.actions.event_data import EventData
from anathema.screens.interface.menu_list import MenuList
from anathema.screens.menu_overlay import MenuOverlay


class MenuData(defaultdict):

    def __init__(self, data_source: List) -> None:
        super().__init__()
        for i, d in enumerate(data_source):
            self[i] = d


class EquipmentMenu(MenuOverlay):

    name: str = "EQUIPMENT"

    def on_enter(self) -> None:
        data = EventData(success = True,
                         require = {'instigator': self.manager.game.player.entity},
                         expect  = {'equipped': []})
        evt = self.manager.game.player.entity.fire_event('try_get_equipped', data)
        self.menu = MenuList(33, 1, 32, 48, " Equipped ", MenuData(evt.data.expect['equipped']))

    def on_draw(self, dt) -> None:
        self.menu.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.menu.selector.selection += y

    def cmd_confirm(self) -> None:
        print(self.menu.select())

    def cmd_pickup(self) -> None:
        pass
