from __future__ import annotations
from typing import *
import tcod
from morphism import *

from anathema.interface.views import View, Layout
from .label_view import LabelView


class BarGaugeView(View):

    def __init__(
            self,
            text: str,
            label: str,
            fullness: float,
            fg: Tuple[int, int, int],
            *args, **kwargs
            ) -> None:
        super().__init__(subviews=[LabelView(label, align_horz = "left")], *args, **kwargs)
        self.text = text
        self.label = label
        self.fullness = fullness
        self.fg = fg
        self.bg_hue = (fg[0] // 2, fg[1] // 2, fg[2] // 2)

    def draw(self):
        self.context.print(Point(1, 1), self.text.center(self.frame.width)[:self.frame.width], fg=(255, 255, 255))
        bar_bg = self.context.tiles_rgb(Point(1, 1), self.frame.width, self.frame.height)["bg"]
        bar_bg[...] = self.bg_hue
        fill_width = max(0, min(self.frame.width, int(self.fullness * self.frame.width)))
        bar_bg[:fill_width] = self.fg
