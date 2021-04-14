from __future__ import annotations
import nocterminal as noc

from screens.main_menu import MainMenuScreen
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager
from anathema.core.player import PlayerManager
from anathema.core.world import WorldManager

from anathema.systems.action_system import ActionSystem
from anathema.systems.physics_system import PhysicsSystem
from anathema.systems.interaction_system import InteractionSystem
from anathema.systems.fov_system import FOVSystem
from anathema.systems.render_system import RenderSystem


class Game(noc.Director):

    _last_update: float = 0.0

    def __init__(self):
        super().__init__(client=self)
        self.ecs = ECSManager(self)
        self.ecs.initialize()
        self.clock = ClockManager(self)
        self.world = WorldManager(self)
        self.player = PlayerManager(self)

        self.action_system = ActionSystem(self)
        self.physics_system = PhysicsSystem(self)
        self.interaction_system = InteractionSystem(self)
        self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)

    def run(self):
        self.replace_screen(self.get_initial_screen())
        noc.terminal.setup()
        self.main_loop()
        noc.terminal.teardown()

    def start(self):
        self.world.initialize()
        self.player.initialize()

    def get_initial_screen(self):
        return MainMenuScreen()

    def engine_update(self, dt):
        self.clock.update(dt)
        player_turn = self.action_system.update(dt)
        if player_turn:
            self.systems_update(dt)

    def systems_update(self, dt):
        self.physics_system.update(dt)
        self.interaction_system.update(dt)
        self.fov_system.update(dt)
        self.render_system.update(dt)
