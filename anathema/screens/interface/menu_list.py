
class Selector:

    def __init__(self, data) -> None:
        self.data = data
        self._selection = 0

    @property
    def selection(self) -> int:
        return int(self._selection)

    @selection.setter
    def selection(self, value: int) -> None:
        self._selection = min(max(0, value), len(self.data) - 1)


class MenuList:

    selected = 0xFFFF00FF
    unselected = 0xFFFFFFFF

    def __init__(self, x: int, y: int, w: int, h: int, title: str, data, spread: int = 2) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.data = data
        self.spread = spread
        self.selector = Selector(data)

    def draw(self, renderer):
        renderer.draw_box(self.x, self.y, self.w, self.h, 0x44FFFFFF)
        renderer.print(self.x-1, self.y, 0xFFFFFFFF, self.title)
        self.draw_menu_list(renderer)

    def draw_menu_list(self, renderer) -> None:
        for i in range(0, len(self.data) * 2, self.spread):
            renderer.print(self.x+5, self.y+3+i, self.unselected, self.data[i//self.spread]['Noun'].noun_text)
            if self.selector.selection == i//2:
                renderer.print(self.x+2, self.y+3+i, self.selected, ">")
                renderer.print(self.x+5, self.y+3+i, self.selected, self.data[self.selector.selection]['Noun'].noun_text)

    def select(self):
        return self.data[self.selector.selection]
