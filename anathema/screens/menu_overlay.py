from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.screens import PlayerReady

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuPanel:

    name: str = "inventory"
    padding_left: int = 4
    padding_right: int = 4
    padding_top: int = 2
    padding_bottom: int = 4

    def __init__(self, screen, x: int = 0, y: int = 0, w: int = 0, h: int = 0) -> None:
        self.screen = screen
        self.renderer = self.screen.game.renderer
        self.item_list = []

        self.w = w
        self.h = h
        self.x = x
        self.y = y

        self._active: bool = False
        self._focused: bool = False

    def draw(self) -> None:
        self.renderer.draw_box(self.x, self.y, self.w, self.h, 0x44FFFFFF)
        for i, item in enumerate(self.item_list):
            self.renderer.print(
                self.x + self.padding_left,
                self.y + self.padding_top + i,
                0xFFFFFFFF,
                item['name']
                )

    def activate(self, data):
        self.item_list.extend(data)
        self.w = self.compute_width()
        self.h = self.compute_height()
        self.x = self.compute_x()
        self.y = self.y
        self._active = True

    def clear(self):
        self.item_list.clear()

    def compute_width(self):
        if self.w == 0:
            return (self.padding_left +
                    max(len(x) for sublist in self.item_list for x in sublist) +
                    self.padding_right)
        else:
            return self.w

    def compute_height(self):
        if self.h == 0:
            return (self.padding_top +
                    len(self.item_list) +
                    self.padding_bottom)
        else:
            return self.h

    def compute_x(self):
        if self.x == 0:
            return 65 - self.w
        else:
            return self.x


class MenuOverlay(PlayerReady):

    name: str = "MENU OVERLAY"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self._menu_items = {
            'inventory': MenuPanel(self, 33, 1, 32, 48),
            'interactions': MenuPanel(self, y=1),
            }

    def on_enter(self, *args) -> None:
        super().on_enter()
        menu_item = args[0]
        menu_data = args[1]
        self._menu_items[menu_item].activate(menu_data)

    def on_leave(self) -> None:
        pass

    def on_draw(self, dt) -> None:
        super().on_draw(dt)
        for menu_item in self._menu_items.values():
            if menu_item._active:
                menu_item.draw()

    def cmd_escape(self) -> None:
        self.game.screens.pop_screen()

    def cmd_inventory(self):
        pass

    def cmd_move(self, x: int, y: int) -> None:
        pass
