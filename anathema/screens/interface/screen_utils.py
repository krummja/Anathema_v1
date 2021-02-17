from __future__ import annotations

import tcod
from anathema.core.options import Options


class UIManager:

    def __init__(self) -> None:
        self.panel_tree = tcod.bsp.BSP(
            x=0,
            y=0,
            width=Options.SCREEN_WIDTH,
            height=Options.SCREEN_HEIGHT
            )

    def split_vertical(self, position: int) -> None:
        self.panel_tree.split_once(horizontal=False, position=position)

    def split_horizontal(self, position: int) -> None:
        self.panel_tree.split_once(horizontal=True, position=position)
