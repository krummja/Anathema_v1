from __future__ import annotations
from typing import *
import numpy as np

from anathema.engine.behavior.goal_types import all_goal_types

if TYPE_CHECKING:
    from ecstremity import Engine, Entity, Component
    from anathema.engine.behavior.goal_types.goal_type import GoalType


class GoalEvaluator:

    goal_type_registry = all_goal_types()

    @staticmethod
    def get(name: str):
        goal_type: Type[GoalType] = GoalEvaluator.goal_type_registry.get(name)
        if not goal_type:
            raise KeyError(f"GoalType [${name}] not found!")
        return goal_type

    @staticmethod
    def is_finished(entity: Entity, goal: Component) -> bool:
        goal_type: Type[GoalType] = GoalEvaluator.get(goal.name)
        return goal_type.is_finished(entity, goal)

    @staticmethod
    def take_action(entity: Entity, goal: Component):
        goal_type: Type[GoalType] = GoalEvaluator.get(goal.name)
        return goal_type.take_action(entity, goal)
