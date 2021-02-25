from __future__ import annotations

from ecstremity import Component

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .body import Body


class Eyes(Component):

    def __init__(self, vision: int = 8, eye_count: int = 2) -> None:
        self.vision = vision
        self._eye_count = eye_count

    @property
    def body(self) -> Body:
        return self._body

    @body.setter
    def body(self, value: Body) -> None:
        self._body = value
