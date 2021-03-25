from __future__ import annotations

from screens.views.view import View
from morphism import Point, Size


class LabelView(View):

    def __init__(
            self,
            text,
            color_fg='#ffffff',
            color_bg='#000000',
            align_horz='center',
            align_vert='center',
            size=None,
            *args,
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.align_horz = align_horz
        self.align_vert = align_vert
        self.text = text
        self.color_fg = color_fg
        self.color_bg = color_bg
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
        ctx.bkcolor = self.color_bg or '#000000'
        if self.clear:
            ctx.clear_area(self.bounds)
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

        ctx.print(Point(x, y).floored, self.text)

    def debug_string(self):
        return super().debug_string() + ' ' + repr(self.text)
