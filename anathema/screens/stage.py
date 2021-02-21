
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from anathema.core.options import Options
from anathema.abstracts import AbstractScreen, T

if TYPE_CHECKING:
    from anathema.core.screens import ScreenManager
    from anathema.core.game import Game


class Stage(AbstractScreen):

    name: str = "STAGE"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game
        self.panels = []

    def on_enter(self) -> None:
        self.game.renderer.clear()
        self.game.fov_system.update(100)
        self.game.render_system.update(100)
        self.game.renderer.terminal.refresh()

    def on_draw(self, dt) -> None:
        self.game.renderer.clear_area(65, 1, 32, 64)
        self.game.renderer.clear_area(1, 49, 64, 16)

        #! Side Panel
        self.game.renderer.draw_box(65, 1, 32, 64, 0xFFFFFFFF)

        #! Log Panel
        self.game.renderer.draw_box(1, 49, 64, 16, 0xFFFFFFFF)

        #! Health
        hp = self.game.player.entity['Health']
        self.game.renderer.print(67, 3, 0xFFFF0000, f"HP: {hp}")

        #! Mana
        mp = self.game.player.entity['Mana']
        self.game.renderer.print(67, 5, 0xFF5C9BED, f"MP: {mp}")

    def on_update(self, dt) -> None:
        self.handle_input()
        self.game.update_engine_systems(dt)

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        self.game.player.move((x, y))

    def cmd_confirm(self) -> Optional[T]:
        self.game.player.entity['Health'].apply_damage(5)

    def cmd_escape(self):
        self.game.screens.replace_screen('MAIN MENU')
