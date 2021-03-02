from __future__ import annotations

from ecstremity import Component


class Noun(Component):

    NAME_SET: bool = False
    ALLOW_CHANGE: bool = False

    def __init__(self, noun_text = "") -> None:
        self._noun_text = noun_text

    @property
    def noun_text(self) -> str:
        return self._noun_text

    @property
    def pronoun(self):
        return Pronoun.it

    @noun_text.setter
    def noun_text(self, value: str) -> None:
        if not self.NAME_SET or self.ALLOW_CHANGE:
            self._noun_text = value
            self.NAME_SET = True
        else:
            pass

    def __str__(self) -> str:
        return str(self._noun_text)


class Pronoun:

    nom: str
    obl: str
    gen: str

    def __init__(self, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen

    @classmethod
    def you(self) -> Pronoun:
        return Pronoun('you', 'you', 'your')

    @classmethod
    def she(self) -> Pronoun:
        return Pronoun('she', 'her', 'her')

    @classmethod
    def he(self) -> Pronoun:
        return Pronoun('he', 'him', 'his')

    @classmethod
    def it(self) -> Pronoun:
        return Pronoun('it', 'it', 'its')

    @classmethod
    def they(self) -> Pronoun:
        return Pronoun('they', 'them', 'their')
