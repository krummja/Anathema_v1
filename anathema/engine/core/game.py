from __future__ import annotations
from typing import *
import tcod
import os

from anathema.engine.core.camera import CameraManager
from anathema.engine.core.clock import ClockManager
from anathema.engine.core.console import ConsoleManager
from anathema.engine.core.content import ContentManager
from anathema.engine.core.ecs import ECSManager
from anathema.engine.core.input import InputManager, LoopExit
from anathema.engine.core.player import PlayerManager
from anathema.engine.core.renderer import RenderManager
from anathema.engine.core.screens import ScreenManager
from anathema.engine.core.storage import StorageManager
from anathema.engine.core.world import WorldManager

from anathema.engine.systems.action_system import ActionSystem
from anathema.engine.systems.interaction_system import InteractionSystem
from anathema.engine.systems.physics_system import PhysicsSystem
from anathema.engine.systems.fov_system import FOVSystem
from anathema.engine.systems.render_system import RenderSystem
from anathema.engine.systems.path_system import PathSystem

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


class Game:

    debug = False
    context: tcod.context.Context

    def __init__(self):
        self.ecs: ECSManager = ECSManager(self)
        self.clock: ClockManager = ClockManager(self)
        self.console: ConsoleManager = ConsoleManager(self)
        self.camera: CameraManager = CameraManager(self)
        self.renderer: RenderManager = RenderManager(self)
        self.screens: ScreenManager = ScreenManager(self)
        self.input: InputManager = InputManager(self)
        self.world: WorldManager = WorldManager(self)
        self.player: PlayerManager = PlayerManager(self)

        self.content: ContentManager = ContentManager(self)
        self.storage: StorageManager = StorageManager(self)

        self.action_system: ActionSystem = ActionSystem(self)
        self.physics_system: PhysicsSystem = PhysicsSystem(self)
        self.interaction_system: InteractionSystem = InteractionSystem(self)
        self.fov_system: FOVSystem = FOVSystem(self)
        self.render_system: RenderSystem = RenderSystem(self)
        self.path_system: PathSystem = PathSystem(self)

    def run(self):
        print("Starting...")
        self.content.load_prefabs(path="content/prefabs/")
        self.screens.replace_screen(self.screens.screens['MAIN MENU'])
        self.loop()

    def loop(self):
        with tcod.context.new(**CONFIG) as self.context:
            print("Welcome to Anathema.")
            while self.screens.should_continue:
                self.screens.update()
                self.context.present(self.console.root)
                self.input.update()

    def player_update(self):
        self.clock.update()
        player_turn = self.action_system.update()
        if player_turn:
            self.systems_update()

    def systems_update(self):
        self.physics_system.update()
        self.interaction_system.update()
        self.path_system.update()
        self.fov_system.update()
        self.render_system.update()
