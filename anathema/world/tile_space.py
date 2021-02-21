
import numpy as np

from anathema.utils.geometry import Rect, Point, Size
from anathema.world.tiles import Tiles


class TileSpace:

    @staticmethod
    def initialize():
        tile_space = np.zeros((64, 64), dtype=object, order="F")

        #! Point where specific generators may intervene.

        tile_space[:, :] = Tiles.flagstone_floor()

        room = Rect(Point(5, 5), Size(10, 10))
        tile_space[room.outer] = Tiles.flagstone_wall()
        tile_space[room.inner] = Tiles.flagstone_floor()
        tile_space[room.top_left.x+3:room.top_left.x+6, room.top] = Tiles.flagstone_floor()

        return tile_space
