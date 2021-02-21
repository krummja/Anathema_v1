from __future__ import annotations
import enum
from typing import TYPE_CHECKING, Tuple, Optional
from enum import Enum

from collections import deque

import tcod
from anathema.abstracts import AbstractManager
from anathema.core.options import Options
from anathema.utils.geometry import Rect, Point, Size

if TYPE_CHECKING:
    from tcod.bsp import BSP
    from anathema.core.game import Game

CENTER = (Options.SCREEN_WIDTH // 2, Options.SCREEN_HEIGHT // 2)
HORIZONTAL = {'horizontal': True, 'position': Options.SCREEN_HEIGHT//2}
VERTICAL = {'horizontal': False, 'position': Options.SCREEN_WIDTH//2}


class UIGlyphs:
    CORNER_TL = "┌"
    CORNER_TR = "┐"
    CORNER_BL = "└"
    CORNER_BR = "┘"
    HORIZONTAL = "─"
    HORIZONTAL_2 = "═"
    VERTICAL = "│"

class Side(Enum):
    LEFT = 0
    RIGHT = 1


class Panel:

    NAME: str = ""

    def __init__(self, manager: UIManager, dimensions: Rect) -> None:
        self.manager = manager
        self.dimensions = dimensions
        self.panel_id: int = 0
        self.focusable: bool = False
        self.in_focus: bool = False
        self.bordered: bool = True

    def on_draw(self, dt) -> None:
        terminal = self.manager.game.renderer.terminal
        terminal.layer(100)
        terminal.clear_area(
            self.dimensions.left,
            self.dimensions.top,
            self.dimensions.width,
            self.dimensions.height
            )

        if self.bordered:
            if self.focusable and self.in_focus:
                terminal.color(0xFFFF00FF)
            else:
                terminal.color(0xFFFFFFFF)

            for x in range(self.dimensions.left+1, self.dimensions.right):
                terminal.put(x, self.dimensions.top, UIGlyphs.HORIZONTAL)
                terminal.put(x, self.dimensions.bottom, UIGlyphs.HORIZONTAL)

            for y in range(self.dimensions.top+1, self.dimensions.bottom):
                terminal.put(self.dimensions.left, y, UIGlyphs.VERTICAL)
                terminal.put(self.dimensions.right, y, UIGlyphs.VERTICAL)

            terminal.put(self.dimensions.right, self.dimensions.top, UIGlyphs.CORNER_TR)
            terminal.put(self.dimensions.left, self.dimensions.top, UIGlyphs.CORNER_TL)
            terminal.put(self.dimensions.right, self.dimensions.bottom, UIGlyphs.CORNER_BR)
            terminal.put(self.dimensions.left, self.dimensions.bottom, UIGlyphs.CORNER_BL)

    def __str__(self) -> str:
        return str(self.panel_id)


class UIManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.root = tcod.bsp.BSP(
            x=0,
            y=0,
            width=Options.SCREEN_WIDTH,
            height=Options.SCREEN_HEIGHT
            )
        self.branches = []
        self.leaves = []
        self.panels = deque([])
        self._current_panel = None

    def next_panel(self):
        if self._current_panel is None:
            self._current_panel = self.panels[0]
            self._current_panel.in_focus = True
        self._current_panel.in_focus = False
        self._current_panel = self.panels.popleft()
        self._current_panel.in_focus = True
        self.panels.append(self._current_panel)

    def make_node(self, horizontal: bool, position: int) -> None:
        self.root.split_once(horizontal=horizontal, position=position)
        self.update_node_tree()

    def update_node_tree(self) -> None:
        self.leaves.clear()
        self.branches.clear()
        self.panels.clear()
        for node in self.root.pre_order():
            if node.children:
                self.branches.append(node.children)
            else:
                self.leaves.append(node)

    def make_panel(self, at: Tuple[int, int]) -> Panel:
        """Make a panel from the node that contains the provided coordinates."""
        node = self.root.find_node(*at)
        panel = Panel(
            manager=self,
            dimensions=Rect(
                Point(node.x, node.y),
                Size(node.width, node.height)
                ))
        panel.panel_id = len(self.panels)
        return panel

    def update(self, dt) -> None:
        pass
