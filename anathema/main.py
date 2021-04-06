import nocterminal as noc
import ecstremity as ecs


class Game:

    def __init__(self):
        self.engine = ecs.EngineAdapter(client=self)
