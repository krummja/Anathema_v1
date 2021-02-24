from __future__ import annotations
from typing import Callable, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from anathema.core.player import CheckResult
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


@dataclass
class Action:
    # TODO: Make this an Abstract and then extend

    def __init__(
            self,
            entity: Entity,
            event: str,
            data: List[Any],
            check: Optional[Callable[[], CheckResult]] = None,
            cost: float = (20 / 20) * 1000
        ) -> None:
        self.entity = entity
        self.event = event
        self.data = data
        self.check = check
        self.cost = cost

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    def plan(self) -> Action:
        if self.check:
            result = self.check()
            self.success = result.success
            self.data.append(result.data)
        return self

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity.fire_event('energy_consumed', self.cost)
        self.entity.fire_event(self.event, (self.success, self.data))
