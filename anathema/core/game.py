from __future__ import annotations

import time

from anathema.core.renderer import RenderManager
from anathema.core.input import InputController
from anathema.core.screens import ScreenManager
from anathema.core.fps import FPSManager
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager


class Game:

    _last_update: float

    def __init__(self) -> None:
        self.ecs = ECSManager(self)

        self.clock = ClockManager(self)
        self.renderer = RenderManager(self)
        # self.camera = CameraManager(self)
        self.screens = ScreenManager(self)
        self.input = InputController(self)
        # self.ui = UIManager(self)
        # self.log = LogManager(self)
        self.fps = FPSManager(self)

        # self.action_system = ActionSystem(self)
        # self.physics_system = PhysicSystem(self)
        # self.fov_system = FOVSystem(self)
        # self.render_system = RenderSystem(self)

    @property
    def engine(self):
        return self.ecs.engine

    def start(self) -> None:
        self.renderer.setup()
        self._last_update = time.time()
        self.loop()
        self.renderer.teardown()

    def update_engine_systems(self) -> None:
        pass

    def update_player_systems(self) -> None:
        pass

    def loop(self) -> None:
        while True:
            now = time.time()
            dt = now - self._last_update
            self.screens.update(dt)
            self.fps.update(dt)
            self.renderer.terminal.refresh()
            self._last_update = now
