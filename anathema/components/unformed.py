from __future__ import annotations

from ecstremity import Component


class Unformed(Component):
    """Flag component for denoting an unformed tile."""

    def __init__(
            self,
            blocker: bool = False,
            opaque: bool = False,
            wet: bool = False,
            doorway: bool = False,
        ) -> None:
        self.blocker = blocker
        self.opaque = opaque
        self.wet = wet
        self.doorway = doorway
