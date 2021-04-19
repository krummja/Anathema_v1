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
            color_fg=(255, 255, 255),
            color_bg=(21, 21, 21),
            size=None,
            clear=False,
            *args, **kwargs
            ) -> None:
        self.label_view = LabelView(
            text,
            align_horz=align_horz,
            align_vert=align_vert,
            size=size,
            color_fg=color_fg,
            color_bg=color_bg,
            clear=clear
            )
        super().__init__(subviews=[self.label_view], *args, **kwargs)
        self.color_fg = color_fg
        self.color_bg = color_bg
        self.callback = callback

    def set_needs_layout(self, val: bool = True) -> None:
        super().set_needs_layout(val)
        self.label_view.set_needs_layout(val)

    def did_become_responder(self):
        self.label_view.color_fg = self.color_bg
        self.label_view.color_bg = self.color_fg

    def did_resign_responder(self):
        self.label_view.color_fg = self.color_fg
        self.label_view.color_bg = self.color_bg

    def draw(self):
        pass

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
    def can_become_responder(self):
        return True

    def handle_input(self, event):
        if event == tcod.event.K_RETURN:
            self.callback()
            return True


class CyclingButtonView(ButtonView):

    def __init__(self, options, initial_value, callback, *args, **kwargs) -> None:
        self.options = options
        self._inner_callback = callback
        super().__init__(initial_value, self._call_inner_callback, *args, **kwargs)

    def _call_inner_callback(self):
        i = self.options.index(self.text)
        new_value = self.options[(i + 1) % len(self.options)]
        self.text = new_value
        self._inner_callback(new_value)
