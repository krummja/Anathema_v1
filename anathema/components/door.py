from __future__ import annotations

from ecstremity import Component


class Door(Component):

    def __init__(self) -> None:
        self._is_open = False
        self._open_char = "○"
        self._closed_char = "◙"

    @property
    def is_open(self) -> bool:
        return self._is_open

    def open_door(self):
        if self._is_open:
            return False
        self._is_open = True
        self.entity['Renderable'].char = self._open_char
        self.entity['Blocker'].impassable = False
        self.entity['Opacity'].opaque = False
        return True

    def close_door(self):
        if not self._is_open:
            return False
        self._is_open = False
        self.entity['Renderable'].char = self._closed_char
        self.entity['Blocker'].impassable = True
        self.entity['Opacity'].opaque = True
        return True

    def on_get_interactions(self, evt):
        if self._is_open:
            evt.data.append({
                "name": "close_door",
                "evt": "try_close_door"
                })
        elif not self._is_open:
            evt.data.append({
                "name": "open_door",
                "evt": "try_open_door"
                })
        return evt

    def on_try_close_door(self, evt):
        _close = self.close_door()
        if _close:
            print("The door shuts.")
        evt.handle()

    def on_try_open_door(self, evt):
        _open = self.open_door()
        if _open:
            print("The door opens.")
        evt.handle()
