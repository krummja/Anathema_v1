from __future__ import annotations
from typing import *

from .base_manager import BaseManager

if TYPE_CHECKING:
    from ecstremity import Entity
    from .game import Game


class PlayerManager(BaseManager):

    def __init__(self, game: Game):
        super().__init__(game)
        self._uid = None

    @property
    def entity(self) -> Entity:
        return self.game.ecs.engine.get_entity(self._uid)

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def is_turn(self) -> bool:
        return self.entity['Actor'].has_energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['Position'].xy

    def initialize(self):
        pass
