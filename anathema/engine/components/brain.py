from __future__ import annotations
from typing import *

from ecstremity import Component
from anathema.engine.behavior.goal_action_result import *

if TYPE_CHECKING:
    from ecstremity import Entity


class Brain(Component):

    def __init__(self, goals: List[Entity] = None) -> None:
        self.goals: List[Entity] = goals if goals else []

    def on_destroyed(self):
        for goal in self.goals:
            goal.destroy()

    def on_take_action(self, evt):
        while self.peek_goal() and self.peek_goal().is_finished():
            self.pop_goal().entity.destroy()

        current_goal = self.peek_goal()
        result = current_goal.take_action()

        if result == FAILURE:
            self.remove_goal(current_goal)
        elif result == INVALID:
            self.remove_goal(current_goal)
            self.entity.fire_event('take_action')
        evt.handle()

    def remove_goal(self, goal):
        goals_to_destroy = []

        def goal_filter(g: Entity):
            is_self: bool = g.uid == goal.entity.uid
            is_sibling_goal: bool = (g['Goal'].original_intent and
                                     g['Goal'].original_intent == goal.original_intent.uid)
            if is_self or is_sibling_goal:
                goals_to_destroy.append(g['Goal'])
                return False
            return True

        self.goals = [_ for _ in filter(goal_filter, self.goals)]
        for goal in goals_to_destroy:
            goal.entity.destroy()

    def append_goal(self, goal):
        if not isinstance(goal, Component):
            raise TypeError(f"Pushing non-Component goal [{goal}]!")
        goal.parent = self.entity
        return self.goals.append(goal.entity)

    def pop_goal(self):
        return self.goals.pop()['Goal']

    def peek_goal(self):
        return self.goals[len(self.goals) - 1]['Goal']
