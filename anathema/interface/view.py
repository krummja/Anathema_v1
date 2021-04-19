from __future__ import annotations
from typing import *
from morphism import *

from .layout import Layout
from .screen import Screen

if TYPE_CHECKING:
    pass


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class ViewTree:

    def __init__(
            self,
            view: View,
            layout: Optional[Layout] = None,
            subviews: List[View] = None
        ) -> None:
        self.view = view
        self._bounds = self.view.frame.with_origin(Point(0, 0))
        self._layout = layout if layout else Layout()
        self._superview: Optional[View] = None

        self.subviews = []
        self.add_subviews(subviews if subviews else [])
        self.needs_layout: bool = True

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect):
        if value.origin != Point(0, 0):
            raise ValueError("Bounds is always anchored at (0, 0)")
        if value == self._bounds:
            return
        self._bounds = value
        self.view.frame = self.view.frame.with_size(value.size)
        self.needs_layout = True

    @property
    def frame(self) -> Rect:
        return self.view.frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        if value == self.view.frame:
            return
        self.view.frame = value
        self.bounds = value.with_origin(Point(0, 0))
        self.needs_layout = True

    @property
    def superview(self) -> Optional[View]:
        try:
            return self._superview
        except AttributeError:
            return None

    @superview.setter
    def superview(self, value: View) -> None:
        self._superview = value

    def add_subviews(self, subviews: List[View]) -> None:
        for view in subviews:
            view.superview = self
        self.subviews.extend(subviews)

    def remove_subviews(self, subviews: List[View]) -> None:
        for view in subviews:
            view.superview = None
        self.subviews = [view for view in self.subviews if view not in subviews]

    def add_subview(self, subview: View) -> None:
        self.add_subviews([subview])

    def remove_subview(self, subview: View) -> None:
        self.remove_subviews([subview])

    def perform_layout(self):
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self):
        for view in self.subviews:
            view.tree.apply_springs_and_struts_in_superview()

    def apply_springs_and_struts_in_superview(self):
        pass


class ViewController:

    def __init__(self, view: View) -> None:
        self.view = view
        self.handler = None
        self.is_handler = False


class View:

    def __init__(
            self,
            screen: Optional[Screen] = None,
            frame: Optional[Rect] = None,
            clear: bool = False,
            layout: Optional[Layout] = None,
            subviews: List[View] = None
        ) -> None:
        self._screen = screen
        self._frame = frame if frame else ZERO_RECT
        self._clear = clear
        self.hidden: bool = False

        self.tree = ViewTree(self, layout, subviews)
        self.controller = ViewController(self)

    @property
    def console(self):
        """Root console."""
        return self._screen.game.console.root

    @property
    def context(self):
        """Context wrapper for TCOD Console.

        Allows for position calls to be routed through the contextmanager
        decorated functions.
        """
        return self._screen.game.console.context

    @property
    def screen(self):
        """The screen this view is rendered in, if it exists."""
        if self._screen:
            return self._screen
        return self.tree.superview.screen

    @property
    def frame(self) -> Rect:
        return self._frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        self._frame = value

    @property
    def intrinsic_size(self) -> Optional[Size]:
        return None

    def perform_draw(self) -> None:
        if self.hidden:
            return
        self.draw()
        for view in self.tree.subviews:
            with self.context.translate(view.frame.origin):
                view.perform_draw()

    def draw(self):
        if self._clear:
            self.console.clear()
