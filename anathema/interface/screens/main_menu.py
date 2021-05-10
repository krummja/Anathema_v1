from __future__ import annotations
from typing import *
import numpy as np
import tcod
from enum import Enum

from morphism import *

from anathema.engine.core.options import Options
from anathema.interface.screens import UIScreen
from anathema.interface.views import Layout, View
from anathema.interface.views.rect_view import RectView
from anathema.interface.views.label_view import LabelView
from anathema.interface.views.button_view import ButtonView
from anathema.interface.views.collection_list import SettingsListView
from anathema.engine.core.input import LoopExit
from anathema.data import CharacterSave, GameData, Storage, CharacterRegistry, get_data, get_save_manifest

if TYPE_CHECKING:
    from anathema.engine.core.game import Game


POSITION_RECT = Rect(Point(0, 0), Size(Options.CONSOLE_WIDTH, Options.CONSOLE_HEIGHT))


class LogoView(View):

    def draw(self):
        logo = [
            "          █                                                                ",
            "          █                                                                ",
            "          █                                                                ",
            "          █                                                                ",
            "          █                                                                ",
            "          █                                                                ",
            "          █                                                                ",
            "   █      █                                                                ",
            "          █                                                                ",
            "     █   ███      ████████                                                 ",
            "      ██ ███   ██████████████                                              ",
            "      ██ █████████████████████                                             ",
            "        ████████████████████████                                           ",
            "     ██████████████        ██████                                          ",
            "████████████████              ████                                         ",
            "     ██████████                ███                                         ",
            "       ██████                    ██                                        ",
            "       █████                      ██                                       ",
            "       █████                █      ██                                      ",
            "       █████                ██     ██                                      ",
            "       ████                █ █      █                                      ",
            "      ████                 ████      █                                     ",
            "      ████                ██ █ █     █                                     ",
            "      ████                █  █  █    █                                     ",
            "      ███                 █ ██   █                                         ",
            "      ███                █ █  █   █                                        ",
            "      ███                ██   ██   █                                       ",
            "      ███                █   █  █   ██                                     ",
            "      ███               █   █   ██    █                                    ",
            "       ██           █   █  █   █  █    ██                                  ",
            "       ██          █ ███  █   █   ██     ██   ██                           ",
            "       ███         ██  █ █   █   █ █       ███  █                          ",
            "        ██        █ ██  █   █   █  █          █  █                         ",
            "         █        ██ █   ███   █   █          █ █ ██                       ",
            "         ██      ██  ██    █  █   ██           █   ██                      ",
            "          ██     █  █ █     ██   █ █            █ █  ██                    ",
            "           █     █ █  ██     ██ █   █            █    ███                  ",
            "            █   █ █  █  ██     █   █ █            ██ █   ██                ",
            "               █ █  █  █  █     █ █   ██            █   █  ██              ",
            "           ██████  █  █  █ ███████   █  █████████████  █  █ ██████████████",
        ]

        for x in range(74):
            for y in range(40):
                self.console.put_char(x + 1, y + 1, ord(logo[y][x]))


class MenuStates(Enum):
    NO_WORLD = 0
    NO_CHARACTER = 1
    READY = 2


class MainMenu(UIScreen):

    def __init__(self, game: Game) -> None:
        self.menu_state = MenuStates.NO_WORLD
        self.menu_updated = False

        # LOGO
        self.logo_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(bottom = POSITION_RECT.relative_point(1.0, 0.33)[1]),
            subviews = [LogoView()])

        # MAIN MENU
        self.start_button = ButtonView(
            "Start", callback = self.ui_start,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))
        self.no_start_label = LabelView(
            "Start", fg = (155, 155, 155),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 8, left = 2))
        self.world_button = ButtonView(
            "World", callback = self.ui_world_menu,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 6, left = 2))
        self.character_button = ButtonView(
            "Character", callback = self.ui_character_menu,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 4, left = 2))
        self.no_character_label = LabelView(
            "Character", fg = (155, 155, 155),
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 4, left = 2))
        self.quit_game_button = ButtonView(
            "Quit Game", callback = self.ui_quit,
            align_horz = "left", align_vert = "bottom",
            layout = Layout(bottom = 2, left = 2))

        self.menu_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                            right = POSITION_RECT.relative_point(0.66, 1.0)[0] + 1),
            subviews = [])

        # WORLD AND CHARACTER INFORMATION
        self.world_label = LabelView(
            "", align_horz = "left", align_vert = "bottom",
            layout = Layout.row_top(1.0).with_updates(top = None, bottom = 4, left = 2))

        self.character_label = LabelView(
            "", align_horz = "left", align_vert = "bottom",
            layout = Layout.row_top(1.0).with_updates(top = None, bottom = 2, left = 2))

        self.character_box = RectView(
            fg = (21, 21, 21),
            layout = Layout(
                top = POSITION_RECT.relative_point(1.0, 0.66)[1] + 1,
                left = POSITION_RECT.relative_point(0.33, 1.0)[0] + 1
            ),
            subviews = [
                self.world_label,
                self.character_label
            ]
        )

        super().__init__(name = "MAIN MENU", game = game, views = [
            self.logo_box,
            self.menu_box,
            self.character_box,
        ])

    def on_enter(self, *args):
        manifest = Storage.manifest

        if manifest["saves"].keys():
            try:
                saves = [file for file in manifest["saves"].keys()]
                game_data: GameData = Storage.load_from_file(saves[-1])
                if game_data:
                    self.game.session.game_data = game_data
                    self.game.session.load_game_data()
            except IndexError:
                print("No game data found!")

    def post_update(self):
        if self.game.session.world_data:
            if self.game.session.character_data:
                if self.menu_state != MenuStates.READY:
                    self.menu_state = MenuStates.READY
                    self.menu_state = False
            else:
                if self.menu_state != MenuStates.NO_CHARACTER:
                    self.menu_state = MenuStates.NO_CHARACTER
                    self.menu_updated = False
        else:
            if self.menu_state != MenuStates.NO_WORLD:
                self.menu_state = MenuStates.NO_WORLD
                self.menu_updated = False

        if not self.menu_updated:
            self.menu_box.remove_subviews([v for v in self.menu_box.subviews])
            if self.menu_state == MenuStates.NO_WORLD:
                self.world_label.update("-- NO WORLD DATA  --")
                self.world_button.callback = self.ui_world_menu
                self.menu_box.add_subviews([
                    self.no_start_label,
                    self.world_button,
                    self.no_character_label,
                    self.quit_game_button,
                ])
                self.world_button.did_become_first_responder()
            elif self.menu_state == MenuStates.NO_CHARACTER:
                self.world_label.update(self.game.session.world_data.world_id)
                self.character_label.update("-- NO CHARACTER --")
                self.menu_box.add_subviews([
                    self.no_start_label,
                    self.world_button,
                    self.character_button,
                    self.quit_game_button,
                ])
                self.world_button.did_become_first_responder()
            elif self.menu_state == MenuStates.READY:
                self.character_label.update(self.game.session.character_data.name)
                self.menu_box.add_subviews([
                    self.start_button,
                    self.world_button,
                    self.character_button,
                    self.quit_game_button
                ])
                self.start_button.did_become_first_responder()
            self.view.find_next_responder()
            self.menu_box.set_needs_layout(True)
            self.menu_box.perform_layout()
            self.menu_updated = True

    def ui_world_menu(self):
        new_world = ButtonView(
            "New", callback = self.ui_new_world,
            align_vert = "top",
            align_horz = "left",
            layout = Layout(top = 2, left = 2)
        )
        load_world = ButtonView(
            "Load", callback = self.ui_load_world,
            align_vert = "top",
            align_horz = "left",
            layout = Layout(top = 3, left = 2)
        )
        delete_world = ButtonView(
            "Delete", callback = None,
            align_vert = "top",
            align_horz = "left",
            layout = Layout(top = 4, left = 2)
        )

        if self.menu_state == MenuStates.NO_WORLD or self.menu_state == MenuStates.READY:
            self.game.screens.push_screen(
                Submenu(
                    name = "WORLD/NO WORLD",
                    game = self.game,
                    views = [new_world, load_world]
                )
            )
        elif self.menu_state == MenuStates.NO_CHARACTER:
            self.game.screens.push_screen(
                Submenu(
                    name = "WORLD/NO CHARACTER",
                    game = self.game,
                    views = [new_world, load_world, delete_world]
                )
            )

    def ui_character_menu(self):
        new_character = ButtonView(
            "New", callback = None,
            align_vert = "top",
            align_horz = "left",
            layout = Layout(top = 2, left = 2)
        )
        delete_character = ButtonView(
            "Delete", callback = None,
            align_vert = "top",
            align_horz = "left",
            layout = Layout(top = 2, left = 2)
        )

        if self.menu_state == MenuStates.NO_CHARACTER:
            self.game.screens.push_screen(
                Submenu(
                    name = "CHARACTER/NO CHARACTER",
                    game = self.game,
                    views = [new_character]
                )
            )
        else:
            Submenu(
                name = "CHARACTER/NO CHARACTER",
                game = self.game,
                views = [delete_character]
            )

    def ui_new_world(self):
        if not self.game.session.game_data:
            self.game.session.new_game_data()
        self.game.screens.push_screen(self.game.screens.screens['WORLD GEN'])

    def ui_load_world(self):
        if not self.game.session.game_data:
            self.game.session.new_game_data()
        self.game.screens.push_screen(SaveFiles(self.game))

    def ui_start(self):
        pass
        # self.game.world.initialize()
        # self.game.player.initialize()
        # self.game.screens.push_screen(self.game.screens.screens['STAGE'])

    def ui_new_character(self):
        pass
        # self.game.screens.push_screen(self.game.screens.screens["NEW CHARACTER"])

    def ui_load_character(self):
        pass
        # self.game.session.data = Storage.load_from_file("test_save")

    def ui_quit(self):
        self.game.screens.quit()

    def cmd_debug_f1(self):
        if not self.game.ui_debug:
            self.logo_box.fg = (255, 0, 0)
            self.menu_box.fg = (255, 0, 0)
            self.character_box.fg = (255, 0, 0)
            self.game.ui_debug = True
        else:
            self.logo_box.fg = (21, 21, 21)
            self.menu_box.fg = (21, 21, 21)
            self.character_box.fg = (21, 21, 21)
            self.game.ui_debug = False


class Submenu(UIScreen):

    def __init__(self, name: str, game: Game, views: List[View]) -> None:
        self.view = RectView(
            subviews = views,
            layout = Layout(top = None, right = None, bottom = 4, left = 14,
                            height = len(views) + 4, width = 14)
        )
        super().__init__(name = name, game = game, views = [self.view])

    def cmd_escape(self):
        self.game.screens.pop_screen()


class SaveFiles(UIScreen):

    def __init__(self, game: Game) -> None:
        self.view = SettingsListView(
            label_control_pairs = [
                (str(index), ButtonView(
                    text = save_id,
                    callback = self.ui_select,
                    align_horz = "left"))
                for index, save_id in SaveFiles.get_save_data()
            ],
            value_column_width = 30,
            layout = Layout(
                top = 10,
                right = None,
                bottom = 12,
                left = 2,
                width = 36,
            )
        )
        super().__init__(name = "SAVE FILES", game = game, views = [self.view])

    @staticmethod
    def get_save_data():
        manifest = get_save_manifest()
        for index, save_id in enumerate(manifest["saves"].keys()):
            yield index, save_id

    def ui_select(self):
        pass

    def cmd_escape(self):
        self.game.screens.replace_screen(self.game.screens.screens["MAIN MENU"])
