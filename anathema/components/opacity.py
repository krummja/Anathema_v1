from ecstremity import Component


class Opacity(Component):
    """Flag component denoting a physics object that may or may not be
    opaque.
    """

    _opaque: bool = True

    @property
    def opaque(self) -> bool:
        return self._opaque

    @opaque.setter
    def opaque(self, value: bool) -> bool:
        self._opaque = value
