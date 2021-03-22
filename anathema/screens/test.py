from __future__ import annotations

from anathema.abstracts.screen import UIScreen


class TestScreen(UIScreen):

    def __init__(self, *args, **kwargs):
        views = []
        super().__init__(views, *args, **kwargs)

    def quit(self):
        self.manager.pop_screen()

    def cmd_escape(self):
        raise SystemExit()
