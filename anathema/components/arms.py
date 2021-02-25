from __future__ import annotations

from ecstremity import Component

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .body import Body


class Arms(Component):

    @property
    def body(self) -> Body:
        return self._body

    @body.setter
    def body(self, value: Body) -> None:
        self._body = value
