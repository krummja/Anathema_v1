from .tilemap import Map_Tilemap
from .terrain import Map_Terrain
from .moniker import Map_Moniker
from .world_location import Map_WorldLocation
from .actors import Map_Actors


def world_components():
    return [
        Map_Actors,
        Map_Tilemap,
        Map_Terrain,
        Map_Moniker,
        Map_WorldLocation,
    ]
