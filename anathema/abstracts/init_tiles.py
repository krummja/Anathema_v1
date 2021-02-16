from abc import ABC, abstractmethod


class AbstractInitTiles(ABC):
    """Abstract for creating an array of Tile objects."""

    def __init__(self) -> None:
        self.tiles = self.initialize_tiles()

    @abstractmethod
    def initialize_tiles(self):
        pass
