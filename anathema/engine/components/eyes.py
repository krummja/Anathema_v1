from ecstremity import Component


class Eyes(Component):

    def __init__(self, sight_range: int = 8) -> None:
        self.sight_range = sight_range
