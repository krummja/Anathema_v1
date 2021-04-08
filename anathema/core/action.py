from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from ecstremity import Entity


class Action:

    def __init__(
            self,
            entity: Entity,
            event: str,
            data: Dict[str, Any],
            cost: float = (20 / 20) * 1000
        ) -> None:
        self.entity = entity
        self.event = event
        self.data = data
        self.cost = cost
