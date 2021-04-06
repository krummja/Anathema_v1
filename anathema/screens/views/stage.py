from __future__ import annotations
from morphism import *

from anathema.screens.views.view import View


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

    def draw(self, ctx):
        ctx.print(Point(1, 1), "Test")
        ctx.print(Point(1, 3), str(self.screen.game.player.position))
