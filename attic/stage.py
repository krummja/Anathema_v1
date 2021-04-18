from nocterminal.ui import *
from typing import *
from nocterminal import terminal
from morphism import Point


MOVE_KEYS: Dict[int, Tuple[int, int]] = {
    # Arrow keys.
    terminal.TK_LEFT: (-1, 0),
    terminal.TK_RIGHT: (1, 0),
    terminal.TK_UP: (0, -1),
    terminal.TK_DOWN: (0, 1),
    terminal.TK_HOME: (-1, -1),
    terminal.TK_END: (-1, 1),
    terminal.TK_PAGEUP: (1, -1),
    terminal.TK_PAGEDOWN: (1, 1),
    terminal.TK_PERIOD: (0, 0),
    # Numpad keys.
    terminal.TK_KP_1: (-1, 1),
    terminal.TK_KP_2: (0, 1),
    terminal.TK_KP_3: (1, 1),
    terminal.TK_KP_4: (-1, 0),
    terminal.TK_KP_5: (0, 0),
    terminal.TK_KP_6: (1, 0),
    terminal.TK_KP_7: (-1, -1),
    terminal.TK_KP_8: (0, -1),
    terminal.TK_KP_9: (1, -1),
    }


class StageView(View):

    def __init__(
            self,
            color_fg=0xFFAAAAAA,
            color_bg=0xFF151515,
            fill=False,
            style='single',
            *args,
            **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.fill = fill
        self.style = style


class StageScreen(UIScreen):

    def __init__(self):
        # views = [StageView(layout=LayoutOptions(left=0, top=0, right=24, bottom=14))]
        self.view = StageView(layout=LayoutOptions(left=0, top=0, right=24, bottom=14))
        views = []
        super().__init__(views)
        self.covers_screen = True

    def become_active(self):
        self.view.perform_draw(self.director.context)
        self.director.client.systems_update(100)

    def terminal_update(self, is_active=False):
        self.director.client.engine_update(0)

    def terminal_read(self, char):
        if char == terminal.TK_ESCAPE:
            self.director.pop_screen()
        if char in MOVE_KEYS:
            self.director.client.player.move(MOVE_KEYS[char])
