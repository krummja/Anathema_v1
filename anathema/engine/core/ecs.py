from __future__ import annotations
from typing import *

from ecstremity import Engine
from anathema.engine.components import all_components
from anathema.engine.core import BaseManager

if TYPE_CHECKING:
    from anathema.engine.core import BaseGame


class ECSManager(BaseManager):

    def __init__(self, game: BaseGame):
        super().__init__(game)
        self.engine = Engine(client=game)
        self.world = self.engine.create_world()

        for component in all_components():
            self.engine.register_component(component)
