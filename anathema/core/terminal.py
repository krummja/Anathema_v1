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

    @staticmethod
    def layer(value):
        return terminal.layer(value)

    @staticmethod
    def clear_area(*args):
        if args and isinstance(args[0], Rect):
            return terminal.clear_area(
                args[0].origin.x, args[0].origin.y,
                args[0].size.width, args[0].size.height)
        return terminal.clear_area(*args)

    @staticmethod
    def crop(*args):
        if args and isinstance(args[0], Rect):
            return terminal.crop(
                args[0].origin.x, args[0].origin.y,
                args[0].size.width, args[0].size.height)
        else:
            return terminal.crop(*args)

    @staticmethod
    def puts(*args):
        if isinstance(args[0], Point):
            return terminal.puts(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.puts(*args)

    @staticmethod
    def printf(*args):
        if isinstance(args[0], Point):
            return terminal.printf(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.printf(*args)

    @staticmethod
    def put(*args):
        if isinstance(args[0], Point):
            return terminal.put(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.put(*args)

    @staticmethod
    def pick(*args):
        if isinstance(args[0], Point):
            return terminal.pick(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick(*args)

    @staticmethod
    def pick_color(*args):
        if isinstance(args[0], Point):
            return terminal.pick_color(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick_color(*args)

    @staticmethod
    def pick_bkcolor(*args):
        if isinstance(args[0], Point):
            return terminal.pick_bkcolor(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.pick_bkcolor(*args)

    @staticmethod
    def put_ext(*args):
        if isinstance(args[0], Point):
            return terminal.put_ext(args[0].x, args[0].y, args[1].x, args[1].y, *args[2:])
        else:
            return terminal.put_ext(*args)

    @staticmethod
    def read_str(*args):
        if isinstance(args[0], Point):
            return terminal.read_str(args[0].x, args[0].y, *args[1:])
        else:
            return terminal.read_str(*args)


blt_state = _TerminalState()
