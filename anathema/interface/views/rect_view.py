from __future__ import annotations
from typing import *
from morphism import *

from anathema.interface.views import View

if TYPE_CHECKING:
    pass


class RectView(View):
    def __init__(
            self,
            fg=(255, 255, 255),
            bg=(21, 21, 21),
            fill=False,
            style='single',
            *args,
            **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self.fg = fg
        self.bg = bg
        self.fill = fill
        self.style = style

    def draw(self):
        self.context.draw_frame(self.bounds, fg=(255, 255, 255), bg=(21, 21, 21))
