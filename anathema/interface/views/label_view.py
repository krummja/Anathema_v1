from __future__ import annotations
from morphism import Point, Size, Rect
from anathema.interface.views import View


class LabelView(View):

    def __init__(
            self,
            text="<unset>",
            fg=(255, 255, 255),
            bg=(21, 21, 21),
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
        self.fg = fg
        self.bg = bg
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

    def update(self, text: str):
        self.text = text

    def draw(self):
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

        self.context.set_fg(Rect(Point(x, y), self.intrinsic_size).floored, self.fg)
        self.context.set_bg(Rect(Point(x, y), self.intrinsic_size).floored, self.bg)
        self.context.print(Point(x, y).floored, self.text)
