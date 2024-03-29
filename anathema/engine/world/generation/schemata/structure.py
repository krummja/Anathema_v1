from __future__ import annotations
from typing import *
from random import randint
import numpy as np

from morphism import *

from anathema.engine.world.tile import tile_dt
from anathema.engine.world.generation.tiles import Tiles
from anathema.engine.world.generation.schemata.scheme import Scheme
from anathema.engine.data.directions import *

if TYPE_CHECKING:
    pass


class Mapping:
    UNSET = 0
    OPEN = 1
    SOLID = 2
    PORTAL = 3
    PADDING = 9


class Themes:
    FLAGSTONE = "flagstone"


class Resources:
    GROUND = "ground"
    WALL = "wall"
    FLOOR = "floor"
    PORTAL = "portal"


def theme_select(theme: str, resource: str):
    return {
        "flagstone": {
            "ground": Tiles.dirt_2.make(),
            "wall": Tiles.flagstone_wall.make(),
            "floor": Tiles.flagstone_floor.make(),
            "portal": Tiles.flagstone_floor.make(),
        }
    }[theme][resource]


def edge_selection(rect: Rect, roll: int) -> Tuple[int, int]:
    return {
        0: point_select(rect.points_left),
        1: point_select(rect.points_right),
        2: point_select(rect.points_top),
        3: point_select(rect.points_bottom),
    }[roll]


def point_select(points: Generator[Point, Any, None]) -> Tuple[int, int]:
    points = [_ for _ in points]
    return points[randint(1, len(points)-1)]


class StructureScheme(Scheme):

    @staticmethod
    def generate(settings: Dict[str, Any] = None) -> np.ndarray:
        if not settings:
            settings = {
                "width": randint(5, 10),
                "height": randint(5, 10),
                "padding": randint(1, 3)
            }
        tile_mask = np.zeros((settings["width"], settings["height"]), dtype=int)
        tile_mask[:] = Mapping.UNSET

        room = Rect(Point(), Size(settings["width"], settings["height"]))
        tile_mask[room.outer] = Mapping.SOLID
        tile_mask[room.inner] = Mapping.OPEN

        tile_mask[edge_selection(room, randint(0, 3))] = 3

        tile_mask = np.pad(tile_mask, settings["padding"], constant_values = Mapping.PADDING)
        return tile_mask

    @staticmethod
    def populate(tile_mask: np.ndarray, theme_name: str) -> np.ndarray:
        tiles = np.zeros(tile_mask.shape, dtype=tile_dt)
        tiles[:] = theme_select(theme_name, Resources.GROUND)
        tiles[tile_mask == 1] = theme_select(theme_name, Resources.FLOOR)
        tiles[tile_mask == 2] = theme_select(theme_name, Resources.WALL)
        tiles[tile_mask == 3] = theme_select(theme_name, Resources.PORTAL)
        return tiles

    @staticmethod
    def plop(struct: np.ndarray, at: Tuple[int, int], tile_map: np.ndarray) -> np.ndarray:
        x, y = at
        width, height = struct.shape
        tile_map[x:width+x, y:height+y] = struct
        return tile_map
