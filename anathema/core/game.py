from __future__ import annotations
import nocterminal as noc
from collections import deque
import tcod

from screens.test_screen import TestScreen
from anathema.core.clock import ClockManager
from anathema.core.ecs import ECSManager
from anathema.core.player import PlayerManager
from anathema.core.world import WorldManager
from anathema.core.storage import StorageManager
from anathema.core.console import ConsoleManager
from anathema.core.input import InputManager
from anathema.core.screen import ScreenManager
# from anathema.core.camera import CameraManager

from anathema.systems.action_system import ActionSystem
from anathema.systems.physics_system import PhysicsSystem
from anathema.systems.interaction_system import InteractionSystem
from anathema.systems.fov_system import FOVSystem
# from anathema.systems.render_system import RenderSystem


class Game:

    _last_update: float = 0.0
    context: tcod.context.Context

    def __init__(self):
        self.ecs = ECSManager(self)
        self.clock = ClockManager(self)
        self.console = ConsoleManager(self)
        self.screens = ScreenManager(self)
        self.input = InputManager(self)
        self.world = WorldManager(self)
        self.player = PlayerManager(self)
        self.storage = StorageManager(self)

        # self.action_system = ActionSystem(self)
        # self.physics_system = PhysicsSystem(self)
        # self.interaction_system = InteractionSystem(self)
        # self.fov_system = FOVSystem(self)
        # self.render_system = RenderSystem(self)

    def run(self):
        self.screens.replace_screen(self.screens.get_initial_screen())
        self.main_loop()

    def start(self):
        self.world.initialize()
        self.player.initialize()

    def main_loop(self):
        with tcod.context.new_terminal(
                columns = self.console.CONSOLE_WIDTH,
                rows = self.console.CONSOLE_HEIGHT,
                tileset = tcod.tileset.load_tilesheet("font_16.png", 32, 8, tcod.tileset.CHARMAP_CP437),
                title = "Anathema",
                vsync = True
        ) as self.context:
            try:
                iteration = False
                while self.loop_iteration():
                    iteration = True
                if not iteration:
                    print("Exited after a single cycle.")
            except KeyboardInterrupt:
                pass

    def loop_iteration(self):
        key_events = tcod.event.wait()
        self.input.handle_input(key_events)
        self.console.root_console.clear()

        i = 0
        for j, screen in enumerate(self.screens._stack):
            if screen.covers_screen:
                i = j
        for screen in self.screens._stack[i:]:
            screen.on_iteration_update(screen == self.screens._stack[-1])

        self.context.present(self.console.root_console)
        return True

    def engine_update(self, dt):
        self.clock.update(dt)
        # player_turn = self.action_system.update(dt)
        # if player_turn:
        #     self.systems_update(dt)

    def systems_update(self, dt):
        pass
        # self.physics_system.update(dt)
        # self.interaction_system.update(dt)
        # self.fov_system.update(dt)
        # self.render_system.update(dt)
