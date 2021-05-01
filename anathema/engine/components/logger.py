from ecstremity import *


class Logger(Component):

    @property
    def moniker(self):
        return self.entity

    def on_log(self, evt: EntityEvent) -> None:
        print(f"{self.moniker}: {evt.data}")
        evt.handle()
