from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component, EventData

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Legs(Component):

    def __init__(self, leg_count: int = 2) -> None:
        super().__init__()
        self._leg_count = leg_count
        self.area = self.client.world.current_area

    def on_try_move(self, evt: EntityEvent) -> None:
        # TODO There has to be a better way to do this lol
        # Ideally return SUCCESS or FAILURE and then resolve from there?
        if self.area.is_blocked(*evt.data.target):

            if self.area.is_interactable(*evt.data.target):
                interactable = self.client.interaction_system.get(*evt.data.target)
                evt.data.instigator = self.entity
                evt.data.interactions = []

                returned = evt.route(new_event='get_interactions', target=interactable)
                if returned.data.instigator == self.client.player.entity:
                    if len(returned.data.interactions) == 1:
                        interaction = returned.data.interactions.pop()
                        interactable.fire_event(interaction['event'], EventData(
                            callback=(lambda f: self.client.to_ui_hook(f))
                            ))
                    else:
                        # Route to the UI
                        pass
                else:
                    # Route to GoalSystem
                    pass
                returned.handle()
            else:
                # Route to LogManager
                pass
        else:
            self.update_position(*evt.data.target)
        evt.handle()

    def update_position(self, x: int, y: int) -> None:
        self.entity['Position'].x = x
        self.entity['Position'].y = y
