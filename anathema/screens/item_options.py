from __future__ import annotations

from anathema.screens.interface.menu_list import MenuList
from anathema.screens.menu_overlay import MenuOverlay


class ItemOptions(MenuOverlay):
    name: str = "ITEM OPTIONS"
    menu: MenuList

