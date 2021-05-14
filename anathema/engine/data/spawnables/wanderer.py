from __future__ import annotations
from typing import *

from anathema.engine.behavior.goal_types.bored_goal_type import BoredGoalType

if TYPE_CHECKING:
    from anathema.engine.core.game import Game
    from anathema.engine.world.tilemap import TileMap


def create_spawnable(game: Game):
    def spawn(x: int, y: int):
        wanderer = game.ecs.world.create_prefab("Wanderer", {
            "position": {
                "area": game.world.current_area,
                "x": x,
                "y": y,
            },
            "renderable": {
                "char": "T",
                "fg": (0, 255, 255)
            }
        })
        wanderer["Brain"].append_goal(BoredGoalType().create(game.ecs.world))
        return wanderer
    return spawn
