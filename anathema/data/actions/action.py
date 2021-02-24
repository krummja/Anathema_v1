from __future__ import annotations
from typing import Dict, Callable, Any, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

from ecstremity import EventData

if TYPE_CHECKING:
    from anathema.core.player import EventData
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


class Action:

    def __init__(
            self, *,
            entity: Entity,
            event: str,
            check: Optional[Callable[[], EventData]] = None,
            cost: float = (20 / 20) * 1000
        ) -> None:
        self.entity = entity
        self.event = event
        self.check = check
        self.cost = cost
        self.data = None

    def plan(self) -> Action:
        """Plan step, which allows for check callbacks and
        various sub-steps of data processing and organization.

        If a check callback is passed in, it is executed. It will
        always return an EventData object.

            EventData
                success: bool
                require: Optional[Dict[str, Any]]
                expect:  Optional[Dict[str, Any]]
                result:  Optional[Dict[str, Any]]

        `success` determines the success of this Action.
        `require` is a dict of resources that must be passed in the act step
                  this is often a reference to an entity whose components we will
                  be expecting something from
        `expect`  is a dict that must be populated by an entity on the execution
                  of the act step.
        `result`  is a dict that contains additional useful data for when the
                  Action finally concludes.
        """
        if self.check:
            self.data = self.check()
        return self

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity.fire_event('energy_consumed', {'cost': self.cost})
        result = self.entity.fire_event(self.event, self.data)
        return result
