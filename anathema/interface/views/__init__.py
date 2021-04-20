from __future__ import annotations
from typing import *
from morphism import *

if TYPE_CHECKING:
    from anathema.interface.screens import Screen


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class Layout:

    def __init__(
            self,
            width: Optional[Union[int, float]] = None,
            height: Optional[Union[int, float]] = None,
            left: Optional[Union[int, float]] = 0,
            top: Optional[Union[int, float]] = 0,
            right: Optional[Union[int, float]] = 0,
            bottom: Optional[Union[int, float]] = 0
        ) -> None:
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.opts = {
            'width': width,
            'height': height,
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom
            }

    @classmethod
    def centered(cls, width, height):
        return LayoutOptions(
            top=None, bottom=None, left=None, right=None,
            width=width, height=height)

    @classmethod
    def column_left(cls, width):
        return LayoutOptions(
            top=0, bottom=0, left=0, right=None,
            width=width, height=None)

    @classmethod
    def column_right(cls, width):
        return LayoutOptions(
            top=0, bottom=0, left=None, right=0,
            width=width, height=None)

    @classmethod
    def row_top(cls, height):
        return LayoutOptions(
            top=0, bottom=None, left=0, right=0,
            width=None, height=height)

    @classmethod
    def row_bottom(cls, height):
        return LayoutOptions(
            top=None, bottom=0, left=0, right=0,
            width=None, height=height)

    # Convenience modifiers ###

    def with_updates(self, **kwargs):
        opts = self.opts
        opts.update(kwargs)
        return LayoutOptions(**opts)

    # Semi-internal layout API ###

    def get_type(self, k):
        val = getattr(self, k)
        if val is None:
            return 'none'
        elif val == 'frame':
            return 'frame'
        elif val == 'intrinsic':
            return 'intrinsic'
        elif isinstance(val, int) or isinstance(val, float):
            if val >= 1:
                return 'constant'
            else:
                return 'fraction'
        else:
            raise ValueError(
                "Unknown type for option {}: {}".format(k, type(k)))

    def get_is_defined(self, k):
        return getattr(self, k) is not None

    def get_debug_string_for_keys(self, keys):
        return ','.join(["{}={}".format(k, self.get_type(k)) for k in keys])

    def get_value(self, k, view):
        if getattr(self, k) is None:
            raise ValueError("Superview isn't relevant to this value")

        elif self.get_type(k) == 'constant':
            return getattr(self, k)

        elif self.get_type(k) == 'intrinsic':
            if k == 'width':
                return view.intrinsic_size[0]
            elif k == 'height':
                return view.intrinsic_size[1]
            else:
                raise KeyError(
                    "'intrinsic' can only be used with width or height.")

        elif self.get_type(k) == 'frame':
            if k == 'left':
                return view.layout_spec.x
            elif k == 'top':
                return view.layout_spec.y
            elif k == 'right':
                return view.superview.bounds.width - view.layout_spec.right
            elif k == 'bottom':
                return view.superview.bounds.height - view.layout_spec.bottom
            elif k == 'width':
                return view.layout_spec.width
            elif k == 'height':
                return view.layout_spec.height
            else:
                raise KeyError("Unknown key:", k)

        elif self.get_type(k) == 'fraction':
            val = getattr(self, k)
            if k in ('left', 'width', 'right'):
                return view.superview.bounds.width * val
            elif k in ('top', 'height', 'bottom'):
                return view.superview.bounds.height * val
            else:
                raise KeyError("Unknown key:", k)


class View:

    def __init__(
            self,
            screen: Optional[Screen] = None,
            layout: Optional[Layout] = None,
            subviews: List[View] = None,
            frame: Optional[Rect] = None,
            clear: bool = False,
        ) -> None:
        if not frame:
            self._frame = ZERO_RECT
        else:
            self._frame = frame

        self._screen = screen
        self._superview = None
        self._bounds = self._frame.with_origin(Point(0, 0))
        self.needs_layout: bool = True

        self.clear: bool = clear
        self.responder = None
        self.is_responder: bool = False
        self.is_hidden: bool = False

        self.subviews: List[View] = []
        self.add_subviews(subviews if subviews else [])
        self.layout_spec = frame

        if not layout:
            self.layout_options = Layout()
        else:
            self.layout_options = layout

    @property
    def console(self):
        return self.screen.game.console.root

    @property
    def context(self):
        return self.screen.game.console.context

    @property
    def screen(self):
        if self._screen:
            return self._screen
        return self._superview.screen

    @property
    def superview(self) -> Optional[View]:
        try:
            return self._superview
        except AttributeError:
            return None

    @superview.setter
    def superview(self, value: View):
        self._superview = value

    def set_needs_layout(self, value: bool = True) -> None:
        self.needs_layout = value

    def add_subviews(self, subviews: List[View]) -> None:
        for v in subviews:
            v.superview = self
        self.subviews.extend(subviews)

    def remove_subviews(self, subviews: List[View]) -> None:
        for v in subviews:
            v.superview = None
        self.subviews = [v for v in self.subviews if v not in subviews]

    def add_subview(self, subview: View) -> None:
        self.add_subviews([subview])

    def remove_subview(self, subview: View) -> None:
        self.remove_subviews([subview])

    def perform_draw(self) -> None:
        if self.is_hidden:
            return
        self.draw()
        for view in self.subviews:
            with self.context.translate(view.frame.origin):
                view.perform_draw()

    def draw(self):
        if self.clear:
            self.console.clear()

    def perform_layout(self) -> None:
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self) -> None:
        for view in self.subviews:
            view.apply_springs_and_struts_layout_in_superview()

    @property
    def intrinsic_size(self) -> Optional[Size]:
        return None

    @property
    def frame(self) -> Rect:
        return self._frame

    @frame.setter
    def frame(self, value: Rect) -> None:
        if value == self._frame:
            return
        self._frame = value
        self._bounds = value.with_origin(Point(0, 0))
        self.set_needs_layout(True)

    @property
    def bounds(self) -> Rect:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Rect) -> None:
        if value.origin != Point(0, 0):
            raise ValueError("Bounds is always anchored at (0, 0)")
        if value == self._bounds:
            return
        self._bounds = value
        self._frame = self._frame.with_size(value.size)
        self.set_needs_layout(True)

    @property
    def can_become_responder(self) -> bool:
        return False

    @property
    def contains_responders(self) -> bool:
        return False

    @property
    def can_resign_responder(self) -> bool:
        return True

    @property
    def responder_container_view(self) -> Optional[View]:
        if self.responder:
            return self
        for v in self.ancestors:
            if v.responder:
                return v
        return None

    def did_become_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_responder = True

    def did_resign_first_responder(self) -> None:
        self.set_needs_layout(True)
        self.is_responder = False

    def descendant_did_become_responder(self, view: View) -> bool:
        pass

    def descendant_did_resign_responder(self, view: View) -> bool:
        pass

    def handle_input(self, char):
        return False

    @property
    def leftmost_leaf(self):
        if self.subviews:
            return self.subviews[0].leftmost_leaf
        else:
            return self

    @property
    def postorder_traversal(self):
        for v in self.subviews:
            yield from v.postorder_traversal
        yield self

    @property
    def ancestors(self):
        v = self.superview
        while v:
            yield v
            v = v.superview

    def get_ancestor_matching(self, predicate):
        v = self.superview
        for _ in self.ancestors:
            if predicate(v):
                return v
        return None

    def apply_springs_and_struts_layout_in_superview(self):
        options = self.layout_options
        spec = self.layout_spec
        superview_bounds = self.superview.bounds

        fields = [('left', 'right', 'x', 'width'),
                  ('top', 'bottom', 'y', 'height')]

        final_frame = Rect(Point(-1000, -1000), Size(-1000, -1000))

        for field_start, field_end, field_coord, field_size in fields:

            debug_string = options.get_debug_string_for_keys(
                [field_start, field_size, field_end])

            matches = (options.get_is_defined(field_start),
                       options.get_is_defined(field_size),
                       options.get_is_defined(field_end))

            if matches == (True, True, True):
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            if matches == (False, False, False):
                raise ValueError(
                    "Invalid spring/strut definition: {}".format(debug_string))

            elif matches == (True, False, False):
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                # pretend that size is constant from frame
                setattr(
                    final_frame, field_size,
                    getattr(spec, field_size))

            elif matches == (True, True, False):
                setattr(
                    final_frame, field_coord,
                    options.get_value(field_start, self))
                setattr(
                    final_frame, field_size,
                    options.get_value(field_size, self))

            elif matches == (False, True, False):  # magical centering!
                size_val = options.get_value(field_size, self)
                setattr(final_frame, field_size, size_val)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) / 2 - size_val / 2)

            elif matches == (False, True, True):
                size_val = options.get_value(field_size, self)
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self) - size_val)
                setattr(final_frame, field_size, size_val)

            elif matches == (False, False, True):
                setattr(
                    final_frame, field_coord,
                    getattr(superview_bounds, field_size) - options.get_value(field_end, self))
                # pretend that size is constant from frame
                setattr(final_frame, field_size, getattr(spec, field_size))

            elif matches == (True, False, True):
                start_val = options.get_value(field_start, self)
                end_val = options.get_value(field_end, self)
                setattr(final_frame, field_coord, start_val)
                setattr(final_frame, field_size,
                        getattr(superview_bounds, field_size) - start_val - end_val)

            else:
                raise ValueError("Unhandled case: {}".format(debug_string))

        assert(final_frame.x != -1000)
        assert(final_frame.y != -1000)
        assert(final_frame.width != -1000)
        assert(final_frame.height != -1000)
        self.frame = final_frame.floored
