from __future__ import annotations
from typing import *
import numpy as np
import tcod

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView, CyclingButtonView
from anathema.interface.views.collection_list import SettingsListView
from anathema.engine.core.input import LoopExit

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


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


class TestScreen(UIScreen):

    name = "TEST"

    def __init__(self, game: Game) -> None:
        views = [
            SettingsListView(
                label_control_pairs=[
                    (label, CyclingButtonView(
                        options = value,
                        initial_value = value[0],
                        callback = (lambda value: print(value)),
                        align_horz = 'left'))
                    for label, value in sorted(CHARACTER_CONFIGURATION.items())
                ],
                value_column_width=30,
                layout=Layout(left=10, right=10, top=5, bottom=5)
            )
        ]
        super().__init__(name="MAIN MENU", game=game, views=views)

