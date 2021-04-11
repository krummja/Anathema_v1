import nocterminal as noc

from screens.character_creation import CharacterCreationScreen
from screens.stage import StageScreen


class MainMenuScreen(noc.ui.UIScreen):

    def __init__(self):
        views = [
            noc.ui.LabelView("Anathema", align_vert="top", align_horz="left",
                             layout=noc.ui.LayoutOptions(left=10, top=10), large=True),
            noc.ui.ButtonView("Start New", callback=self.create, align_horz="left",
                              layout=noc.ui.LayoutOptions(left=10, top=20)),
            noc.ui.ButtonView("Load", callback=self.load, align_horz="left",
                              layout=noc.ui.LayoutOptions(left=10, top=24)),
            noc.ui.ButtonView("Options", callback=self.options, align_horz="left",
                              layout=noc.ui.LayoutOptions(left=10, top=28)),
            noc.ui.ButtonView("Quit", callback=self.quit, align_horz="left",
                              layout=noc.ui.LayoutOptions(left=10, top=32)),
            ]
        super().__init__(views)
        self.covers_screen = True

    def become_active(self):
        self.director.context.clear()
        self.terminal_update()

    def terminal_update(self, is_active=False):
        self.director.context.clear()
        super().terminal_update()

    def create(self):
        self.director.push_screen(CharacterCreationScreen())

    def load(self):
        self.director.start()
        self.director.push_screen(StageScreen())

    def options(self):
        pass

    def quit(self):
        self.director.pop_screen()
