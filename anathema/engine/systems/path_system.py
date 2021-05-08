from __future__ import annotations
from typing import *
from collections import deque

import tcod
import numpy as np

from anathema.engine.systems import BaseSystem

if TYPE_CHECKING:
    from ecstremity import Entity
    from anathema.engine.world.tilemap import TileMap


class PathSystem(BaseSystem):

    def initialize(self):
        self.query('pathing', all_of=[ 'Actor' ])
        self.query('blockers', all_of=[ 'Blocker' ])

    def compute_path(self, pathing_entity: Entity):
        _area: TileMap = self.game.world.current_area
        walkable = np.copy(_area.tiles["move_cost"])

        dest_xy = pathing_entity['Actor'].dest_xy
        blocker_pos = [e["Position"].ij for e in self._queries['blockers'].result]
        blocker_index = tuple(np.transpose(blocker_pos))

        walkable[blocker_index] = 50
        walkable.T[dest_xy] = 1

        graph = tcod.path.SimpleGraph(cost=walkable, cardinal=2, diagonal=2)
        pf = tcod.path.Pathfinder(graph)
        pf.add_root(pathing_entity['Position'].ij)
        return [(ij[1], ij[0]) for ij in pf.path_to(dest_xy[::-1])[1:].tolist()]

    def update(self):
        pathing_entities = filter((lambda e: e['Actor'].is_pathing), self._queries['pathing'].result)

        for entity in pathing_entities:
            entity['Actor'].path = self.compute_path(entity)
