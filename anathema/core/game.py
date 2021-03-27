from __future__ import annotations

import time

from anathema.core.renderer import RenderManager
from anathema.core.input import InputController
from anathema.core.screens import ScreenManager
from anathema.core.fps import FPSManager
from anathema.core.log import LogManager
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager
from anathema.core.world import WorldManager
from anathema.core.player import PlayerManager

from anathema.systems.render_system import RenderSystem
from anathema.systems.action_system import ActionSystem
from anathema.systems.physics_system import PhysicsSystem
from anathema.systems.fov_system import FOVSystem
from anathema.systems.interaction_system import InteractionSystem


class Game:

    _last_update: float

    def __init__(self) -> None:
        self.ecs = ECSManager(self)

        self.clock = ClockManager(self)
        self.renderer = RenderManager(self)
        self.world = WorldManager(self)
        self.player = PlayerManager(self)
        self.screens = ScreenManager(self)
        self.input = InputController(self)
        self.log = LogManager(self)
        self.fps = FPSManager(self)

        self.action_system = ActionSystem(self)
        self.physics_system = PhysicsSystem(self)
        self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)
        self.interaction_system = InteractionSystem(self)

    @property
    def engine(self):
        return self.ecs.engine

    def start(self):
        self.renderer.setup()
        self._last_update = time.time()
        self.screens.replace_screen(self.screens.get_initial_screen())
        self.renderer.refresh()

        try:
            self.loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.renderer.teardown()

    def loop(self):
        try:
            iteration = False
            while self.loop_iteration():
                iteration = True
            if not iteration:
                print("Exited after a single cycle.")
        except KeyboardInterrupt:
            pass

    def loop_iteration(self):
        now = time.time()
        dt = now - self._last_update
        self.fps.update(dt)

        should_continue = self.screens.update(dt)

        self.renderer.update()
        self._last_update = now
        return should_continue

    def update_engine_systems(self, dt):
        for _ in range(20):
            self.clock.update(dt)
            player_turn = self.action_system.update(dt)
            if player_turn:
                self.update_player_systems(dt)
                return

    def update_player_systems(self, dt):
        self.physics_system.update(dt)
        self.interaction_system.update(dt)
        self.fov_system.update(dt)
        self.render_system.update(dt)
