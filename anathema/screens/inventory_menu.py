from __future__ import annotations

from anathema.screens.menu_overlay import MenuOverlay


class InventoryMenu(MenuOverlay):
    name: str = "INVENTORY"
    _data = None
    _selection: int = 0
    _layout = {'x': 33, 'y': 1, 'w': 32, 'h': 48}

    def on_enter(self) -> None:
        self._data = self.game.player.entity['Inventory'].contents

    @property
    def data(self):
        _data = {}
        for i, d in enumerate(self._data):
            _data[i] = d
        return _data

    @property
    def selection(self) -> int:
        return self._selection

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = min(max(0, value), len(self.data) - 1)

    def draw_menu_list(self):
        for i in range(0, len(self._data) * 2, 2):
            self.game.renderer.print(
                x=self._layout['x'] + 5,
                y=self._layout['y'] + 3 + i,
                color=0xFFFFFFFF,
                string=self.data[i//2]['Noun'].noun_text
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
                    string=self.data[self.selection]['Noun'].noun_text
                    )

    def on_draw(self, dt) -> None:
        self.game.renderer.draw_box(**self._layout, color=0x44FFFFFF)
        self.game.renderer.print(
            x=self._layout['x'] - 1,
            y=self._layout['y'],
            color=0xFFFFFFFF,
            string=' Inventory '
            )
        self.draw_menu_list()
        super().on_draw(dt)

    def select(self):
        if len(self.data) > 0:
            return self.data[self.selection]
        else:
            pass

    def cmd_move(self, x: int, y: int) -> None:
        self.selection += y

    def cmd_confirm(self) -> None:
        selection = self.select()
        if selection:
            evt = selection.fire_event('get_interactions', {'expect': []})
            self.game.screens.push_screen(
                'ITEM INFO',
                evt.data['expect'],
                self._data[self.selection]
                )


class ItemInfo(MenuOverlay):
    name: str = "ITEM INFO"
    _data = None
    _item = None
    _selection: int = 0
    _layout = {'x': 33, 'y': 1, 'w': 32, 'h': 0}

    def on_enter(self, *args):
        if args[0]:
            self._data = args[0]
        if args[1]:
            self._item = args[1]

    @property
    def data(self):
        _data = {}
        for i, d in enumerate(self._data):
            _data[i] = d
        return _data

    @property
    def selection(self) -> int:
        return self._selection

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = min(max(0, value), len(self.data) - 1)

    def draw_menu_list(self):
        for i in range(0, len(self._data) * 2, 2):
            self.game.renderer.print(
                x=self._layout['x'] + 5,
                y=self._layout['y'] + 3 + i,
                color=0xFFFFFFFF,
                string=self.data[i//2]['name']
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
                    string=self.data[self.selection]['name']
                    )

    def on_draw(self, dt) -> None:
        self._layout['h'] = 5 + (len(self.data) * 2)
        self.game.renderer.draw_box(**self._layout, color=0x44FFFFFF)
        self.game.renderer.print(
            x=self._layout['x'] - 1,
            y=self._layout['y'],
            color=0xFFFFFFFF,
            string=f" {self._item['Noun'].noun_text}"
            )
        self.draw_menu_list()
        super().on_draw(dt)

    def select(self):
        if len(self.data) > 0:
            return self.data[self.selection]['evt']
        else:
            pass

    def cmd_move(self, x: int, y: int) -> None:
        self.selection += y

    def cmd_confirm(self) -> None:
        selection = self.select()
        if selection:
            self._item.fire_event(selection, {})
