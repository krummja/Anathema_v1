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
    DEBUG: bool = False

    def __init__(self, manager: UIManager, dimensions: Rect) -> None:
        self.manager = manager
        self.dimensions = dimensions
        self.panel_id: int = 0
        self.focusable: bool = False
        self.in_focus: bool = False
        self.bordered: bool = False

        if self.manager.DEBUG:
            self.DEBUG = True

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
            if self.focusable and self.in_focus:
                terminal.color(0xFFFF00FF)
            else:
                terminal.color(0xFFFFFFFF)

            terminal.put(self.dimensions.left, self.dimensions.top, UIGlyphs.CORNER_TL)
            terminal.put(self.dimensions.right, self.dimensions.top, UIGlyphs.CORNER_TR)
            terminal.put(self.dimensions.left, self.dimensions.bottom, UIGlyphs.CORNER_BL)
            terminal.put(self.dimensions.right, self.dimensions.bottom, UIGlyphs.CORNER_BR)

            for x in range(self.dimensions.left+1, self.dimensions.right):
                terminal.put(x, self.dimensions.top, UIGlyphs.HORIZONTAL)
                terminal.put(x, self.dimensions.bottom, UIGlyphs.HORIZONTAL)

            for y in range(self.dimensions.top+1, self.dimensions.bottom):
                terminal.put(self.dimensions.left, y, UIGlyphs.VERTICAL)
                terminal.put(self.dimensions.right, y, UIGlyphs.VERTICAL)

    def __str__(self) -> str:
        return str(self.panel_id)


class UIManager(AbstractManager):

    DEBUG: bool = False

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

    def split(self, horizontal: bool = False, position: int = 0) -> None:
        self.root.split_once(horizontal=horizontal, position=48)
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

    def make_panels(self) -> None:
        panel_count = len(self.panels)
        node_count = len(self.leaves)

        for node in self.leaves:
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

    def make_panel(self, at: Tuple[int, int]) -> None:
        """Make a panel from the node that contains the provided coordinates."""
        node = self.root.find_node(*at)
        panel = Panel(
            manager=self,
            dimensions=Rect(
                Point(node.x, node.y),
                Size(node.width, node.height)
                ))
        self.panels.append(panel)
        panel.panel_id = len(self.panels)

    def gutters(self, width: int, layout: Optional[BSP] = None) -> BSP:
        if layout is not None:
            next = layout
        else:
            next = self.root
        next.split_once(horizontal=False, position=width)
        next = self.root.find_node(*CENTER)
        next.split_once(horizontal=False, position=(Options.SCREEN_WIDTH - width))
        next = self.root.find_node(*CENTER)
        self.update_node_tree()
        self.make_panel(at=CENTER)
        self.panels[0].bordered=True
        return next

    def letterbox(self, height: int, layout: Optional[BSP] = None) -> BSP:
        if layout is not None:
            next = layout
        else:
            next = self.root
        next.split_once(horizontal=True, position=height)
        next = self.root.find_node(*CENTER)
        next.split_once(horizontal=True, position=(Options.SCREEN_HEIGHT - height))
        next = self.root.find_node(*CENTER)
        self.update_node_tree()
        self.make_panel(at=CENTER)
        self.panels[0].bordered=True
        return next

    def side_panel(self, width: int, right: bool = True):
        position: int = width if not right else Options.SCREEN_WIDTH - width
        next = self.root
        next.split_once(horizontal=False, position=position)
        self.update_node_tree()

        at = (1, 1) if not right else (Options.SCREEN_WIDTH - 1, 1)
        self.make_panel(at=at)
        self.panels[0].bordered=True

    def layout_floating_modal(self):
        self.root.split_once(horizontal=False, position=16)
        next = self.root.find_node(48, 32)
        next.split_once(horizontal=False, position=80)
        next = self.root.find_node(48, 32)
        next.split_once(horizontal=True, position=16)
        next = self.root.find_node(48, 32)
        next.split_once(horizontal=True, position=48)
        self.update_node_tree()
        self.make_panels()

    def stage_view(self):
        self.root.split_once(horizontal=False, position=64)
        next = self.root.find_node(32, 1)
        next.split_once(horizontal=True, position=48)
        self.update_node_tree()
        self.make_panels()
        log_panel = self.panels[0]
        side_panel = self.panels[1]
        stage_panel = self.panels[2]

        log_panel.bordered = True
        side_panel.bordered = True
        return (stage_panel, log_panel, side_panel)

    def main_menu_view(self):
        pass
