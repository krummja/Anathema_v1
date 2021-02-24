from ecstremity import Component


class Blocker(Component):
    """State component denoting a non-passable physics object."""

    _impassable: bool = True

    @property
    def impassable(self) -> bool:
        return self._impassable

    @impassable.setter
    def impassable(self, value: bool) -> None:
        self._impassable = value
