from __future__ import annotations

from bearlibterminal import terminal

from screens.views.view import View
from anathema.core.terminal import blt_state


class FirstResponderContainerView(View):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.first_responder = None
        self.find_next_responder()

    @property
    def contains_first_responders(self):
        return True

    def first_responder_traversal(self):
        for subview in self.subviews:
            yield from self._first_responder_traversal(subview)

    def _first_responder_traversal(self, v):
        if v.contains_first_responders:
            yield v
            return
        for subview in v.subviews:
            yield from self._first_responder_traversal(subview)
        yield v

    @property
    def _eligible_first_responders(self):
        return [v for v in self.first_responder_traversal()
                if v != self and v.can_become_first_responder]

    def remove_subviews(self, subviews):
        super().remove_subviews(subviews)
        for v in subviews:
            for subview in self._first_responder_traversal(v):
                if subview == self.first_responder:
                    self.set_first_responder(None)
                    self.find_next_responder()
                    return

    def set_first_responder(self, value):
        if self.first_responder:
            self.first_responder.did_resign_first_responder()
            for ancestor in self.first_responder.ancestors:
                ancestor.descendant_did_resign_first_responder(self.first_responder)

        self.first_responder = value

        if self.first_responder:
            self.first_responder.did_become_first_responder()
            for ancestor in self.first_responder.ancestors:
                ancestor.descendant_did_become_first_responder(self.first_responder)

    def find_next_responder(self):
        existing_responder = self.first_responder
        if self.first_responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_first_responders

        try:
            i = all_responders.index(existing_responder)
            if i == len(all_responders) - 1:
                self.set_first_responder(all_responders[0])
            else:
                self.set_first_responder(all_responders[i + 1])

        except ValueError:
            if all_responders:
                self.set_first_responder(all_responders[0])
            else:
                self.set_first_responder(None)

    def find_prev_responder(self):
        existing_responder = self.first_responder
        if self.first_responder is None:
            existing_responder = self.leftmost_leaf
        all_responders = self._eligible_first_responders

        try:
            i = all_responders.index(existing_responder)
            if i == 0:
                self.set_first_responder(all_responders[-1])
            else:
                self.set_first_responder(all_responders[i - 1])

        except ValueError:
            if all_responders:
                self.set_first_responder(all_responders[-1])
            else:
                self.set_first_responder(None)

    def terminal_read(self, val):
        handled = self.first_responder and self.first_responder.terminal_read(val)
        if self.first_responder and not handled:
            for v in self.first_responder.ancestors:
                if v == self:
                    break
                if v.terminal_read(val):
                    return True

        can_resign = (not self.first_responder or
                      self.first_responder.can_resign_first_responder)
        return self.terminal_read_after_first_responder(val, can_resign)

    def terminal_read_after_first_responder(self, val, can_resign):
        if can_resign and val == terminal.TK_TAB:
            if blt_state.shift:
                self.find_prev_responder()
                return True
            else:
                self.find_next_responder()
                return True
        return False
