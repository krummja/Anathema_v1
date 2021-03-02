from __future__ import annotations
from typing import Tuple
import math

from anathema.screens.player_ready import PlayerReady
from anathema.core.options import Options


class PickLocation(PlayerReady):
    """Screen raised when selecting a visible tile."""

    name: str = "PICK LOCATION"

    start_xy: Tuple[int, int]
    cursor_xy: Tuple[int, int]
    desc: str

    def on_enter(self):
        self.start_xy = self.manager.game.player.position
        self.cursor_xy = self.start_xy
        self.make_description()

    def on_draw(self, dt) -> None:
        x = self.cursor_xy[0]
        y = self.cursor_xy[1]
        self.manager.game.renderer.clear_area(0, 0, Options.STAGE_WIDTH, Options.STAGE_HEIGHT)

        # Selection reticle
        self.manager.game.renderer.print(x-1, y-1, 0xFFFF0000, chr(0x250C))
        self.manager.game.renderer.print(x+1, y-1, 0xFFFF0000, chr(0x2510))
        self.manager.game.renderer.print(x-1, y+1, 0xFFFF0000, chr(0x2514))
        self.manager.game.renderer.print(x+1, y+1, 0xFFFF0000, chr(0x2518))

        # Selection content
        self.manager.game.renderer.print(1, 1, 0xFFFFFFFF, self.desc)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        x += self.cursor_xy[0]
        y += self.cursor_xy[1]
        x = min(max(0, x), Options.STAGE_WIDTH)
        y = min(max(0, y), Options.STAGE_HEIGHT)
        if not self.manager.game.fov_system.visible[x, y]:
            self.cursor_xy = self.cursor_xy
        else:
            self.cursor_xy = x, y

        self.make_description()

    def make_description(self):
        target_list = self.manager.game.physics_system.entity_at_pos(*self.cursor_xy)
        target_list = [self.manager.game.ecs.engine.get_entity(uid) for uid in target_list]

        desc_list = []
        for entity in target_list:
            if entity.has('Noun'):
                desc_list.append(entity['Noun'].noun_text)
        self.desc = "\n".join(desc_list)

    def cmd_confirm(self) -> Tuple[int, int]:
        dx = abs(self.cursor_xy[0] - self.manager.game.player.position[0])
        dy = abs(self.cursor_xy[1] - self.manager.game.player.position[1])

        if dx <= 1 and dy <= 1:
            data = (dx, dy)
        else:
            data = None

        self.manager.game.screens.pop_screen()
        return self.cursor_xy

    def cmd_escape(self) -> None:
        self.manager.game.screens.pop_screen()
