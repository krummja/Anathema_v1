from __future__ import annotations

from ecstremity import Component


class Health(Component):

    def __init__(self, base: int) -> None:
        self._BASE_HEALTH = base
        self._DAMAGE: int = 0
        self._ALIVE: bool = True

    @property
    def current(self) -> int:
        return self._BASE_HEALTH - self._DAMAGE

    def apply_damage(self, value: int) -> None:
        if self._ALIVE:
            self._DAMAGE += value
        if self._DAMAGE == self._BASE_HEALTH:
            self._ALIVE = False

    def apply_healing(self, value: int) -> None:
        self.apply_damage(value * -1)

    def __str__(self) -> str:
        return f"{self.current} / {self._BASE_HEALTH}"
