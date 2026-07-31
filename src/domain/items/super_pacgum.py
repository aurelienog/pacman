from .item import Item, CollectResult

class SuperPacgum(Item):
    value = 50

    def on_collect(self) -> CollectResult:
        return CollectResult(self.value, frightened_mode=True)