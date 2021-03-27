from __future__ import annotations

from bearlibterminal import terminal

from anathema.screens.views.label_view import LabelView
from anathema.screens.views.layout_options import LayoutOptions
from anathema.screens.views.view import View

from morphism import Point, Size


class IntStepperView(View):

    def __init__(
            self,
            value,
            callback,
            min_value=None,
            max_value=None,
            *args, **kwargs
        ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.label_view = LabelView(
            str(value), align_horz='left', align_vert='top',
            layout=LayoutOptions().with_updates(left=2, right=0))
        self.value = value
        super().__init__(subviews=[self.label_view], *args, **kwargs)
        self.callback = callback

    @property
    def can_become_first_responder(self):
        return True

    @property
    def value(self):
        return int(self.label_view.text)

    @value.setter
    def value(self, new_value):
        self.label_view.text = str(new_value)
        if self.superview:
            self.superview.set_needs_layout()

    @property
    def intrinsic_size(self):
        # add space for arrows
        return self.label_view.intrinsic_size + Size(4, 0)

    def set_needs_layout(self, val=True):
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_first_responder(self):
        self.label_view.color_fg = 0xFF151515
        self.label_view.color_bg = 0xFFFFFFFF

    def did_resign_first_responder(self):
        self.label_view.color_fg = 0xFFFFFFFF
        self.label_view.color_bg = 0xFF151515

    def draw(self, ctx):
        color_fg = 0xFFFFFFFF
        color_bg = 0xFF151515
        if self.is_first_responder:
            color_fg = 0xFF151515
            color_bg = 0xFFFFFFFF
        ctx.color = color_fg
        ctx.bkcolor = color_bg
        ctx.print(Point(0, 0), '← ')
        ctx.print(Point(self.bounds.width + 2, 0), ' →')

    def terminal_read(self, val):
        if val == terminal.TK_LEFT and (self.min_value is None or self.value > self.min_value):
            self.value -= 1
            self.callback(self.value)
            return True

        if val == terminal.TK_RIGHT and (self.max_value is None or self.value < self.max_value):
            self.value += 1
            self.callback(self.value)
            return True
