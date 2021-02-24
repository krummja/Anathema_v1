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
        self.entity.remove('Blocker')
        self.entity.remove('Opacity')
        return True

    def close_door(self):
        if not self._is_open:
            return False
        self._is_open = False
        self.entity['Renderable'].char = self._closed_char
        self.entity.add('Blocker', {})
        self.entity.add('Opacity', {})
        return True

    def on_get_interactions(self, evt):
        if self._is_open:
            evt.data.expect['interactions'].append({
                "name": "Close",
                "evt": "try_close_door"
                })
        elif not self._is_open:
            evt.data.expect['interactions'].append({
                "name": "Open",
                "evt": "try_open_door"
                })
            # evt.data.expect['interactions'].append({
            #     "name": "Bash",
            #     "evt": "try_bash_door"
            #     })
        return evt

    def on_try_close_door(self, evt):
        if self.close_door():
            print("The door shuts.")
        evt.handle()

    def on_try_open_door(self, evt):
        if self.open_door():
            print("The door opens.")
        evt.handle()
