from __future__ import annotations

from ecstremity import Component


class Container(Component):

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.contents = []
        self._is_open = False
        self._open_char = "⌠"
        self._closed_char = "⌡"

    @property
    def is_open(self) -> bool:
        return self._is_open

    def open_chest(self):
        if self._is_open:
            return False
        self._is_open = True
        self.entity['Renderable'].char = self._open_char
        return True

    def close_chest(self):
        if not self._is_open:
            return False
        self._is_open = False
        self.entity['Renderable'].char = self._closed_char
        return True

    def display_contents(self):
        return enumerate(self.contents)

    def on_get_interactions(self, evt):
        if self._is_open:
            evt.data.expect['interactions'].append({
                "name": "Close",
                "evt": "try_close_chest"
                })
        elif not self._is_open:
            evt.data.expect['interactions'].append({
                "name": "Open",
                "evt": "try_open_chest"
                })
        return evt

    def on_try_close_chest(self, evt):
        if self.close_chest():
            print("The chest shuts.")
        evt.handle()

    def on_try_open_chest(self, evt):
        if self.open_chest():
            print("The chest opens.")
        evt.data.append(self.display_contents())
        evt.handle()
        return evt.data
