from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.screens import PlayerReady

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuPanel:

    name: str = "inventory"

    def __init__(self, screen, x: int, y: int, w: int, h: int) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.renderer = self.screen.game.renderer

    def draw(self) -> None:
        self.renderer.draw_box(self.x, self.y, self.w, self.h, 0x44FFFFFF)


class MenuOverlay(PlayerReady):

    name: str = "MENU OVERLAY"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self._menu_items = {
            'inventory': MenuPanel(self, 33, 1, 32, 48)
            }
        self._menu_list = []

    def on_enter(self, *args) -> None:
        super().on_enter()
        for arg in args:
            self.push_menu(arg)

    def on_leave(self) -> None:
        self.clear_menus()

    def on_draw(self, dt) -> None:
        super().on_draw(dt)
        if len(self._menu_list) > 0:
            for menu_item in self._menu_list:
                menu_item.draw()

    def push_menu(self, menu_id) -> None:
        self._menu_list.append(self._menu_items[menu_id])

    def pop_menu(self) -> None:
        self._menu_list.pop()

    def clear_menus(self) -> None:
        self._menu_list.clear()

    def cmd_escape(self) -> None:
        self.game.screens.replace_screen("PLAYER READY")

    def cmd_inventory(self):
        pass

    def cmd_move(self, x: int, y: int) -> None:
        pass
