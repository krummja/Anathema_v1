from __future__ import annotations

from bearlibterminal import terminal
from morphism import Point, Rect


class _TerminalState:
    pass


for constant_key in (c for c in dir(terminal) if c.startswith('TK_')):
    def getter(k):
        constant_value = getattr(terminal, k)

        def get(self):
            return terminal.state(constant_value)
        return get
    constant_name = constant_key[3:].lower()
    attr_name = 'num_{}'.format(
        constant_name) if constant_name[0].isdigit() else constant_name
    setattr(
        _TerminalState,
        attr_name,
        property(getter(constant_key)))


class BaseTerminal:

    def __getattr__(self, k):
        return getattr(terminal, k)

    def clear_area(self, *args):
        if args and isinstance(args[0], Rect):
            return terminal.clear_area(
                args[0].origin.x, args[0].origin.y,
                args[0].size.width, args[0].size.height)
        return terminal.clear_area(*args)

    def crop(self, *args):
        if args and isinstance(args[0], Rect):
            return terminal.crop(
                args[0].origin.x, args[0].origin.y,
                args[0].size.width, args[0].size.height)
        else:
            return terminal.crop(*args)

    def puts(self, *args):
        if isinstance(args[0], Point):
            return terminal.puts(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.puts(*args)

    def printf(self, *args):
        if isinstance(args[0], Point):
            return terminal.printf(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.printf(*args)

    def put(self, *args):
        if isinstance(args[0], Point):
            return terminal.put(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.put(*args)

    def pick(self, *args):
        if isinstance(args[0], Point):
            return terminal.pick(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick(*args)

    def pick_color(self, *args):
        if isinstance(args[0], Point):
            return terminal.pick_color(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick_color(*args)

    def pick_bkcolor(self, *args):
        if isinstance(args[0], Point):
            return terminal.pick_bkcolor(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick_bkcolor(*args)

    def put_ext(self, *args):
        if isinstance(args[0], Point):
            return terminal.put_ext(args[0].x, args[0].y, args[1].x, args[1].y, *args[2:])
        else:
            return terminal.put_ext(*args)

    def read_str(self, *args):
        if isinstance(args[0], Point):
            return terminal.read_str(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.read_str(*args)

blt_state = _TerminalState()
