from __future__ import annotations

from ecstremity import Component


class Body(Component):

    def __init__(self) -> None:
        self.head = None
        self.torso = None
        self.arms = None
        self.legs = None
        self.eyes = None

    def on_attached(self) -> None:
        if self.entity.has('Head'):
            self.head = self.entity['Head']
            self.head.body = self
        if self.entity.has('Torso'):
            self.torso = self.entity['Torso']
            self.torso.body = self
        if self.entity.has('Arms'):
            self.Arms = self.entity['Arms']
            self.torso.arms = self
        if self.entity.has('Legs'):
            self.legs = self.entity['Legs']
            self.legs.body = self

        if self.entity.has('Eyes'):
            self.eyes = self.entity['Eyes']
            self.eyes.body = self

    def equip(self, where: str):
        body_part = getattr(self, where)
