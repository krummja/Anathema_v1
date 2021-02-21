import random
import numpy as np

from anathema.utils.geometry import Rect, Point, Size
from anathema.world.tiles import Tiles


class TileSpace:

    @staticmethod
    def initialize():
        tile_space = np.zeros((64, 64), dtype=object, order="F")

        #! Point where specific generators may intervene.

        tile_space[:, :] = Tiles.unformed()

        for x in range(64):
            for y in range(64):
                if tile_space[x, y] == Tiles.unformed():
                    roll = random.randrange(0, 100)
                    if roll <= 10:
                        tile_space[x, y] = Tiles.tree_1()
                    if 10 < roll <= 20:
                        tile_space[x, y] = Tiles.grass()
                    if 20 < roll <= 40:
                        tile_space[x, y] = Tiles.tall_grass()

        tile_space[tile_space[:] == Tiles.unformed()] = Tiles.dirt_2()

        # room = Rect(Point(5, 5), Size(10, 10))
        # tile_space[room.outer] = Tiles.flagstone_wall()
        # tile_space[room.inner] = Tiles.flagstone_floor()
        # tile_space[room.top_left.x+3:room.top_left.x+6, room.top] = Tiles.flagstone_floor()

        tile_space[16:25, 16:25] = Tiles.unformed_wet()
        tile_space[18:23, 18:23] = Tiles.solid_wet()

        return tile_space
