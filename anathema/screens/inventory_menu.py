from __future__ import annotations

from anathema.screens.menu_overlay import MenuOverlay


class InventoryMenu(MenuOverlay):
    name: str = "INVENTORY"
    menus = []

    @property
    def active(self):
        return self.menus[-1]

    def push_menu(self, menu):
        self.menus.append(menu)

    def pop_menu(self):
        self.menus.pop()

    def on_enter(self) -> None:
        data = self.game.player.entity['Inventory'].contents
        menu_data = {}
        for i, d in enumerate(data):
            menu_data[i] = d
        # menu = MenuList(33, 1, 32, 48, " Inventory ", menu_data)
        # self.push_menu(menu)

    def on_draw(self, dt) -> None:
        self.active.draw(self.manager.game.renderer)
        super().on_draw(dt)

    def cmd_move(self, x: int, y: int) -> None:
        self.active.selector.selection += y

    def cmd_confirm(self) -> None:
        selection = self.active.select()
        evt = selection.fire_event('get_interactions',
                                   {'expect': []})
        option_data = {}
        for i, d in enumerate(evt.data['expect']):
            option_data[i] = d
        # options = OptionList(33, 1, 32, 48, f" {selection['Noun'].noun_text} ", option_data)
        # self.push_menu(options)

    def cmd_pickup(self) -> None:
        pass
