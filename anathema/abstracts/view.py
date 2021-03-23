from __future__ import annotations
from numbers import Real
from collections import namedtuple
import weakref
from morphism import Point, Rect, Size


ZERO_RECT = Rect(Point(0, 0), Size(0, 0))


class LayoutOptions(namedtuple('LayoutOptions', 'width height top right bottom left', defaults=[0])):

    __slots__ = ()
    def __new__(cls, width=None, height=None, top=None, right=None, bottom=None, left=None):
        return super(LayoutOptions, cls).__new__(cls, width, height, top, right, bottom, left)

    # def __new__(cls, width=None, height=None, top=None, right=None, bottom=None, left=None):
    #     return super().__new__(cls, width, height, top, right, bottom, left)

    # Convenience initializers ###

    @classmethod
    def centered(cls, width, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view in the
        center of the superview with a constant width and height.
        """
        return LayoutOptions(
            top=None, bottom=None, left=None, right=None,
            width=width, height=height)

    @classmethod
    def column_left(cls, width):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height left column with a constant width.
        """
        return LayoutOptions(
            top=0, bottom=0, left=0, right=None,
            width=width, height=None)

    @classmethod
    def column_right(cls, width):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height right column with a constant width.
        """
        return LayoutOptions(
            top=0, bottom=0, left=None, right=0,
            width=width, height=None)

    @classmethod
    def row_top(cls, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height top row with a constant height.
        """
        return LayoutOptions(
            top=0, bottom=None, left=0, right=0,
            width=None, height=height)

    @classmethod
    def row_bottom(cls, height):
        """
        Create a :py:class:`LayoutOptions` object that positions the view as a
        full-height bottom row with a constant height.
        """
        return LayoutOptions(
            top=None, bottom=0, left=0, right=0,
            width=None, height=height)

    # Convenience modifiers ###

    def with_updates(self, **kwargs):
        """
        Returns a new :py:class:`LayoutOptions` object with the given changes to
        its attributes. For example, here's a view with a constant width, on the
        right side of its superview, with half the height of its superview::
          # "right column, but only half height"
          LayoutOptions.column_right(10).with_updates(bottom=0.5)
        """
        opts = self._asdict()
        opts.update(kwargs)
        return LayoutOptions(**opts)

    # Semi-internal layout API ###

    def get_type(self, k):
        # Return one of ``{'none', 'frame', 'constant', 'fraction'}``
        val = getattr(self, k)
        if val is None:
            return 'none'
        elif val == 'frame':
            return 'frame'
        elif val == 'intrinsic':
            return 'intrinsic'
        elif isinstance(val, int):
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
                return view.intrinsic_size.width
            elif k == 'height':
                return view.intrinsic_size.height
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


class AbstractView:

    def __init__(
            self,
            frame=None,
            subviews=None,
            screen=None,
            layout_options=None,
            clear=False
        ) -> None:
        self._screen = screen
        self._superview = lambda: None
        self._frame = frame or ZERO_RECT
        self._bounds = self._frame.with_origin(Point(0, 0))

        self.subviews = []
        self.add_subviews(subviews or [])

        self.clear = clear
        self.is_first_responder = False
        self.is_hidden = False
        self.needs_layout = True

        self.layout_spec = frame
        self.layout_options = layout_options or LayoutOptions()

    # core api ###

    @property
    def screen(self):
        """
        The scene this view is being rendered in, or ``None``.
        """
        if self._screen:
            return self._screen
        else:
            return self.superview.screen

    @property
    def superview(self):
        """
        Weak reference to the view this view is a child of, or ``None``.
        """
        try:
            return self._superview()
        except AttributeError:
            return None  # it may be super early in init time

    @superview.setter
    def superview(self, new_value):
        if new_value:
            self._superview = weakref.ref(new_value)
        else:
            self._superview = lambda: None

    def set_needs_layout(self, val=True):
        """
        :param bool val: If ``True``, view needs to be redrawn. (default ``True``)
        Call this if the view's :py:meth:`~clubsandwich.ui.View.frame` or content
        changes. :py:meth:`~View.draw` is only called if this was called first.
        Note that if you're changing either :py:attr:`View.layout_options` or
        changing something that affects the view's springs-and-struts layout
        metrics, you may need to call ``self.superview.set_needs_layout()`` to
        have the layout algorithm re-run on your view.
        """
        self.needs_layout = val

    def add_subviews(self, subviews):
        """
        :param list subviews: List of :py:class:`View` objects
        Append to this view's subviews
        """
        for v in subviews:
            v.superview = self
        self.subviews.extend(subviews)

    def remove_subviews(self, subviews):
        """
        :param list subviews: List of :py:class:`View` objects
        Remove the given subviews from this view
        """
        for v in subviews:
            v.superview = None
        self.subviews = [v for v in self.subviews if v not in subviews]

    def add_subview(self, subview):
        self.add_subviews([subview])

    def remove_subview(self, subview):
        self.remove_subviews([subview])

    def perform_draw(self, ctx):
        """
        Internal. Recursively draw all dirty views. Do not call or subclass this
        unless you are avoiding :py:class:`UIScene` for some reason.
        """
        if self.is_hidden:
            return
        self.draw(ctx)
        for view in self.subviews:
            with ctx.translate(view.frame.origin):
                view.perform_draw(ctx)

    def draw(self, ctx):
        """
        :param BearLibTerminalContext ctx:
        Draw this view. *ctx* is a full copy of the BearLibTerminal API moved into
        this view's frame of reference, so you can use (0, 0) as the upper left
        corner.
        This method will not be called if :py:attr:`View.is_hidden` is ``True``.
        """
        if self.clear:
            ctx.clear_area(self.bounds)

    def perform_layout(self):
        """
        Internal. Recursively layout all dirty views. Do not call or subclass this
        unless you are avoiding :py:class:`UIScene` for some reason.
        """
        if self.needs_layout:
            self.layout_subviews()
            self.needs_layout = False
        for view in self.subviews:
            view.perform_layout()

    def layout_subviews(self):
        """
        Set the frames of all subviews relative to ``self.bounds``. By default,
        applies the springs-and-struts algorithm using each view's
        ``layout_options`` and ``layout_spec`` properties.
        You shouldn't need to override this unless :py:class:`LayoutOptions` isn't
        expressive enough for you.
        """
        for view in self.subviews:
            view.apply_springs_and_struts_layout_in_superview()

    # bounds, frame ###

    @property
    def intrinsic_size(self):
        """
        Optional. Values for ``intrinsic``-valued attributes of
        :py:attr:`LayoutOptions`.
        """
        raise NotImplementedError()

    @property
    def frame(self):
        """
        This view's rect *relative to its superview's bounds*.
        """
        return self._frame

    @frame.setter
    def frame(self, new_value):
        if new_value == self._frame:
            return
        self._frame = new_value
        self._bounds = new_value.with_origin(Point(0, 0))
        self.set_needs_layout(True)

    @property
    def bounds(self):
        """
        This view's rect from its internal frame of reference. That means
        ``self.bounds.origin`` is always ``Point(0, 0)``.
        """
        return self._bounds

    @bounds.setter
    def bounds(self, new_value):
        if new_value.origin != Point(0, 0):
            raise ValueError("Bounds is always anchored at (0, 0)")
        if new_value == self._bounds:
            return
        self._bounds = new_value
        self._frame = self._frame.with_size(new_value.size)
        self.set_needs_layout(True)

    # responder chain, input ###

    @property
    def can_become_first_responder(self):
        """
        View subclasses should return ``True`` iff they want to be selectable and
        handle user input.
        """
        return False

    @property
    def contains_first_responders(self):
        return False

    @property
    def can_resign_first_responder(self):
        """
        View subclass can return ``True`` to prevent the ``tab`` key from taking
        focus away. It should be rare to need this.
        """
        return True

    def did_become_first_responder(self):
        """
        Called immediately after view becomes the first responder.
        """
        self.set_needs_layout(True)
        self.is_first_responder = True

    def did_resign_first_responder(self):
        """
        Called immediately after view resigns first responder status.
        """
        self.set_needs_layout(True)
        self.is_first_responder = False

    def descendant_did_become_first_responder(self, view):
        """
        :param View view:
        Called when any descendant of this view becomes the first responder. This
        is so scrollable view containers can scroll it into view.
        """
        pass

    def descendant_did_resign_first_responder(self, view):
        """
        :param View view:
        Called when any descendant of this view unbecomes the first responder.
        This is so scrollable view containers can release keyboard event handlers.
        """
        pass

    def terminal_read(self, val):
        """
        :param val: Return value of ``terminal_read()``
        :return: bool (``True`` if you handled the event)
        Fires when an input event occurs, and either:
        * This view is the first responder
        * The first responder is a descendant, and no other descendants have
          already handled this event
        You **must** return a truthy value if you handled the event so it doesn't get
        handled twice.
        """
        return False

    @property
    def first_responder_container_view(self):
        """
        The ancestor (including ``self``) that is a
        :py:class:`FirstResponderContainerView`.
        The most common use for this will probably be to manually change the
        first responder::
          def a_method_on_your_view(self):
            # forceably become first responder, muahaha!
            self.first_responder_container_view.set_first_responder(self)
        """
        # pretty hacky way to check for this but whatever
        if hasattr(self, 'first_responder'):
            return self
        for v in self.ancestors:
            if hasattr(v, 'first_responder'):
                return v
        return None

    # tree traversal ###

    @property
    def leftmost_leaf(self):
        """
        Leftmost leaf of the tree.
        """
        if self.subviews:
            return self.subviews[0].leftmost_leaf
        else:
            return self

    @property
    def postorder_traversal(self):
        """
        Generator of all nodes in this subtree, including ``self``, such that a
        view is visited after all its subviews.
        """
        for v in self.subviews:
            yield from v.postorder_traversal
        yield self

    @property
    def ancestors(self):
        """
        Generator of all ancestors of this view, not including ``self``.
        """
        v = self.superview
        while v:
            yield v
            v = v.superview

    def get_ancestor_matching(self, predicate):
        """
        :param func predicate: ``predicate(View) -> bool``
        Returns the ancestor matching the given predicate, or ``None``.
        """
        v = self.superview
        for _ in self.ancestors:
            if predicate(v):
                return v
        return None

    @property
    def debug_string(self):
        """A string containing helpful debugging info for this view"""
        return '{} {!r}'.format(type(self).__name__, self.frame)

    def debug_print(self, indent=0):
        """Print hierarchical representation of this view and its subviews to
        stdout"""
        print(' ' * indent + self.debug_string)
        for sv in self.subviews:
            sv.debug_print(indent + 2)

    def __str__(self):
        return self.debug_string

    def __repr__(self):
        return self.debug_string

    def apply_springs_and_struts_layout_in_superview(self):
        options = self.layout_options
        spec = self.layout_spec
        superview_bounds = self.superview.bounds

        fields = [
            ('left', 'right', 'x', 'width'),
            ('top', 'bottom', 'y', 'height'),
            ]

        final_frame = Rect(Point(-1000, -1000), Size(-1000, -1000))

        for field_start, field_end, field_coord, field_size in fields:

            debug_string = options.get_debug_string_for_keys(
                [field_start, field_size, field_end])

            matches = (
                options.get_is_defined(field_start),
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

        assert(final_frame.left != -1000)
        assert(final_frame.top != -1000)
        assert(final_frame.width != -1000)
        assert(final_frame.height != -1000)
        self.frame = final_frame.floored
