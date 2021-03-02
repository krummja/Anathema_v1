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

    def open_container(self):
        if self._is_open:
            return False
        self._is_open = True
        self.entity['Renderable'].char = self._open_char
        return True

    def close_container(self):
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
                "evt": "try_close_container"
                })
        elif not self._is_open:
            evt.data.expect['interactions'].append({
                "name": "Open",
                "evt": "try_open_container"
                })
        return evt

    def on_try_close_container(self, evt):
        if self.close_container():
            print("The chest shuts.")
        evt.handle()

    def on_try_open_container(self, evt):
        if self.open_container():
            print("The chest opens.")
        evt.data.append(self.display_contents())
        evt.handle()
        return evt.data

    def on_get_inventories(self, evt):
        inventories = evt.data.require['inventories']
        inventories[self.entity['Name'].noun_text] = self
        evt.data.require['inventories'] = inventories
        print(inventories)
        return evt
