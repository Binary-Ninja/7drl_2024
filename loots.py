from collections import namedtuple, defaultdict
import random
from typing import Sequence

from data import ItemID, TileID
from items import Item

LootItem = namedtuple("LootItem", ("id", "prob", "min", "max"),
                      defaults=(1.0, 1, 1))

tile_break_loot = defaultdict(tuple)
tile_break_loot.update({
    TileID.GRASS: (LootItem(ItemID.WHEAT_SEEDS, 0.4), ),
    TileID.SAND: (LootItem(ItemID.SAND), ),
    TileID.STONE: (LootItem(ItemID.STONE, 1.0, 2, 5), LootItem(ItemID.COAL, 0.8, 1, 3)),
    TileID.TREE: (LootItem(ItemID.WOOD, 1.0, 2, 5), LootItem(ItemID.APPLE, 0.5, 1, 3)),
    TileID.CACTUS: (LootItem(ItemID.WOOD), ),
    TileID.DIRT: (LootItem(ItemID.DIRT), ),
    TileID.WHEAT: (LootItem(ItemID.WHEAT, 1.0, 3, 4), ),
    TileID.PALM_TREE: (LootItem(ItemID.WOOD, 1.0, 1, 3), LootItem(ItemID.COCONUT, 0.8, 1, 3)),
    TileID.IRON_ORE: (LootItem(ItemID.IRON_ORE, 1.0, 3, 6), ),
    TileID.GOLD_ORE: (LootItem(ItemID.GOLD_ORE, 1.0, 3, 6), ),
    TileID.GEM_ORE: (LootItem(ItemID.GEM, 1.0, 3, 6), ),
    TileID.DESERT_BONES: (LootItem(ItemID.BONE, 1.0, 2, 4), ),
    TileID.WINDOW: (LootItem(ItemID.GLASS, 1.0, 2, 4), LootItem(ItemID.WOOD, 1.0, 2, 2)),
    TileID.WOOD_WALL: (LootItem(ItemID.WOOD_WALL),),
    TileID.STONE_WALL: (LootItem(ItemID.STONE_WALL),),
    TileID.CLOSED_WOOD_DOOR: (LootItem(ItemID.WOOD_DOOR),),
    TileID.OPEN_WOOD_DOOR: (LootItem(ItemID.WOOD_DOOR),),
})


def resolve_loot(loot_list: Sequence[LootItem]) -> list[Item]:
    item_list: list[Item] = []
    for loot_item in loot_list:
        if random.random() > loot_item.prob:
            continue
        count = random.randint(loot_item.min, loot_item.max)
        if count <= 0:
            continue
        item_list.append(Item(loot_item.id, count))
    return item_list
