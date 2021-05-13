from __future__ import annotations
from typing import *
import numpy as np
import tcod
import copy

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView, CyclingButtonView
from anathema.interface.views.collection_list import SettingsListView
from anathema.engine.core.input import LoopExit
from anathema.data import *
from anathema.storage import Storage

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


CHARACTER_CONFIGURATION = {
    'Background': [
        "Commoner"
        ],
    'Path': [
        "Adventurer"
        ]
    }


class NewCharacter(UIScreen):

    def __init__(self, game: Game) -> None:
        views = [
            RectView(
                layout = Layout(left = 20, right = 5, top = 5, bottom = 5),
                subviews = [
                    SettingsListView(
                        label_control_pairs = [
                            (label, CyclingButtonView(
                                key = label,
                                options = value,
                                initial_value = value[0],
                                callback = self.ui_mock_value,
                                align_horz = 'left'))
                            for label, value in sorted(CHARACTER_CONFIGURATION.items())
                        ],
                        value_column_width = 15,
                        layout = Layout(top = 10, left = 2, width = 30, right = None, height = 6, bottom = None)
                    ),

                    ButtonView(
                        "Back", align_horz = "left", align_vert = "bottom",
                        callback = self.ui_back,
                        layout = Layout.row_bottom(3).with_updates(left = 2, bottom = 2)
                    ),

                    ButtonView(
                        "Accept", align_horz = "left", align_vert = "bottom",
                        callback = self.ui_accept,
                        layout = Layout.row_bottom(3).with_updates(left = 8, bottom = 2)
                    )
                ]
            )
        ]
        super().__init__(name="NEW CHARACTER", game=game, views=views)

    def ui_mock_value(self, k, v):
        print(f"{k}: {v}")

    def ui_back(self):
        self.game.screens.pop_screen()

    def ui_accept(self):
        self.game.player.initialize()
        self.game.session.data.character_save = CharacterSave(
            name = "Test Player",
            level = 1,
            uid = self.game.player.uid,
            world_id = self.game.session.data.world_save.world_id,
            entity = copy.copy(self.game.player.entity)
        )
        Storage.write_to_file(self.game.session)
        self.game.screens.replace_screen(self.game.screens.screens["MAIN MENU"])
