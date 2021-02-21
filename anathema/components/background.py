from __future__ import annotations
from collections import defaultdict

from ecstremity import Component


class Cultures(defaultdict):

    def __init__(self) -> None:
        self['unset'] = ""
        self['southlander'] = "Southlander"


class Paths(defaultdict):

    def __init__(self) -> None:
        self['unset'] = ""
        self['pauper'] = "Pauper"
        self['farmer'] = "Farmer"
        self['adventurer'] = "Adventurer"


class Background(Component):

    _cultures = Cultures()
    _paths = Paths()

    def __init__(self) -> None:
        self.culture = self._cultures['southlander']
        self.path = self._paths['adventurer']
