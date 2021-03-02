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
        return self.game.ecs.engine.get_entity(self._player_uid)

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
        player = self.game.ecs.engine.create_entity()
        self.game.ecs.engine.prefabs.apply_to_entity(
            player, 'Player', {'Position': {'x': 10, 'y': 10, 'z': Depth.ABOVE_1.value}})
        player['Noun'].noun_text = "Aulia Inuicta"
        self._player_uid = player.uid

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]

        def block_check() -> EventData:
            """Blocker check callback"""

            if self.game.world.current_area.is_blocked(target_x, target_y):

                return EventData(success = False,
                                 result  = Message("The way is blocked!"))

            return EventData(success = True,
                             require = {'to': direction})

        def interact_check() -> EventData:
            """Interactable check callback."""

            if self.game.world.current_area.is_interactable(target_x, target_y):
                interactable = self.game.interaction_system \
                    .get_interactables_at_pos(target_x, target_y)

                return EventData(success = True,
                                 require = {'target': interactable},
                                 expect  = {'interactions': []})

            return EventData(success = False,
                             result  = Message("The way is blocked!"))

        # Check if the target position is blocked.
        action = Action(
            entity = self.entity,
            event  = 'try_move',
            check  = block_check
            ).plan()

        # If so...
        if not action.data.success:
            # Try to see if we can interact with it.
            action = Action(
                entity = self.entity,
                event  = 'try_get_interactions',
                check  = interact_check
                ).plan()

        self.action_queue.append(action)

    def close(self, closable) -> None:

        def open_check() -> EventData:
            """Open check callback."""

            if closable.has('Door') and closable['Door'].is_open:

                return EventData(success = True,
                                 require = {'target': closable},
                                 expect  = {'interactions': []})

            if closable.has('Container') and closable['Container'].is_open:

                return EventData(success = True,
                                 require = {'target': closable},
                                 expect  = {'interactions': []})

            return EventData(success = False,
                             result  = {'message': "Close what?"})

        # Check if the target interactable is open, so that we can close it.
        action = Action(
            entity = self.entity,
            event  = 'try_get_interactions',
            check  = open_check
            ).plan()

        self.action_queue.append(action)

    def pickup(self) -> None:

        target = self.game.interaction_system.get_interactables_at_pos(*self.position)

        def lift_check() -> EventData:
            """Lift check callback."""

            if target and target.has('Item') and target.has('IsInteractable'):

                return EventData(success = True,
                                 require  = {'target': target,
                                             'instigator': self.entity},
                                 expect   = {'interactions': []},
                                #  result   = {'message': 'You take the %s', 'a': target})
                                 result   = Message(
                                     f"{0} pick[s] up the {1} and stow[s] {1, THEM}.",
                                     noun1=self.entity['Noun'],
                                     noun2=target['Noun']))

            return EventData(success = False,
                             result  = Message(
                                 f"{0} cannot lift that!",
                                 noun1=self.entity['Noun']))

        action = Action(
            entity = self.entity,
            event  = 'try_pickup',
            check  = lift_check
            ).plan()

        self.action_queue.append(action)
