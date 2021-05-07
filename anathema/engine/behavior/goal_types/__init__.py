from typing import Dict, Type

from anathema.engine.behavior.goal_types.goal_type import GoalType
from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType
from anathema.engine.behavior.goal_types.move_goal_type import MoveGoalType
from anathema.engine.behavior.goal_types.kill_something_goal_type import KillSomethingGoalType


def all_goal_types() -> Dict[str, Type[GoalType]]:
    return {
        "Bored": BoredGoalType,
        "Move": MoveGoalType,
        "KillSomething": KillSomethingGoalType
    }
