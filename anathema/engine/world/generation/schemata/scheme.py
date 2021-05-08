from __future__ import annotations
from typing import *
import numpy as np

if TYPE_CHECKING:
    pass


class Scheme:

    @staticmethod
    def generate(settings: Dict[str, Any]) -> np.ndarray:
        pass

    @staticmethod
    def populate(tiles: np.ndarray, theme: str) -> np.ndarray:
        pass
