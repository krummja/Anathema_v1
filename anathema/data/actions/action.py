from __future__ import annotations
from typing import *

from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


@dataclass
class Action:
    entity: Entity
    event: str
    data: Dict[str, Any]
    cost: float = (20 / 10) * 1000

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity.fire_event('energy_consumed', {'cost': self.cost})
        result = self.entity.fire_event(self.event, self.data)
        return result
