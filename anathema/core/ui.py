from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.abstracts import AbstractManager
from anathema.utils.observer import Data

if TYPE_CHECKING:
    from anathema.core.game import Game


class UIManager(AbstractManager, Data):

    def __init__(self, game: Game) -> None:
        AbstractManager.__init__(self, game)
        Data.__init__(self)

    def clear_data(self):
        self._data.clear()
