from __future__ import annotations

from ecstremity import Component


class Door(Component):

    def __init__(self, is_open: bool = True) -> None:
        self._is_open = is_open
        self._open_char = "○"
        self._closed_char = "◙"

    def open_door(self):
        print(self._is_open)
        if self._is_open:
            return False
        self._is_open = True
        self.entity['Renderable'].char = self._open_char
        self.entity['Blocker'].impassable = False
        self.entity['Opacity'].opaque = False
        return True

    def close_door(self):
        pass

    def on_get_interactions(self, evt):
        if self._is_open:
            evt.data.append({
                "name": "close_door",
                "evt": "try_close_door"
                })
        else:
            evt.data.append({
                "name": "open_door",
                "evt": "try_open_door"
                })
        return evt

    def on_try_close_door(self, evt):
        pass

    def on_try_open_door(self, evt):
        open = self.open_door()
        if open:
            print("The door opens.")
        evt.handle()
