from data import ItemID, item_tags, item_graphics, item_names, ItemTag


class Item:
    def __init__(self, itemid: ItemID, count: int = 1):
        self.name = item_names[itemid]
        self.graphic = item_graphics[itemid]
        self.stackable = ItemTag.STACKABLE in item_tags[itemid]
        self.count = count

    def __str__(self):
        return self.name
