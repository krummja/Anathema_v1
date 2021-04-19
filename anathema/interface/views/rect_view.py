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
        self.console.draw_frame(self.bounds.x+10, self.bounds.y+10, self.bounds.width-20, self.bounds.height-20,
                                title="Test Title", fg=(255, 0, 0), bg=(21, 21, 21))
