from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from collections import deque

import tcod
from anathema.abstracts import AbstractManager
from anathema.core.options import Options
from anathema.utils.geometry import Rect, Point, Size

if TYPE_CHECKING:
    from anathema.core.game import Game


class UIGlyphs:
    CORNER_TL = "╒"
    CORNER_TR = "╕"
    CORNER_BL = "└"
    CORNER_BR = "┘"
    HORIZONTAL = "─"
    HORIZONTAL_2 = "═"
    VERTICAL = "│"


class Panel:

    DEBUG: bool = False

    def __init__(self, manager: UIManager, dimensions: Rect) -> None:
        self.manager = manager
        self.dimensions = dimensions
        self.panel_id: int = 0
        self.in_focus: bool = False
        self.bordered: bool = True

    def draw(self) -> None:
        terminal = self.manager.game.renderer.terminal
        terminal.layer(100)

        if self.DEBUG:
            terminal.put(self.dimensions.left+1, self.dimensions.top+1, str(self.panel_id))
            terminal.print(self.dimensions.left+5,
                           self.dimensions.top+1,
                           f"focused: {self.in_focus}")
            terminal.print(self.dimensions.left+1,
                           self.dimensions.top+3,
                           f"x: {self.dimensions.left}")
            terminal.print(self.dimensions.left+1,
                           self.dimensions.top+4,
                           f"y: {self.dimensions.top}")
            terminal.print(self.dimensions.left+1,
                           self.dimensions.top+5,
                           f"w: {self.dimensions.width}")
            terminal.print(self.dimensions.left+1,
                           self.dimensions.top+6,
                           f"h: {self.dimensions.height}")

        if self.bordered:
            if self.in_focus:
                terminal.color(0xFFFF00FF)
            else:
                terminal.color(0xFFFFFFFF)

            terminal.put(self.dimensions.left, self.dimensions.top, UIGlyphs.CORNER_TL)
            terminal.put(self.dimensions.right, self.dimensions.top, UIGlyphs.CORNER_TR)
            terminal.put(self.dimensions.left, self.dimensions.bottom, UIGlyphs.CORNER_BL)
            terminal.put(self.dimensions.right, self.dimensions.bottom, UIGlyphs.CORNER_BR)

            for x in range(self.dimensions.left+1, self.dimensions.right):
                terminal.put(x, self.dimensions.top, UIGlyphs.HORIZONTAL_2)
                terminal.put(x, self.dimensions.bottom, UIGlyphs.HORIZONTAL)

            for y in range(self.dimensions.top+1, self.dimensions.bottom):
                terminal.put(self.dimensions.left, y, UIGlyphs.VERTICAL)
                terminal.put(self.dimensions.right, y, UIGlyphs.VERTICAL)

    def __str__(self) -> str:
        return str(self.panel_id)


class UIManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.panel_tree = tcod.bsp.BSP(
            x=0,
            y=0,
            width=Options.SCREEN_WIDTH,
            height=Options.SCREEN_HEIGHT
            )
        self.branches = []
        self.nodes = []
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

    def split(self, horizontal: bool = False, position: int = 0) -> None:
        self.panel_tree.split_once(horizontal=horizontal, position=48)
        self.update_panel_tree()

    def update_panel_tree(self) -> None:
        self.nodes.clear()
        self.branches.clear()
        self.panels.clear()
        for node in self.panel_tree.pre_order():
            if node.children:
                self.branches.append(node.children)
            else:
                self.nodes.append(node)
        self.make_panels()

    def make_panels(self) -> None:
        panel_count = len(self.panels)
        node_count = len(self.nodes)

        for node in self.nodes:
            if panel_count < node_count:
                panel = Panel(
                    manager=self,
                    dimensions=Rect(
                        Point(node.x, node.y),
                        Size(node.width, node.height)
                        ))

                self.panels.append(panel)
                panel.panel_id = len(self.panels)

        self.next_panel()

    def update(self, dt) -> None:
        pass
