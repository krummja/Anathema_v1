from __future__ import annotations
from collections import defaultdict

from ecstremity import Component


class Body(Component):

    def __init__(self) -> None:
        self.body_parts = defaultdict()

        self.body_parts['head'] = None
        self.body_parts['eyes'] = None
        self.body_parts['torso'] = None
        self.body_parts['back'] = None
        self.body_parts['waist'] = None
        self.body_parts['arms'] = None
        self.body_parts['hands'] = None
        self.body_parts['legs'] = None
        self.body_parts['feet'] = None

    def on_attached(self) -> None:
        if self.entity.has('Head'):
            self.body_parts['head'] = self.entity['Head']
            self.body_parts['head'].body = self
        if self.entity.has('Torso'):
            self.body_parts['torso'] = self.entity['Torso']
            self.body_parts['torso'].body = self
        if self.entity.has('Arms'):
            self.body_parts['arms'] = self.entity['Arms']
            self.body_parts['arms'].body = self
        if self.entity.has('Legs'):
            self.body_parts['legs'] = self.entity['Legs']
            self.body_parts['legs'].body = self

        if self.entity.has('Eyes'):
            self.body_parts['eyes'] = self.entity['Eyes']
            self.body_parts['eyes'].body = self

    def equip(self, where: str, item):
        body_part = self.body_parts[where]
        body_part.equip(item)
