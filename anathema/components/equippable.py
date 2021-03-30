from __future__ import annotations

from ecstremity import Component


class Equippable(Component):

    def __init__(self, body_part: str) -> None:
        self.body_part = body_part
        self._owner = None

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value) -> None:
        self._owner = value

    @staticmethod
    def on_get_interactions(evt):
        evt.data['expect'].append({
            'name': 'Equip',
            'evt': 'try_equip'
            })
