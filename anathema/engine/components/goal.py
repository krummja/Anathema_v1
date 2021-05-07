from __future__ import annotations
from typing import *

from ecstremity import Component, Entity
from anathema.engine.behavior.goal_evaluator import GoalEvaluator

if TYPE_CHECKING:
    pass


class Goal(Component):

    def __init__(
            self,
            name: str = 'Bored',
            original_intent: Entity = None,
            parent: Entity = None,
            target: Entity = None,
            complete: bool = False,
            data: Dict[str, Any] = None
        ) -> None:
        self.name = name
        self.original_intent = original_intent
        self.parent = parent
        self.target = target
        self.complete = complete
        self.data = data if data else {}

    def is_finished(self):
        return GoalEvaluator.is_finished(self.parent, self)

    def take_action(self):
        return GoalEvaluator.take_action(self.parent, self)
