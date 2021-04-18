from __future__ import annotations
from typing import *
import tcod

from anathema.engine.core import BaseGame

from anathema.engine.core.clock import ClockManager
from anathema.engine.core.console import ConsoleManager
from anathema.engine.core.content import ContentManager
from anathema.engine.core.ecs import ECSManager
from anathema.engine.core.input import InputManager
from anathema.engine.core.player import PlayerManager
from anathema.engine.core.renderer import RenderManager
from anathema.engine.core.screens import ScreenManager
from anathema.engine.core.storage import StorageManager
from anathema.engine.core.world import WorldManager

from anathema.engine.systems.action_system import ActionSystem
from anathema.engine.systems.interaction_system import InteractionSystem
from anathema.engine.systems.physics_system import PhysicsSystem


if TYPE_CHECKING:
    pass


CONFIG = {
    'columns': Options.CONSOLE_WIDTH,
    'rows': Options.CONSOLE_HEIGHT,
    'tileset': Options.TILESET,
    'title': Options.TITLE,
    'vsync': Options.VSYNC
}


class Game(BaseGame):

    context: tcod.context.Context

    def __init__(self):
        self.ecs: ECSManager = ECSManager(self)
        self.clock: ClockManager = ClockManager(self)
        self.console: ConsoleManager = ConsoleManager(self)
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

    def run(self):
        self.loop()

    def loop(self):
        with tcod.context.new_terminal(**CONFIG) as self.context:
            while True:
                self.context.present(self.console.root)
