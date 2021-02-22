from ecstremity import Component


class Blocker(Component):
    """Flag component denoting a non-passable physics object."""

    _impassable: bool = True

    @property
    def impassable(self) -> bool:
        return self._impassable

    @impassable.setter
    def impassable(self, value: bool) -> None:
        self._impassable = value
