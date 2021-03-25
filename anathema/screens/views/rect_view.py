from __future__ import annotations

from screens.views.view import View


class RectView(View):

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
        ctx.color = self.color_fg
        ctx.bkcolor = self.color_bg
        if self.fill or self.clear:
            ctx.clear_area(self.bounds)
        ctx.draw_box(self.bounds, 0xFFAAAAAA)
