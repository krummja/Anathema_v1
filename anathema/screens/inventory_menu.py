from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.screens import MenuOverlay

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager


class InventoryMenu(MenuOverlay):

    name: str = "INVENTORY"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)

    def on_draw(self, dt) -> None:
        pass
