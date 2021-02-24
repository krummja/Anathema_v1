from __future__ import annotations
from typing import Optional

from anathema.abstracts import T
from anathema.screens.stage import Stage


class PlayerReady(Stage):

    name: str = "PLAYER READY"

    def on_enter(self, *args) -> None:
        self.game.fov_system.update(100)
        self.game.render_system.update(100)

    def on_update(self, dt) -> None:
        super().on_update(dt)
        self.game.update_engine_systems(dt)

    def on_draw(self, dt) -> None:
        self.draw_panel_borders()
        self.draw_character_info(65, 2)
        self.draw_stat_block(65, 10)

    def draw_panel_borders(self) -> None:
        self.game.renderer.draw_box(65, 1, 32, 64, 0x44FFFFFF)
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

    def cmd_close(self) -> None:
        nearby = self.game.interaction_system.get_nearby_interactables()
        if len(nearby) > 1:
            # TODO: Handle multiple interactables - raise a selection menu
            pass
        else:
            self.game.player.close(nearby[0])

    def cmd_escape(self) -> None:
        self.game.screens.replace_screen('MAIN MENU')

    def cmd_inventory(self) -> None:
        self.game.screens.replace_screen("MENU OVERLAY", "inventory")

    def cmd_move(self, x: int, y: int) -> None:
        self.game.player.move((x, y))
