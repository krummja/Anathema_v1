from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from anathema.screens.player_ready import PlayerReady
from anathema.utils.config import Config

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class MenuConfig(Config):

    @property
    def position(self) -> Tuple[int, int]:
        return self.get_property('POSITION')

    @property
    def size(self) -> Tuple[int, int]:
        return self.get_property('SIZE')

    @property
    def title(self) -> str:
        return self.get_property('TITLE')


class MenuOverlay(PlayerReady):
    """Extensible base screen for creating menus."""

    name: str = ""

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self._data = None
        self._selection = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value) -> None:
        self._data = value

    @property
    def selection(self) -> int:
        return int(self._selection)

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = min(max(0, value), len(self.data) - 1)

    def on_draw(self, dt) -> None:
        super().on_draw(dt)
        self.draw_frame()
        self.draw_contents()

    def draw_frame(self) -> None:
        pass

    def draw_contents(self) -> None:
        pass

    def cmd_escape(self) -> None:
        self.game.screens.pop_screen()
