from __future__ import annotations
from typing import Optional

from ecstremity import Component


class Dimensions(Component):

    def __init__(
            self,
            width: int,
            height: int,
            margin: Optional[int] = 0,
            padding: Optional[int] = 0,
        ) -> None:
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
