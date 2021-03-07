from __future__ import annotations
from typing import Callable, Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


class Action:

    def __init__(
            self, *,
            entity: Entity,
            event: str,
            data: Dict[str, Any],
            cost: float = (20 / 20) * 1000
        ) -> None:
        self.entity = entity
        self.event = event
        self.data = data
        self.cost = cost

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity.fire_event('energy_consumed', {'cost': self.cost})
        result = self.entity.fire_event(self.event, self.data)
        return result
