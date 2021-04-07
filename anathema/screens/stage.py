import nocterminal as noc
from morphism import Point


class StageScreen(noc.ui.Screen):

    def terminal_update(self, is_active=False):
        self.director.context.print(Point(1, 10), "Stage Test!")
        return True

    def terminal_read(self, char):
        if char == noc.terminal.TK_ESCAPE:
            self.director.pop_screen()
