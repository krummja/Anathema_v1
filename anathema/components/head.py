from __future__ import annotations
from typing import TYPE_CHECKING

from .bases.body_part import BodyPart

if TYPE_CHECKING:
    from .body import Body


class Head(BodyPart):

    def __init__(self) -> None:
        super().__init__()
