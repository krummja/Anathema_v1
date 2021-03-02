from __future__ import annotations
from typing import TYPE_CHECKING

from anathema.abstracts import AbstractManager

if TYPE_CHECKING:
    from anathema.core import Game


class LogManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.log = []

    def report(self, message):
        print(message.text)
        if self.log and self.log[-1].text == message.text:
            self.log[-1].count += 1
        else:
            self.log.append(message)
