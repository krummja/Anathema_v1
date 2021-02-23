from __future__ import annotations

from anathema.screens import PlayerReady


class MenuOverlay(PlayerReady):

    name: str = "MENU OVERLAY"

    def on_draw(self, dt) -> None:
        super().on_draw(dt)
        self.game.renderer.draw_box(1, 1, 20, 20, 0x44FFFFFF)

    def cmd_escape(self) -> None:
        self.game.screens.replace_screen("PLAYER READY")

    def cmd_inventory(self):
        pass

    def cmd_move(self, x: int, y: int) -> None:
        pass
