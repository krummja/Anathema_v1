from __future__ import annotations

import nocterminal as noc
from ecstremity import EventData


class ModalView(noc.ui.RectView):

    def __init__(self, title=None, *args, subviews=None, layout=None, **kwargs):
        super().__init__(*args, fill=True, layout=layout, **kwargs)
        self.title_view = noc.ui.LabelView(title, layout=noc.ui.LayoutOptions.row_top(1))
        self.content_view = noc.ui.View(
            subviews=subviews, layout=noc.ui.LayoutOptions(top=1, right=1, bottom=1, left=1))
        self.add_subviews([self.title_view, self.content_view])


class SelectFrom(noc.ui.UIScreen):

    def __init__(self, data: EventData, layout=None):
        button_generator = (noc.ui.ButtonView(
            text=interaction['name'],
            callback=interaction['event'],
            post_callback=self.quit
        ) for interaction in data.interactions)

        self.key_assign = noc.ui.KeyAssignedListView(value_controls=button_generator)

        height = len(data.interactions) + 4
        if layout is None:
            layout = noc.ui.LayoutOptions.centered(width=16, height=height)

        super().__init__(ModalView(
            title=f"Item",
            subviews=[self.key_assign],
            layout=layout))
        self.covers_screen = False

    def quit(self):
        self.director.pop_screen()
