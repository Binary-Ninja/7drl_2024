from collections import namedtuple

from data import Color, Graphic, MobID, ItemID, ItemTag, TileID

item_to_mob = {
    MobID.WORKBENCH: ItemID.WORKBENCH,
}

ItemData = namedtuple("ItemData", ("name", "graphic", "tags", "data"),
                      defaults=(tuple(), tuple()))
item_data = {
    ItemID.WORKBENCH: ItemData("workbench", (Graphic.WORKBENCH, Color.BROWN),
                               (ItemTag.SPAWN_MOB,), (MobID.WORKBENCH,)),
    ItemID.DIRT: ItemData("dirt", (Graphic.DIRT, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE),
                          (TileID.DIRT, TileID.HOLE, TileID.WATER)),
    ItemID.STONE: ItemData("stone", (Graphic.STONE_ITEM, Color.STONE),
                           (ItemTag.STACKABLE,), ),
    ItemID.SAND: ItemData("sand", (Graphic.SAND, Color.YELLOW),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE),
                          (TileID.SAND, TileID.DIRT)),
    ItemID.WOOD: ItemData("wood", (Graphic.WOOD, Color.BROWN), (ItemTag.STACKABLE,), ),
    ItemID.PICKUP: ItemData("pickup", (Graphic.PICKUP, Color.BROWN), (ItemTag.PICKUP,),
                            item_to_mob),
    ItemID.APPLE: ItemData("apple", (Graphic.APPLE, Color.RED),
                           (ItemTag.STACKABLE, ItemTag.HEAL), (1,)),
    ItemID.WHEAT_SEEDS: ItemData("seeds", (Graphic.SEEDS, Color.GREEN), (ItemTag.STACKABLE,)),
    ItemID.WOOD_PICK: ItemData("wood pick", (Graphic.PICKAXE, Color.BROWN),
                               (ItemTag.BREAK_TILE,), (TileID.STONE,)),
    ItemID.WOOD_SWORD: ItemData("wood sword", (Graphic.SWORD, Color.BROWN),
                               (ItemTag.DAMAGE_MOBS,), (2,))
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
        self.data = self.item_data.data

    def has_tag(self, tag: ItemTag) -> bool:
        return tag in self.tags

    def __str__(self):
        return (f"{self.count} " if self.stackable else "") + self.name
