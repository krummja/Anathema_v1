import nocterminal as noc
from nocterminal.ui import *


class CharacterCreationScreen(noc.ui.UIScreen):

    def __init__(self):

        self.left_margin = 12

        view = WindowView(
            'Character',
            layout=LayoutOptions(top=7, right=10, bottom=7, left=10),
            subviews=[

                LabelView(
                    text='Name:',
                    align_horz='left',
                    layout=LayoutOptions(
                        left=1, height=1, top=1, bottom=None)),
                TextInputView(
                    callback=lambda t: print(t),
                    layout=LayoutOptions(
                        left=self.left_margin, height=1, top=1, bottom=None, right=40)),

                LabelView(
                    text='Surname:',
                    align_horz='left',
                    layout=LayoutOptions(
                        left=1, height=1, top=3, bottom=None)),
                TextInputView(
                    callback=lambda t: print(t),
                    layout=LayoutOptions(
                        left=self.left_margin, height=1, top=3, bottom=None, right=40)),

                ButtonView(
                    text='Continue',
                    callback=lambda: print("Next"),
                    layout=LayoutOptions.row_bottom(2).with_updates(left=0.6)),
                ButtonView(
                    text='Cancel',
                    callback=lambda: self.director.pop_screen(),
                    layout=LayoutOptions.row_bottom(2).with_updates(left=0.9)),

                ]
            )

        super().__init__(view)
        self.covers_screen = True

    def back(self):
        self.director.pop_screen()

    def next(self):
        pass
