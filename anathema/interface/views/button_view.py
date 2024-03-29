from __future__ import annotations
import tcod

from anathema.interface.views import View
from .label_view import LabelView


class ButtonView(View):

    def __init__(
            self,
            text: str,
            callback,
            align_horz='center',
            align_vert='center',
            fg=(255, 255, 255),
            bg=(21, 21, 21),
            size=None,
            clear=False,
            *args, **kwargs
            ) -> None:
        self.label_view = LabelView(
            text,
            align_horz=align_horz,
            align_vert=align_vert,
            size=size,
            fg=fg,
            bg=bg,
            clear=clear
            )
        super().__init__(subviews=[self.label_view], *args, **kwargs)
        self.fg = fg
        self.bg = bg
        self.callback = callback

    def set_needs_layout(self, val: bool = True) -> None:
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_first_responder(self):
        self.label_view.fg = self.bg
        self.label_view.bg = self.fg

    def did_resign_first_responder(self):
        self.label_view.fg = self.fg
        self.label_view.bg = self.bg

    def draw(self):
        if self.clear:
            self.context.clear_area(self.bounds)

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

    def handle_input(self, event):
        if event.sym == tcod.event.K_RETURN:
            self.callback()
            return True


class CyclingButtonView(ButtonView):

    def __init__(self, key, options, initial_value, callback, *args, **kwargs) -> None:
        self.key = key
        self.options = options
        self._inner_callback = callback
        super().__init__(initial_value, self._call_inner_callback, *args, **kwargs)

    def _call_inner_callback(self):
        i = self.options.index(self.text)
        new_value = self.options[(i + 1) % len(self.options)]
        self.text = new_value
        self._inner_callback(self.key, new_value)
