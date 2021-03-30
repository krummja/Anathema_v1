from __future__ import annotations

from ecstremity import Component, Entity


class Stackable(Component):

    def __init__(self, identifier: str, quantity: int = 1) -> None:
        self.identifier = identifier
        self.quantity = quantity

    @property
    def display(self) -> str:
        return f"x {self.quantity}"

    def increment(self, amount: int) -> None:
        self.quantity += amount

    def add_other(self, other) -> None:
        self.increment(other['Stackable'].quantity)
        other['Stackable'].quantity = 0
        other.add('IsDestroying', {})

    def split(self, quantity: int):
        quantity = min(max(0, quantity), self.quantity)
        clone = self.entity.clone()
        clone['Stackable'].quantity -= quantity
        self.quantity = quantity

        if clone.has('IsInventoried'):
            clone['IsInventoried'].owner['Inventory'].contents.append(clone)

        return clone


class Inventory(Component):

    def __init__(self) -> None:
        self.contents = []

    def on_destroyed(self) -> None:
        for entity in self.contents:
            entity.destroy()

    def get_stackable(self, identifier: str):
        pass

    def add_to(self, item: Entity):
        # if item.has('Stackable'):
        #     existing = self.get_stackable(item['Stackable'].identifier)
        #     if existing:
        #         existing['Stackable'].add_other(item)
        #         return
        item.add('IsInventoried', {'owner': self.entity})
        self.contents.append(item)

    def take_from(self, item):
        pass

    def drop_from(self, item):
        item['IsInventoried'].destroy()
        item['Position'].xy = self.entity['Position'].xy
        self.contents.remove(item)
