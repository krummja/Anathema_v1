from __future__ import annotations
from typing import *
import tcod
import os
import logging
import time

from anathema.engine.core.camera import CameraManager
from anathema.engine.core.clock import ClockManager
from anathema.engine.core.console import ConsoleManager
from anathema.engine.core.content import ContentManager
from anathema.engine.core.ecs import ECSManager
from anathema.engine.core.input import InputManager, LoopExit
from anathema.engine.core.player import PlayerManager
from anathema.engine.core.renderer import RenderManager
from anathema.engine.core.screens import ScreenManager
from anathema.engine.core.world import WorldManager

from anathema.engine.systems.action_system import ActionSystem
from anathema.engine.systems.interaction_system import InteractionSystem
from anathema.engine.systems.physics_system import PhysicsSystem
from anathema.engine.systems.fov_system import FOVSystem
from anathema.engine.systems.render_system import RenderSystem
from anathema.engine.systems.path_system import PathSystem

from anathema.data import *

from .options import Options

if TYPE_CHECKING:
    pass


CONFIG = {
    'columns': Options.CONSOLE_WIDTH,
    'rows': Options.CONSOLE_HEIGHT,
    'tileset': Options.TILESET,
    'title': Options.TITLE,
    'vsync': Options.VSYNC
}


class AbstractGame:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

        self.ecs: Optional[ECSManager] = None
        self.clock: Optional[ClockManager] = None
        self.console: Optional[ConsoleManager] = None
        self.camera: Optional[CameraManager] = None
        self.renderer: Optional[RenderManager] = None
        self.screens: Optional[ScreenManager] = None
        self.input: Optional[InputManager] = None
        self.world: Optional[WorldManager] = None
        self.player: Optional[PlayerManager] = None

        self.content: Optional[ContentManager] = None

        self.action_system: Optional[ActionSystem] = None
        self.physics_system: Optional[PhysicsSystem] = None
        self.interaction_system: Optional[InteractionSystem] = None
        self.fov_system: Optional[FOVSystem] = None
        self.render_system: Optional[RenderSystem] = None
        self.path_system: Optional[PathSystem] = None


class Game(AbstractGame):

    debug = False
    context: tcod.context.Context

    def __init__(self):
        super().__init__()

        self.last_update: float = 0.0

        logging.info("Starting Core Managers\n============================================================")
        self.ecs = ECSManager(self)
        self.clock = ClockManager(self)
        self.console = ConsoleManager(self)
        self.camera = CameraManager(self)
        self.renderer = RenderManager(self)
        self.screens = ScreenManager(self)  # TODO Rename this to "interface"
        self.input = InputManager(self)
        self.world = WorldManager(self)     # TODO Rename this to "maps"
        self.content = ContentManager(self)

    def initialize(self):
        logging.info("ECStremity: Creating World\n============================================================")
        self.ecs.new_world()
        logging.info("Loading Component Prefabs\n============================================================")
        self.content.load_prefabs()
        self.player = PlayerManager(self)

        logging.info("Starting Engine Systems\n============================================================")
        self.action_system: ActionSystem = ActionSystem(self)
        self.physics_system: PhysicsSystem = PhysicsSystem(self)
        self.interaction_system: InteractionSystem = InteractionSystem(self)
        self.fov_system: FOVSystem = FOVSystem(self)
        self.render_system: RenderSystem = RenderSystem(self)
        self.path_system: PathSystem = PathSystem(self)

        self.world.initialize()
        self.player.initialize()

    def teardown(self):
        self.player.teardown()
        self.world.teardown()

        self.action_system = None
        self.physics_system = None
        self.interaction_system = None
        self.fov_system = None
        self.render_system = None
        self.path_system = None

        self.player = None
        self.content.unload_prefabs()
        self.ecs.delete_world()

    def run(self):
        self.last_update = time.time()
        self.screens.replace_screen(self.screens.screens['MAIN MENU'])
        self.loop()

    def loop(self):
        with tcod.context.new(**CONFIG) as self.context:
            while self.screens.should_continue:
                now = time.time()

                self.screens.update()
                self.input.update()
                self.context.present(self.console.root)

                self.last_update = now

    def engine_update(self):
        for _ in range(20):
            self.clock.update()
            player_turn = self.action_system.update()

            self.path_system.update()

            if player_turn:
                self.fov_system.update()
                self.render_system.update()
                return
