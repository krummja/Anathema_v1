from __future__ import annotations

from .rect_view import RectView
from .label_view import LabelView
from anathema.abstracts.view import AbstractView, LayoutOptions


class WindowView(RectView):

    def __init__(self, title=None, *args, subviews=None, **kwargs):
        super().__init__(*args, fill=True, **kwargs)
        self.title_view = LabelView(title, layout_options=LayoutOptions.row_top(1))
        self.content_view = AbstractView(
            subviews=subviews,
            layout_options=LayoutOptions(top=1, right=1, bottom=1, left=1))
        self.add_subviews([self.title_view, self.content_view])
