from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from abc import ABC, abstractmethod


class Effect(ABC):

    def __init__(
            self,
            start_frame: int = 0,
            stop_frame: int = 0,
            delete_count = None
        ) -> None:
        self._manager = None
        self._start_frame = start_frame
        self._stop_frame = stop_frame
        self._delete_count = delete_count

    def update(self, frame_no: int):
        if (frame_no >= self._start_frame and
            (self._stop_frame == 0 or frame_no < self._stop_frame)):
            self._update(frame_no)

    def register_manager(self, manager) -> None:
        self._manager = manager

    @abstractmethod
    def _update(self, frame_no: int) -> None:
        pass
