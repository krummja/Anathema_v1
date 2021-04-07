from __future__ import annotations
import nocterminal as noc

from screens.main_menu import MainMenuScreen
from anathema.core.ecs import ECSManager
from anathema.core.actions import ActionManager
from anathema.core.player import PlayerManager


class Game(noc.Director):

    def __init__(self):
        super().__init__()
        self.ecs = ECSManager(self)
        print(self.ecs.engine.components)
        self.actions = ActionManager(self)
        self.player = PlayerManager(self)

    def get_initial_screen(self):
        return MainMenuScreen()
