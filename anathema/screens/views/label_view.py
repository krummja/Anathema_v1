from __future__ import annotations

from screens.views.view import View
from morphism import Point, Size, Rect


class LabelView(View):

    def __init__(
            self,
            text,
            color_fg=0xFFFFFFFF,
            color_bg=0xFF151515,
            align_horz='center',
            align_vert='center',
            size=None,
            large=False,
            *args,
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.align_horz = align_horz
        self.align_vert = align_vert
        self.text = text
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.large = large
        self._explicit_size = size

    @property
    def intrinsic_size(self):
        if self._explicit_size:
            return self._explicit_size
        height = 0
        width = 0
        for line in self.text.splitlines():
            height += 1
            width = max(width, len(line))
        return Size(width, height)

    def draw(self, ctx):
        ctx.color = self.color_fg
        ctx.bkcolor = self.color_bg

        if self.color_bg is None:
            ctx.bkcolor = 0xFF151515
        # if self.clear:
        #     ctx.clear_area(self.bounds)
        x = 0
        if self.align_horz == 'center':
            x = self.bounds.width / 2 - self.intrinsic_size.width / 2
        elif self.align_horz == 'right':
            x = self.bounds.width - self.intrinsic_size.width

        y = 0
        if self.align_vert == 'center':
            y = self.bounds.height / 2 - self.intrinsic_size.height / 2
        elif self.align_vert == 'bottom':
            y = self.bounds.height - self.intrinsic_size.height

        if self.clear:
            for _x in range(self.intrinsic_size.width):
                ctx.clear_area(Rect(Point(x + _x, y), Size(1, 1)))

        if self.large:
            ctx.print_big(Point(x, y).floored, self.text)
        else:
            ctx.print(Point(x, y).floored, self.text)

    def debug_string(self):
        return super().debug_string() + ' ' + repr(self.text)
