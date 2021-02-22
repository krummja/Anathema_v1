from __future__ import annotations
from collections import defaultdict
from typing import Callable, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


@dataclass
class Action:
    # TODO: Make this an Abstract and then extend

    entity: Entity
    event: str
    data: List[Any]
    condition: Callable[[], bool] = None
    cost: int = (20 / 20) * 1000  # FIXME: Add skill-based mods here

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    def plan(self) -> Optional[Action]:
        if self.condition:
            result = self.condition()
            if isinstance(result, bool):
                self.success = result
            else:
                self.success = result[0]
                self.data.append(result[1])
        return self

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity.fire_event('energy_consumed', self.cost)
        self.entity.fire_event(self.event, (self.success, self.data))
