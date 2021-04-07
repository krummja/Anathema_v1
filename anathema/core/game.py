from __future__ import annotations
import nocterminal as noc

from screens.main_menu import MainMenuScreen
from .ecs import ECSManager


class Game(noc.Director):

    def __init__(self):
        super().__init__()
        self.ecs = ECSManager(self)

    def get_initial_screen(self):
        return MainMenuScreen()
