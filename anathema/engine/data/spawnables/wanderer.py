from __future__ import annotations
from typing import *

import random
from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType

if TYPE_CHECKING:
    from anathema.engine.core.game import Game
    from anathema.engine.world.tilemap import TileMap


def pick_name():
    names = [
        "Korok Shyden",
        "Eithne",
        "Rolm",
        "Gloisur",
        "Braagen",
        "Sethchell",
        "Kiroum",
        "Darglin",
        "Hiabaid Akoorb",
        "Naadra",
        "Jethrik",
        "Zynx",
        "Datz",
        "Batrosque",
        "Eriptil",
        "Gleyden",
        "Frosserthil",
        "Ancelyn Helziatz",
        "Mekeesha",
    ]
    return names[random.randrange(0, len(names)-1)]


def create_spawnable(game: Game):
    def spawn(x: int, y: int):
        wanderer = game.ecs.world.create_prefab("Wanderer", {
            "position": {
                "area": game.maps.current_area,
                "x": x,
                "y": y,
            },
            "renderable": {
                "char": "T",
                "fg": (0, 255, 255)
            },
            "moniker": {
                "name": pick_name()
            }
        })
        wanderer["Brain"].append_goal(BoredGoalType().create(game.ecs.world))
        return wanderer
    return spawn
