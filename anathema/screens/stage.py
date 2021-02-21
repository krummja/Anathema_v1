
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
        self.draw_panel_borders()
        self.draw_character_info(65, 2)
        self.draw_stat_block(65, 10)

    def draw_panel_borders(self) -> None:

        self.game.renderer.clear_area(64, 0, 32, 64)
        self.game.renderer.clear_area(0, 48, 64, 16)

        #! Side Panel
        self.game.renderer.draw_box(65, 1, 32, 64, 0x44FFFFFF)
        #! Log Panel
        self.game.renderer.draw_box(1, 49, 64, 16, 0x44FFFFFF)

    def draw_character_info(self, x: int, y: int) -> None:
        x_margin = 2
        x = x + x_margin

        name = self.game.player.entity['Name']
        self.game.renderer.print(x, y, 0xFFFFFFFF, name.noun_text)

        background = self.game.player.entity['Background']
        self.game.renderer.print(x, y+2, 0x88FFFFFF, f"{background.culture} {background.path}")

    def draw_stat_block(self, x: int, y: int) -> None:
        x_margin = 2
        x = x + x_margin
        bar_offset = 15

        #! Health
        hp = self.game.player.entity['Health']
        self.game.renderer.print(x, y, 0xFFFF0000, f"HP: {hp}")
        self.game.renderer.draw_bar(x + bar_offset, y, 10, hp.current, hp.maximum, 0xFF0000)

        #! Mana
        mp = self.game.player.entity['Mana']
        self.game.renderer.print(x, y+2, 0xFF5C9BED, f"MP: {mp}")
        self.game.renderer.draw_bar(x + bar_offset, y+2, 10, mp.current, mp.maximum, 0x5C9BED)

        #! Stamina
        sp = self.game.player.entity['Stamina']
        self.game.renderer.print(x, y+4, 0xFFABEB34, f"SP: {sp}")
        self.game.renderer.draw_bar(x + bar_offset, y+4, 10, sp.current, sp.maximum, 0xABEB34)

    def on_update(self, dt) -> None:
        self.handle_input()
        self.game.update_engine_systems(dt)

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        self.game.player.move((x, y))

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self):
        self.game.screens.replace_screen('MAIN MENU')
