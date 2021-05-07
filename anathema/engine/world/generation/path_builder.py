from __future__ import annotations
from typing import *
from morphism import *

if TYPE_CHECKING:
    pass


class PathBuilder:

    def __init__(
            self, *,
            start: Rect,
            end: Rect,
            size: int,
        ) -> None:
        _distance = start.distance_to(end)
        _count = _distance // size

