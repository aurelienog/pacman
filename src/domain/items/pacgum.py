from .item import Item, CollectResult

class Pacgum(Item):
    value = 10

    def on_collect(self) -> CollectResult:
        return CollectResult(self.value)