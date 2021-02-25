from __future__ import annotations
from contextlib import suppress
from typing import Any, List, Optional, Protocol, Union


class Observer(Protocol):
    def _update(self, subject: Subject) -> None:
        pass


class Subject:

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        with suppress(ValueError):
            self._observers.remove(observer)

    def notify(self, modifier: Optional[Observer] = None) -> None:
        for observer in self._observers:
            if modifier != observer:
                observer._update(self)


class Data(Subject):

    def __init__(self) -> None:
        super().__init__()
        self._data = []

    @property
    def data(self) -> List[Any]:
        return self._data

    @data.setter
    def data(self, value: Union[List[Any], Any]) -> None:
        if isinstance(value, list):
            self._data = value
        else:
            self._data.append(value)
        self.notify()
