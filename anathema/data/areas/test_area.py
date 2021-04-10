from __future__ import annotations
from morphism import Size
from anathema.world.area import Area
from anathema.world.region import Region
from anathema.data.tile_spaces.test_space import TestSpace


class TestArea(Area):

    name: str = "Test Area"

    def __init__(
            self,
            region: Region,
            size: Size
        ) -> None:
        space = TestSpace(size)
        super().__init__(region, size, space)
