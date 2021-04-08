from __future__ import annotations

from anathema.systems.base_system import BaseSystem
from morphism import Rect, Point, Size


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query('tiles', all_of=[ 'Renderable' ], none_of=[ 'Actor' ])
        self.query('actors', all_of=[ 'Actor' ])
        # self.query('items', all_of=[ 'Item' ], none_of=[ 'IsInventoried' ])

    def draw_tiles(self, dt) -> None:
        for tile in self._queries['tiles'].result:
            x, y, z = tile['Position'].xyz

            if not self.game.fov_system.explored[x, y]:
                alpha = 0x00000000
            elif (self.game.fov_system.explored[x, y] and
                not self.game.fov_system.visible[x, y]):
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            if tile['Renderable'].back is not None:
                back = alpha + tile['Renderable'].back
                self.game.context.fill_area(Rect(Point(x, y), Size(1, 1)), color=back)

            self.game.context.color = alpha + tile['Renderable'].fore
            self.game.context.put(Point(x, y), tile['Renderable'].char)

    def draw_items(self, dt) -> None:
        for item in self._queries['items'].result:
            x, y, z = item['Position'].xyz

            if not self.game.fov_system.explored[x, y]:
                alpha = 0x00000000
            elif (self.game.fov_system.explored[x, y] and
                not self.game.fov_system.visible[x, y]):
                alpha = 0x66000000
            else:
                alpha = 0xFF000000

            # if item['Renderable'].back is not None:
            #     back = alpha + item['Renderable'].back
            #     self.game.renderer.fill_area(x, y, 1, 1, color=back)

            self.game.context.color = alpha + item['Renderable'].fore
            self.game.context.put(Point(x, y), item['Renderable'].char)

    def draw_actors(self, dt) -> None:
        for actor in self._queries['actors'].result:
            x, y, z = actor['Position'].xyz

            self.game.context.clear_area(Rect(Point(x, y), Size(1, 1)))
            self.game.context.color = actor['Renderable'].fore
            self.game.context.put(Point(x, y), actor['Renderable'].char)
        print("Actors drawing")

    def update(self, dt) -> None:
        self.game.context.push_to_stack(self.draw_tiles)
        self.game.context.push_to_stack(self.draw_items)
        self.game.context.push_to_stack(self.draw_actors)
