from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from collections import deque

from anathema.data.actions.action import Action
from anathema.abstracts import AbstractManager
from anathema.world.tile_factory import Depth

if TYPE_CHECKING:
    from anathema.core import Game


class PlayerManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.action_queue = deque([])
        self._player_uid = None
        self.initialize_player()

    @property
    def entity(self):
        return self.game.ecs.engine.get_entity(self._player_uid)

    @property
    def uid(self):
        return self._player_uid

    @property
    def is_turn(self) -> bool:
        return self.entity['Actor'].has_energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['Position'].xy

    def initialize_player(self):
        player = self.game.ecs.engine.create_entity()
        self.game.ecs.engine.prefabs.apply_to_entity(
            player, 'Player', {'Position': {'x': 10, 'y': 10, 'z': Depth.ABOVE_1.value}})
        self._player_uid = player.uid

        self.game.world.current_area.tiles[10, 10, Depth.ABOVE_1.value] = self._player_uid
        return player

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        def blocked() -> bool:
            if self.game.world.current_area.is_blocked(
                self.position[0] + direction[0],
                self.position[1] + direction[1]
                ):
                return False
            return True
        action = Action(self.entity, 'try_move', direction, blocked).plan()
        self.action_queue.append(action.act)
