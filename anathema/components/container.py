from __future__ import annotations

from anathema.data.message import Message
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

    def add_to(self, item) -> None:
        pass

    def take_from(self, item) -> None:
        pass

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
            evt.data['expect'].append({
                "name": "Close",
                "evt": "try_close_container"
                })
        elif not self._is_open:
            evt.data['expect'].append({
                "name": "Open",
                "evt": "try_open_container"
                })
        return evt

    def on_try_close_container(self, evt):
        if self.close_container():
            self.ecs.client.log.report(Message(f"The {0} shut[s].",
                                               noun1=self.entity['Noun']))
        evt.handle()

    def on_try_open_container(self, evt):
        if self.open_container():
            self.ecs.client.log.report(Message(f"The {0} open[s].",
                                               noun1=self.entity['Noun']))
        evt.data.append(self.display_contents())
        evt.handle()
        return evt.data
