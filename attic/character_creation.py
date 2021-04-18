import nocterminal as noc
from nocterminal.ui import *
from anathema.utils.print_utils import bcolors


class CharacterCreationScreen(noc.ui.UIScreen):

    CHARACTER_CONFIGURATION = {
        'Background': [
            'Nobility',
            'Beggar',
            'Scholar',
            'Laborer',
            ],
        'Path': [
            'Sorcerer',
            'Arcanist',
            'Artificer',
            'Alchemist',
            'Spellsword',
            ]
        }

    def __init__(self):

        self.left_margin = 12
        self.character_data = {
            'name': "",
            'surname': "",
            'background': "Nobility",
            'path': "Sorcerer",
            }

        view = WindowView(
            'Create New Character',
            layout=LayoutOptions(top=7, right=10, bottom=7, left=10),
            subviews=[

                # Name Input
                LabelView(
                    text='Name:',
                    align_horz='left',
                    layout=LayoutOptions(
                        left=1, height=1, top=1, bottom=None)),
                TextInputView(
                    callback=lambda t: self.set_name(t),
                    layout=LayoutOptions(
                        left=self.left_margin, height=1, top=1, bottom=None, right=40)),

                # Surname Input
                LabelView(
                    text='Surname:',
                    align_horz='left',
                    layout=LayoutOptions(
                        left=1, height=1, top=3, bottom=None)),
                TextInputView(
                    callback=lambda t: self.set_surname(t),
                    layout=LayoutOptions(
                        left=self.left_margin, height=1, top=3, bottom=None, right=40)),

                SettingsListView(
                    label_control_pairs=[
                        (label, CyclingButtonView(
                            options=value,
                            initial_value=value[0],
                            callback=(lambda _: None),
                            align_horz='left'))
                        for label, value in sorted(self.CHARACTER_CONFIGURATION.items())
                        ],
                    value_column_width=10,
                    max_height = 8,
                    layout=LayoutOptions(left=2, height=8, top=8, bottom=None, right=40)),

                # Navigation
                ButtonView(
                    text='Continue',
                    callback=self.next,
                    layout=LayoutOptions.row_bottom(2).with_updates(left=0.6)),
                ButtonView(
                    text='Cancel',
                    callback=lambda: self.director.pop_screen(),
                    layout=LayoutOptions.row_bottom(2).with_updates(left=0.9)),

                ]
            )

        super().__init__(view)
        self.covers_screen = True

    def set_name(self, text: str = "") -> None:
        self.character_data['name'] = text

    def set_surname(self, text: str = "") -> None:
        self.character_data['surname'] = text

    def back(self):
        self.director.pop_screen()

    def next(self):
        character_name = f"{self.character_data['name']} {self.character_data['surname']}"
        print(f"Creating character {bcolors.BOLD}{bcolors.HEADER}{character_name}{bcolors.ENDC}{bcolors.ENDC} "
              f"[{self.character_data['background']}, {self.character_data['path']}]")
        print(f"{bcolors.OKGREEN}Character saved!{bcolors.ENDC}")
