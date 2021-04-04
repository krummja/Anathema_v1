from __future__ import annotations

from anathema.screens.menu_overlay import MenuOverlay


class EquipmentMenu(MenuOverlay):
    name: str = "EQUIPMENT"
    _data = None
    _selection = 0
    _layout = {'x': 1, 'y': 1, 'w': 32, 'h': 48}

    def on_enter(self):
        self._data = self.game.player.entity['Body'].body_parts

    @property
    def data(self):
        _data = {}
        for i, d in enumerate(self._data):
            _data[i] = d
        return _data

    # TODO Make this prop and its setter a mixin?
    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = min(max(0, value), len(self.data) - 1)

    def draw_menu_list(self):
        # Display slot name if empty
        # Else display item in slot
        # When selected, slot names should open an equip menu
        for i in range(0, len(self._data) * 2, 2):
            self.game.renderer.print(
                x=self._layout['x'] + 5,
                y=self._layout['y'] + 3 + i,
                color=0xFFFFFFFF,
                string=self.data[i//2].upper()
                )
            if self.selection == i//2:
                self.game.renderer.print(
                    x=self._layout['x']+2,
                    y=self._layout['y']+3+i,
                    color=0xFFFF00FF,
                    string=">"
                    )
                self.game.renderer.print(
                    x=self._layout['x'] + 5,
                    y=self._layout['y'] + 3 + i,
                    color=0xFFFF00FF,
                    string=self.data[self.selection].upper()
                    )

    def on_draw(self, dt):
        self.game.renderer.draw_box(**self._layout, color=0x44FFFFFF)
        self.game.renderer.print(
            x=self._layout['x'] - 1,
            y=self._layout['y'],
            color=0xFFFFFFFF,
            string=' Equipment '
            )
        self.draw_menu_list()
        super().on_draw(dt)

    def select(self):
        if len(self.data) > 0:
            return self.data[self.selection]
        else:
            pass

    def cmd_move(self, x: int, y: int):
        self.selection += y

    def cmd_confirm(self):
        selection = self.select()
        if selection:
            print("Selection")
