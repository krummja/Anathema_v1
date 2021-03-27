from __future__ import annotations
from typing import Optional, Union


class LayoutOptions:

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
