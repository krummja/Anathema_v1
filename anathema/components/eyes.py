from __future__ import annotations

from .bases.body_part import BodyPart

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .body import Body


class Eyes(BodyPart):

    def __init__(self, vision: int = 8, eye_count: int = 2) -> None:
        super().__init__()
        self.vision = vision
        self._eye_count = eye_count
