from enum import Enum, auto
from collections import namedtuple

from data import Color, Graphic


class ItemID(Enum):
    WORKBENCH = 1
    DIRT = 2
    STONE = 3
    SAND = 4
    WOOD = 5
    PICKUP = 6


class ItemTag(Enum):
    STACKABLE = auto()


ItemData = namedtuple("ItemData", ("name", "graphic", "tags"))
item_data = {
    ItemID.WORKBENCH: ItemData("workbench", (Graphic.WORKBENCH, Color.BROWN), tuple(), ),
    ItemID.DIRT: ItemData("dirt", (Graphic.DIRT, Color.BROWN), (ItemTag.STACKABLE,), ),
    ItemID.STONE: ItemData("stone", (Graphic.STONE_ITEM, Color.STONE),
                           (ItemTag.STACKABLE,), ),
    ItemID.SAND: ItemData("sand", (Graphic.SAND, Color.YELLOW), (ItemTag.STACKABLE,), ),
    ItemID.WOOD: ItemData("wood", (Graphic.WOOD, Color.BROWN), (ItemTag.STACKABLE,), ),
    ItemID.PICKUP: ItemData("pickup", (Graphic.PICKUP, Color.BROWN), tuple(), ),
}


class Item:
    def __init__(self, itemid: ItemID, count: int = 1):
        self.id = itemid
        self.item_data = item_data[self.id]
        self.name = self.item_data.name
        self.graphic = self.item_data.graphic
        self.tags = self.item_data.tags
        self.stackable = ItemTag.STACKABLE in self.tags
        self.count = count

    def has_tag(self, tag: ItemTag) -> bool:
        return tag in self.tags

    def __str__(self):
        return (f"{self.count} " if self.stackable else "") + self.name
