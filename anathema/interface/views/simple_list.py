from __future__ import annotations
from typing import *
from morphism import *
from math import floor
import tcod

from anathema.engine.core.options import Options
from .label_view import LabelView
from .rect_view import RectView
from .first_responder import FirstResponderView
from anathema.interface.views import View


class SimpleListView(View):

    def __init__(
            self,
            *args,
            **kwargs
        ) -> None:
        self.rect_view = RectView()
        self.rect_view.fill = False

        self.list_items = []
        super().__init__(subviews=[self.rect_view], *args, **kwargs)

    @property
    def inner_height(self) -> int:
        return self.frame.height - 3

    def update(self, display_list):
        self.list_items = []
        self.list_items = [LabelView(item, align_horz = "left") for item in display_list]
