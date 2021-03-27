from __future__ import annotations

from bearlibterminal import terminal
from anathema.screens.views.view import View
from anathema.screens.views.label_view import LabelView


class ButtonView(View):

    def __init__(
            self,
            text: str,
            callback,
            align_horz='center',
            align_vert='center',
            color_fg=0xFFFFFFFF,
            color_bg=0xFF151515,
            size=None,
            *args, **kwargs
            ) -> None:
        self.label_view = LabelView(
            text,
            align_horz=align_horz,
            align_vert=align_vert,
            size=size,
            color_fg=color_fg,
            color_bg=color_bg
            )
        super().__init__(subviews=[self.label_view], *args, **kwargs)

        self.color_fg = color_fg
        self.color_bg = color_bg
        self.callback = callback

    def set_needs_layout(self, val: bool = True) -> None:
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_first_responder(self):
        self.label_view.color_fg = self.color_bg
        self.label_view.color_bg = self.color_fg

    def did_resign_first_responder(self):
        self.label_view.color_fg = self.color_fg
        self.label_view.color_bg = self.color_bg

    def draw(self, ctx):
        if self.clear:
            ctx.bkcolor(self.color_bg)
            ctx.clear_area(self.bounds)

    @property
    def text(self):
        return self.label_view.text

    @text.setter
    def text(self, new_value):
        self.label_view.text = new_value

    @property
    def intrinsic_size(self):
        return self.label_view.intrinsic_size

    def layout_subviews(self):
        super().layout_subviews()
        self.label_view.frame = self.bounds

    @property
    def can_become_first_responder(self):
        return True

    def terminal_read(self, val):
        if val == terminal.TK_ENTER:
            self.callback()
            return True
