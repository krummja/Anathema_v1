from __future__ import annotations
from typing import *
from anathema.engine.behavior.goal_action_result import *

if TYPE_CHECKING:
    from ecstremity import World, Entity, Component


class GoalType:

    name: str = ""

    @staticmethod
    def is_finished(entity: Entity, goal: Component):
        return False

    @staticmethod
    def take_action(entity: Entity, goal: Component):
        return FAILURE

    def create_sub_goal(self, world: World, original_intent: Component, properties=None):
        if not properties:
            properties = {}

        properties.update({
            "original_intent": original_intent.entity.uid
        })

        return self.create(world, properties)

    def create(self, world: World, properties=None) -> Optional[Component]:
        if not properties:
            properties = {}

        prefab_props = { "GOAL": {} }
        properties.update({ "name": self.name })
        prefab_props["GOAL"] = properties

        return world.create_prefab("Goal", prefab_props)["Goal"]
