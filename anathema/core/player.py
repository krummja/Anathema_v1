from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Union, Tuple, Optional, TYPE_CHECKING
from collections import deque

from anathema.data.actions.action import Action
from anathema.abstracts import AbstractManager
from anathema.world.tile_factory import Depth

if TYPE_CHECKING:
    from anathema.core import Game

@dataclass
class EventData:
    # Did the Action succeed?
    success: bool = False
    done: bool = False
    # What does the Action require?
    require: Dict[str, Any] = None
    # What can I expect back from its completion?
    expect: Dict[str, Any] = None
    # Additional useful data to do something with
    result: Dict[str, Any] = None


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
        player['Name'].noun_text = "Aulia Inuicta"
        self._player_uid = player.uid

    def get_next_action(self):
        return self.action_queue.popleft()

    def move(self, direction: Tuple[int, int]) -> None:
        target_x = self.position[0] + direction[0]
        target_y = self.position[1] + direction[1]

        def block_check() -> bool:
            """Blocker check callback"""

            if self.game.world.current_area.is_blocked(target_x, target_y):

                return EventData(success = False)

            return EventData(success = True,
                             require = {'to': direction})

        def interact_check() -> Union[bool, Tuple[bool, str]]:
            """Interactable check callback."""

            if self.game.world.current_area.is_interactable(target_x, target_y):
                interactable = self.game.interaction_system \
                    .get_interactables_at_pos(target_x, target_y)

                return EventData(success = True,
                                 require = {'target': interactable},
                                 expect  = {'interactions': []})

            return EventData(success = False,
                             result  = {'message': "The way is blocked!"})

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

        def open_check() -> bool:
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

        print(self.entity)

        target = self.game.interaction_system.get_interactables_at_pos(*self.position)

        def lift_check() -> bool:
            """Lift check callback."""

            if target and target.has('Item') and target.has('IsInteractable'):

                return EventData(success = True,
                                 require  = {'target': target,
                                             'instigator': self.entity},
                                 expect   = {'interactions': []})

            return EventData(success = False,
                             result  = {'message': 'You cannot lift that!'})

        action = Action(
            entity = self.entity,
            event  = 'try_pickup',
            check  = lift_check
            ).plan()

        self.action_queue.append(action)
