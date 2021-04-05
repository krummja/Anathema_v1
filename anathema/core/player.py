from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from collections import deque

from anathema.data.actions.event_data import EventData
from anathema.data.actions.action import Action
from anathema.data.message import Message, THEM
from anathema.abstracts import AbstractManager
from anathema.world.tile_factory import Depth

if TYPE_CHECKING:
    from anathema.core import Game


class PlayerManager(AbstractManager):

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.action_queue = deque([])
        self._player_uid = None
        self.initialize_player()

    @property
    def entity(self):
        return self.game.ecs.get_entity(self._player_uid)

    @property
    def uid(self):
        return self._player_uid

    @property
    def is_turn(self) -> bool:
        return self.entity['Actor'].has_energy

    @property
    def position(self) -> Tuple[int, int]:
        return self.entity['Position'].xy

    def initialize_player(self):
        player = self.game.ecs.create_entity()
        self.game.ecs.prefabs.apply_to_entity(
            player, 'Player', {'Position': {'x': 10, 'y': 10, 'z': Depth.ABOVE_2.value}})
        player['Noun'].noun_text = "Aulia Inuicta"
        self._player_uid = player.uid

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]

        # Check if there is an obstacle in the way
        if self.game.world.current_area.is_blocked(target_x, target_y):

            # Hmm, it's blocked - see if we can interact with it...
            if self.game.world.current_area.is_interactable(target_x, target_y):
                interactable = self.game.interaction_system.get(target_x, target_y)

                # We can! Let's do some work.
                self.action_queue.append(
                    Action(entity = self.entity, event = 'try_get_interactions',
                           data = {
                               'target': interactable,
                               'expect': []
                               }
                           ))

            # Nope! Can't move that way :(
            self.game.log.report(Message("The way is blocked!"))

        # If no obstacle, we're good to go!
        else:
            self.action_queue.append(
                Action(entity = self.entity, event = 'try_move',
                       data = {
                           'target': direction
                           }
                       ))

    def close(self, closable) -> None:
        if ((closable.has('Door') and closable['Door'].is_open) or
            (closable.has('Container') and closable['Container'].is_open)):

            self.action_queue.append(
                Action(entity = self.entity, event = 'try_get_interactions',
                       data = {
                           'target': closable,
                           'expect': []
                           }
                       ))

    def pickup(self) -> None:
        target = self.game.interaction_system.get(*self.position)
        self.action_queue.append(
            Action(entity = self.entity, event = 'try_pickup',
                   data = {
                       'target': target,
                       'instigator': self.entity
                       }
                   ))

        # self.game.log.report(Message(f"{0} pick[s] up the {1} and stow[s] {1, THEM}.",
        #                              noun1=self.entity['Noun'],
        #                              noun2=target['Noun']))
