from __future__ import annotations

from .bases.body_part import BodyPart

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .body import Body


class Arms(BodyPart):

    def __init__(self, arm_count: int = 2) -> None:
        super().__init__()
        self.arm_count = arm_count
