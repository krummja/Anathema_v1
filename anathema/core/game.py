from __future__ import annotations

import time

from anathema.core.renderer import RenderManager
from anathema.core.input import InputController
from anathema.core.screens import ScreenManager
from anathema.core.fps import FPSManager
from anathema.core.camera import CameraManager
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager
from anathema.core.world import WorldManager
from anathema.core.player import PlayerManager
from anathema.core.ui import UIManager

from anathema.systems.render_system import RenderSystem
from anathema.systems.action_system import ActionSystem
from anathema.systems.physics_system import PhysicsSystem
from anathema.systems.fov_system import FOVSystem


class Game:

    _last_update: float

    def __init__(self) -> None:
        self.ecs = ECSManager(self)

        self.clock = ClockManager(self)
        self.renderer = RenderManager(self)
        self.world = WorldManager(self)
        self.player = PlayerManager(self)
        self.ui = UIManager(self)
        self.screens = ScreenManager(self)
        self.input = InputController(self)
        self.fps = FPSManager(self)

        self.action_system = ActionSystem(self)
        self.physics_system = PhysicsSystem(self)
        self.fov_system = FOVSystem(self)
        self.render_system = RenderSystem(self)

    @property
    def engine(self):
        return self.ecs.engine

    def start(self) -> None:
        self.renderer.setup()
        self._last_update = time.time()
        self.loop()
        self.renderer.teardown()

    def update_engine_systems(self, dt) -> None:
        for _ in range(20):
            self.clock.update(dt)
            player_turn = self.action_system.update(dt)
            if player_turn:
                self.update_player_systems(dt)
                return

    def update_player_systems(self, dt) -> None:
        self.physics_system.update(dt)
        self.fov_system.update(dt)
        self.render_system.update(dt)

    def loop(self) -> None:
        while True:
            now = time.time()
            dt = now - self._last_update
            self.fps.update(dt)

            self.screens.update(dt)     # enque render_system on_draw methods
            # self.ui.update(dt)
            self.renderer.update(dt)    # run entire render stack

            self._last_update = now
