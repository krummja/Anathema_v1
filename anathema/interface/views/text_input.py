from __future__ import annotations
from typing import *
from dataclasses import dataclass

from time import time
import datetime

import tcod.event
from morphism import *
from anathema.interface.views import View

if TYPE_CHECKING:
    pass


@dataclass
class TextInputConfig:
    initial_value: str = str(datetime.date.today())
    color_unselected_fg = (255, 255, 255)
    color_unselected_bg = (21, 21, 21)
    color_selected_fg = (255, 255, 0)
    color_selected_bg = (21, 21, 21)


class TextInputView(View):

    def __init__(
            self,
            config: TextInputConfig,
            callback,
            *args, **kwargs
        ) -> None:
        self.config = config
        self.text = config.initial_value
        self.callback = callback
        super().__init__(*args, **kwargs)

    def intrinsic_size(self) -> Optional[Size]:
        return Size(len(self.text) + 1, 1)

    def draw(self):
        color_fg = self.config.color_selected_fg if self.is_first_responder else self.config.color_unselected_fg
        color_bg = self.config.color_selected_bg if self.is_first_responder else self.config.color_unselected_bg
        self.context.print(Point(0, 0), self.text, fg = color_fg, bg = color_bg)

        text_len = len(self.text)
        if int(self.bounds.width) > text_len:
            self.context.print(Point(text_len, 0), "." * (self.bounds.width - text_len - 1))
        if self.is_first_responder and int(time() * 1.2) % 2 == 0:
            self.context.put_char(Point(text_len, 0), ord("█"))

    def did_resign_first_responder(self) -> None:
        super().did_resign_first_responder()
        self.set_needs_layout()

    def can_become_first_responder(self) -> bool:
        return True

    def _update_text(self, value: str):
        self.text = value
        self.superview.set_needs_layout()

    def handle_input(self, event):
        if event.sym == tcod.event.K_RETURN:
            self.callback(self.text)
            self.first_responder_container_view.find_next_responder()
            return True
        if event.sym == tcod.event.K_TAB:
            self.callback(self.text)
            return False
        elif event.sym == tcod.event.K_BACKSPACE:
            if self.text:
                self._update_text(self.text[:-1])
                return True

    def handle_textinput(self, event):
        self._update_text(self.text + event.text)
