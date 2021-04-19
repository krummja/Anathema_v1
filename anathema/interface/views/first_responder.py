from __future__ import annotations
from typing import *
import tcod

from anathema.interface.views import View

if TYPE_CHECKING:
    pass


class FirstResponderView(View):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.responder = None
        self.find_next_responder()

    @property
    def contains_responders(self):
        return True

    def responder_traversal(self):
        for subview in self.subviews:
            yield from self._responder_traversal(subview)

    def _responder_traversal(self, v):
        if v.contains_responders:
            yield v
            return
        for subview in v.subviews:
            yield from self._responder_traversal(subview)
        yield v

    @property
    def _eligible_responders(self):
        return [v for v in self.responder_traversal()
                if v != self and v.can_become_responder]

    def remove_subviews(self, subviews):
        super().remove_subviews(subviews)
        for v in subviews:
            for subview in self._responder_traversal(v):
                if subview == self.responder:
                    self.set_responder(None)
                    self.find_next_responder()
                    return

    def set_responder(self, value):
        if self.responder:
            self.responder.did_resign_responder()
            for ancestor in self.responder.ancestors:
                ancestor.descendant_did_resign_responder(self.responder)

        self.responder = value

        if self.responder:
            self.responder.did_become_responder()
            for ancestor in self.responder.ancestors:
                ancestor.descendant_did_become_responder(self.responder)

    def find_next_responder(self):
        existing_responder = self.responder
        if self.responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_responders

        try:
            i = all_responders.index(existing_responder)
            if i == len(all_responders) - 1:
                self.set_responder(all_responders[0])
            else:
                self.set_responder(all_responders[i + 1])

        except ValueError:
            if all_responders:
                self.set_responder(all_responders[0])
            else:
                self.set_responder(None)

    def find_prev_responder(self):
        existing_responder = self.responder
        if self.responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_responders

        try:
            i = all_responders.index(existing_responder)
            if i == 0:
                self.set_responder(all_responders[-1])
            else:
                self.set_responder(all_responders[i - 1])

        except ValueError:
            if all_responders:
                self.set_responder(all_responders[-1])
            else:
                self.set_responder(None)

    def handle_input(self, val):
        handled = self.responder and self.responder.handle_input(val)
        if self.responder and not handled:
            for v in self.responder.ancestors:
                if v == self:
                    break
                if v.handle_input(val):
                    return True

        can_resign = (not self.responder or self.responder.can_resign_responder)
        return self.handle_input_after_responder(val, can_resign)

    def handle_input_after_responder(self, val, can_resign):
        if can_resign and val == tcod.event.K_TAB:
            if val & tcod.event.KMOD_LSHIFT:
                self.find_prev_responder()
                return True
            else:
                self.find_next_responder()
                return True
        return False
