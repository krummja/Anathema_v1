import nocterminal as noc

from screens.stage import StageScreen


class MainMenuScreen(noc.ui.UIScreen):

    def __init__(self):
        views = [
            noc.ui.LabelView("Anathema", align_vert="top", align_horz="left",
                             layout=noc.ui.LayoutOptions(left=10, top=10), large=True),
            noc.ui.ButtonView("Play", callback=self.play,
                              layout=noc.ui.LayoutOptions.row_bottom(12).with_updates(
                                  left=0.2, width=0.2, right=None)),
            noc.ui.ButtonView("Quit", callback=self.quit,
                              layout=noc.ui.LayoutOptions.row_bottom(12).with_updates(
                                  left=0.6, width=0.2, right=None)),
            ]
        super().__init__(views)

    def become_active(self):
        self.director.context.clear()

    def play(self):
        self.director.push_screen(StageScreen())

    def quit(self):
        self.director.pop_screen()
