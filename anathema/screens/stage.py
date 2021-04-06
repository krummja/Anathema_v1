from __future__ import annotations
from typing import Dict, Tuple

from bearlibterminal import terminal as blt

from anathema.core.options import Options
from anathema.screens.screen import UIScreen
from anathema.screens.views.rect_view import RectView
from anathema.screens.views.layout_options import LayoutOptions
from anathema.screens.views.stage import StageView


MOVE_KEYS: Dict[int, Tuple[int, int]] = {
    # Arrow keys.
    blt.TK_LEFT: (-1, 0),
    blt.TK_RIGHT: (1, 0),
    blt.TK_UP: (0, -1),
    blt.TK_DOWN: (0, 1),
    blt.TK_HOME: (-1, -1),
    blt.TK_END: (-1, 1),
    blt.TK_PAGEUP: (1, -1),
    blt.TK_PAGEDOWN: (1, 1),
    blt.TK_PERIOD: (0, 0),
    # Numpad keys.
    blt.TK_KP_1: (-1, 1),
    blt.TK_KP_2: (0, 1),
    blt.TK_KP_3: (1, 1),
    blt.TK_KP_4: (-1, 0),
    blt.TK_KP_5: (0, 0),
    blt.TK_KP_6: (1, 0),
    blt.TK_KP_7: (-1, -1),
    blt.TK_KP_8: (0, -1),
    blt.TK_KP_9: (1, -1),
    }


class Stage(UIScreen):

    def __init__(self, *args, **kwargs) -> None:
        views = [
            StageView(layout=LayoutOptions(left=0, top=0, right=24, bottom=14))
            # RectView(layout=LayoutOptions(left=0, top=0, right=24, bottom=14),
            #          subviews=[StageView()]),
            # RectView(layout=LayoutOptions(left=Options.SCREEN_WIDTH-24, right=0)),
            # RectView(layout=LayoutOptions(top=Options.SCREEN_HEIGHT-14, right=24, bottom=0))
            ]
        super().__init__(views, *args, **kwargs)
        self.covers_screen = True

    def become_active(self):
        self.view.perform_draw(self.manager.ctx)
        self.game.renderer.refresh()

    def terminal_update(self, is_active=False):
        self.game.update_engine_systems(0)

    def terminal_read(self, val):
        if val == blt.TK_ESCAPE:
            self.manager.pop_screen(may_exit=False)
        if val in MOVE_KEYS:
            self.game.player.move(MOVE_KEYS[val])
