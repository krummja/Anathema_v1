from __future__ import annotations

from .rect_view import RectView
from .label_view import LabelView
from screens.views.view import View
from .layout_options import LayoutOptions


class WindowView(RectView):

    def __init__(self, title=None, *args, subviews=None, **kwargs):
        super().__init__(*args, fill=True, **kwargs)
        self.title_view = LabelView(title, layout=LayoutOptions.row_top(1))
        self.content_view = View(
            subviews=subviews,
            layout=LayoutOptions(top=1, right=1, bottom=1, left=1))
        self.add_subviews([self.title_view, self.content_view])
