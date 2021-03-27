from __future__ import annotations

from anathema.screens.stage import Stage
from anathema.screens.screen import UIScreen
from anathema.screens.views.layout_options import LayoutOptions
from anathema.screens.views.button_view import ButtonView
from anathema.screens.views.label_view import LabelView
from anathema.screens.views.int_stepper import IntStepperView
from anathema.screens.views.rect_view import RectView
from anathema.screens.views.collection_list import KeyAssignedListView
from anathema.screens.views.window_view import WindowView


class MainMenu(UIScreen):

    def __init__(self, *args, **kwargs) -> None:
        views = [
            LabelView("Anathema", align_vert='top', align_horz='left',
                      layout=LayoutOptions(left=10, top=10), large=True),
            ButtonView("Play", callback=self.play,
                       layout=LayoutOptions.row_bottom(12).with_updates(
                           left=0.2, width=0.2, right=None)),
            ButtonView("Quit", callback=self.quit,
                       layout=LayoutOptions.row_bottom(12).with_updates(
                           left=0.6, width=0.2, right=None)),
            ]
        super().__init__(views, *args, **kwargs)
        self.covers_screen = True

    def become_active(self) -> None:
        self.game.renderer.clear()

    def play(self):
        self.manager.push_screen(Stage())

    def quit(self) -> None:
        self.manager.pop_screen()
