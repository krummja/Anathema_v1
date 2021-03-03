from __future__ import annotations

from ecstremity import Component


class IsDestroying(Component):
    """Flag component to mark entities as undergoing destruction. Prevents systems
    from exploding mid-cycle..."""

    cycle: int = 0

