from __future__ import annotations
from morphism import Point, Size, Rect
from anathema.interface.views import View


class LabelView(View):

    def __init__(
            self,
            text,
            color_fg=(255, 255, 255),
            color_bg=(21, 21, 21),
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
    def intrinsic_size(self) -> Size:
        if self._explicit_size:
            return self._explicit_size
        height = 0
        width = 0
        for line in self.text.splitlines():
            height += 1
            width = max(width, len(line))
        return Size(width, height)

    def draw(self):
        self.context.set_fg(self.bounds, self.color_fg)
        self.context.set_bg(self.bounds, self.color_bg)

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

        self.context.print(Point(x, y).floored, self.text)
