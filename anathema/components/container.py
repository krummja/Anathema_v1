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
        evt.data.instigator = self.entity
        if self._is_open:
            evt.data.interactions.append({
                "name": "Close",
                "event": "try_close_container"
                })
        elif not self._is_open:
            evt.data.interactions.append({
                "name": "Open",
                "event": self.open_container
            })
            evt.data.interactions.append({
                "name": "Test",
                "event": "test_method"
            })
        evt.handle()

    def on_try_close_container(self, evt):
        # if self.close_container():
        #     self.ecs.client.log.report(Message(f"The {0} shut[s].",
        #                                        noun1=self.entity['Noun']))
        if self.close_container():
            evt.handle()

    def on_try_open_container(self, evt):
        # if self.open_container():
        #     self.ecs.client.log.report(Message(f"The {0} open[s].",
        #                                        noun1=self.entity['Noun']))
        if self.open_container():
            evt.data.callback(self.display_contents)
            evt.handle()
