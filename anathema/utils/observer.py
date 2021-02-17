from __future__ import annotations
from contextlib import suppress
from typing import List, Optional, Protocol


class Observer(Protocol):
    def update(self, subject: Subject) -> None:
        pass


class Subject:

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        pass
