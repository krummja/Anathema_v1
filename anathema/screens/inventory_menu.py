from __future__ import annotations
from typing import TYPE_CHECKING
from collections import defaultdict

from anathema.utils.math_utils import clamp
from anathema.screens.menu_overlay import MenuOverlay

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class Selector:

    def __init__(self, data) -> None:
        self.data = data
        self._selection = 0

    @property
    def selection(self) -> int:
        return int(self._selection)

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = clamp(value, 0, len(self.data) - 1)


class MenuData(defaultdict):

    def __init__(self) -> None:
        self['name'] = ''
        self['data'] = None


class TestData(defaultdict):

    def __init__(self) -> None:
        self[0] = "Data 1"
        self[1] = "Data 2"
        self[2] = "Data 3"
        self[3] = "Data 4"


class InventoryMenu(MenuOverlay):

    name: str = "INVENTORY"
    data = TestData()
    selector = Selector(data)

    def on_enter(self) -> None:
        pass

    def on_draw(self, dt) -> None:
        self.manager.game.renderer.draw_box(33, 1, 32, 48, 0x44FFFFFF)
        self.draw_data(38, 3)
        super().on_draw(dt)

    def draw_data(self, x: int, y: int) -> None:
        selected = 0xFFFF00FF
        unselected = 0xFFFFFFFF
        for i in range(0, len(self.data) * 2, 2):
            self.manager.game.renderer.print(x, y+i, unselected, self.data[i//2])
            if self.selector.selection == i//2:
                self.manager.game.renderer.print(x - 3, y+i, selected, ">")
                self.manager.game.renderer.print(x, y+i, selected, self.data[self.selector.selection])

    def cmd_move(self, x: int, y: int) -> None:
        self.selector.selection += y

    def cmd_confirm(self) -> None:
        item = self.data[self.selector.selection]
        print(item)

    def cmd_pickup(self) -> None:
        pass
