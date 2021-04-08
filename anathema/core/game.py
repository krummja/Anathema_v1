from __future__ import annotations
import nocterminal as noc

from screens.main_menu import MainMenuScreen
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager
from anathema.core.player import PlayerManager

from anathema.systems.action_system import ActionSystem
from anathema.systems.physics_system import PhysicsSystem
from anathema.systems.interaction_system import InteractionSystem
from anathema.systems.fov_system import FOVSystem


class Game(noc.Director):

    def __init__(self):
        super().__init__()
        self.ecs = ECSManager(self)
        self.clock = ClockManager(self)
        self.player = PlayerManager(self)

        self.action_system = ActionSystem(self)
        self.physics_system = PhysicsSystem(self)
        self.interaction_system = InteractionSystem(self)
        self.fov_system = FOVSystem(self)

    def get_initial_screen(self):
        return MainMenuScreen()

    def pre_update(self, dt):
        for _ in range(20):
            self.clock.update(dt)  # TICK!
            self.action_system.update(dt)
            self.physics_system.update(dt)
            self.interaction_system.update(dt)

    def post_update(self, dt):
        for _ in range(20):
            self.fov_system.update(dt)
            # self.render_system.update(dt)
            pass
