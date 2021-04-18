from __future__ import annotations
from typing import *

from anathema.engine.systems import BaseSystem

if TYPE_CHECKING:
    pass


class ActionSystem(BaseSystem):

    def initialize(self):
        self.query('actors', all_of=[ 'Actor' ])

    def update(self):
        pass
