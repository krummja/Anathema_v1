from __future__ import annotations

from anathema.core.options import Options
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
        self.draw_stat_block(65, 7)
        self.draw_log()
        # self.draw_equipment_overview(65, 15)

    def draw_panel_borders(self) -> None:
        self.game.renderer.draw_box(65, 1, 32, 64, 0x44FFFFFF)
        self.game.renderer.draw_box(1, 49, 64, 16, 0x44FFFFFF)

    def draw_log(self) -> None:
        y_index = 0
        x, y = 1, Options.SCREEN_HEIGHT - 2

        self.game.renderer.clear_area(2, 50, 62, 14)
        self.game.renderer.clear_area(2, 63, 62, 1)
        messages = [msg for msg in self.game.log.log[::1]]

        if messages:
            message = messages[-1]
            self.game.renderer.print(x, y, 0xFFFFFFFF, str(message))

        messages = [msg for msg in self.game.log.log[-2::-1]]
        for text in messages:
            y_index += 1
            if y_index >= 14:
                break
            self.game.renderer.print(x, y - y_index, 0x66FFFFFF, str(text))
        # NOTE Use "terminal.measure" to get line length for wrapping

    def draw_character_info(self, x: int, y: int) -> None:
        x_margin = 2
        x = x + x_margin

        name = self.game.player.entity['Noun']
        self.game.renderer.print(x, y, 0xFFFFFFFF, name.noun_text)

        background = self.game.player.entity['Background']
        self.game.renderer.print(x, y+2, 0x88FFFFFF, f"{background.culture} {background.path}")

    def draw_stat_block(self, x: int, y: int) -> None:
        x_margin = 2
        x = x + x_margin
        bar_offset = 15

        # Health
        hp = self.game.player.entity['Health']
        self.game.renderer.print(x, y, 0xFFFF0000, f"HP: {hp}")
        self.game.renderer.draw_bar(x + bar_offset, y, 10, hp.current, hp.maximum, 0xFF0000)

        # Mana
        mp = self.game.player.entity['Mana']
        self.game.renderer.print(x, y+2, 0xFF5C9BED, f"MP: {mp}")
        self.game.renderer.draw_bar(x + bar_offset, y+2, 10, mp.current, mp.maximum, 0x5C9BED)

        # Stamina
        sp = self.game.player.entity['Stamina']
        self.game.renderer.print(x, y+4, 0xFFABEB34, f"SP: {sp}")
        self.game.renderer.draw_bar(x + bar_offset, y+4, 10, sp.current, sp.maximum, 0xABEB34)

    def draw_equipment_overview(self, x: int, y: int) -> None:
        x_margin = 2
        x = x + x_margin

        head = self.game.player.entity['Head']
        torso = self.game.player.entity['Torso']
        back = self.game.player.entity['Back']
        arms = self.game.player.entity['Arms']
        hands = self.game.player.entity['Hands']
        legs = self.game.player.entity['Legs']
        feet = self.game.player.entity['Feet']

        self.game.renderer.print(x, y,    0xFFFFFFFF, ' Head')
        self.game.renderer.print(x, y+2,  0xFFFFFFFF, 'Torso')
        self.game.renderer.print(x, y+4,  0xFFFFFFFF, ' Back')
        self.game.renderer.print(x, y+6,  0xFFFFFFFF, ' Arms')
        self.game.renderer.print(x, y+8,  0xFFFFFFFF, 'Hands')
        self.game.renderer.print(x, y+10, 0xFFFFFFFF, ' Legs')
        self.game.renderer.print(x, y+12, 0xFFFFFFFF, ' Feet')

        self.game.renderer.print(
            x+8, y,
            0xFFFFFFFF if head.equipped_name else 0x88FFFFFF,
            head.equipped_name if head.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+2,
            0xFFFFFFFF if torso.equipped_name else 0x88FFFFFF,
            torso.equipped_name if torso.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+4,
            0xFFFFFFFF if back.equipped_name else 0x88FFFFFF,
            back.equipped_name if back.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+6,
            0xFFFFFFFF if arms.equipped_name else 0x88FFFFFF,
            arms.equipped_name if arms.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+8,
            0xFFFFFFFF if hands.equipped_name else 0x88FFFFFF,
            hands.equipped_name if hands.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+10,
            0xFFFFFFFF if legs.equipped_name else 0x88FFFFFF,
            legs.equipped_name if legs.equipped_name else "<empty>")

        self.game.renderer.print(
            x+8, y+12,
            0xFFFFFFFF if feet.equipped_name else 0x88FFFFFF,
            feet.equipped_name if feet.equipped_name else "<empty>")

    def cmd_close(self) -> None:
        nearby = self.game.interaction_system.get_nearby_interactables()
        if len(nearby) > 1:
            # TODO: Handle multiple interactables - raise a selection menu
            pass
        else:
            self.game.player.close(nearby[0])

    def cmd_escape(self) -> None:
        self.game.screens.pop_screen()

    def cmd_inventory(self) -> None:
        self.game.screens.push_screen("INVENTORY")

    def cmd_equipment(self) -> None:
        self.game.screens.push_screen("EQUIPMENT")

    def cmd_examine(self):
        self.game.screens.push_screen("PICK LOCATION")

    def cmd_move(self, x: int, y: int) -> None:
        self.game.player.move((x, y))

    def cmd_pickup(self) -> None:
        self.game.player.pickup()
