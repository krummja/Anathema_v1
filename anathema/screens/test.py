from __future__ import annotations

from anathema.core.options import Options
from anathema.screens.screen import UIScreen
from anathema.screens.views.layout_options import LayoutOptions
from anathema.screens.views.label_view import LabelView
from anathema.screens.views.window_view import WindowView
from anathema.screens.views.rect_view import RectView


class TestScreen(UIScreen):

    name: str = "Test"

    def __init__(self, *args, **kwargs):
        views = [
            RectView(color_bg=0x66FF1111,
                     layout=LayoutOptions(left=6, right=6, top=4, bottom=4))
            ]
        super().__init__(views, *args, **kwargs)
        self.covers_screen = True

    def become_active(self):
        self.game.renderer.clear()

    def quit(self):
        self.manager.pop_screen()


class TestScreen2(UIScreen):

    name: str = "Test2"

    def __init__(self, *args, **kwargs):
        views = []
        super().__init__(views, *args, **kwargs)

    def quit(self):
        self.manager.pop_screen()
