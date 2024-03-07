from collections import namedtuple, defaultdict
import random
from typing import Sequence

from data import ItemID, TileID, MobID
from items import Item

LootItem = namedtuple("LootItem", ("id", "prob", "min", "max"),
                      defaults=(1.0, 1, 1))

tile_break_loot = defaultdict(tuple)
tile_break_loot.update({
    TileID.GRASS: (LootItem(ItemID.WHEAT_SEEDS, 0.4), ),
    TileID.SAND: (LootItem(ItemID.SAND), ),
    TileID.STONE: (LootItem(ItemID.STONE, 1.0, 2, 5), LootItem(ItemID.COAL, 0.5, 1, 3)),
    TileID.TREE: (LootItem(ItemID.WOOD, 1.0, 2, 5), LootItem(ItemID.APPLE, 0.5, 1, 3),
                  LootItem(ItemID.TREE_SAPLING, 0.8, 1, 2)),
    TileID.CACTUS: (LootItem(ItemID.WOOD), LootItem(ItemID.POKE_PEAR, 0.5, 1, 2),
                    LootItem(ItemID.CACTUS_SAPLING, 0.8, 1, 2)),
    TileID.DIRT: (LootItem(ItemID.DIRT), ),
    TileID.WHEAT: (LootItem(ItemID.WHEAT, 1.0, 3, 4), ),
    TileID.TUBER_CROP: (LootItem(ItemID.TUBER, 1.0, 3, 4),),
    TileID.PALM_TREE: (LootItem(ItemID.WOOD, 1.0, 1, 3), LootItem(ItemID.COCONUT, 0.8, 1, 3),
                       LootItem(ItemID.PALM_TREE_SAPLING, 0.8, 1, 2)),
    TileID.IRON_ORE: (LootItem(ItemID.IRON_ORE, 1.0, 2, 4), ),
    TileID.GOLD_ORE: (LootItem(ItemID.GOLD_ORE, 1.0, 2, 4), ),
    TileID.GEM_ORE: (LootItem(ItemID.GEM, 1.0, 4, 10), ),
    TileID.DESERT_BONES: (LootItem(ItemID.BONE, 1.0, 2, 4), ),
    TileID.ASH_BONES: (LootItem(ItemID.BONE, 1.0, 2, 4), LootItem(ItemID.COAL, 1.0, 1, 2),
                       LootItem(ItemID.ASH, 1.0, 2, 4)),
    TileID.WINDOW: (LootItem(ItemID.WINDOW, 1.0, 1, 1), ),
    TileID.WOOD_WALL: (LootItem(ItemID.WOOD_WALL),),
    TileID.STONE_WALL: (LootItem(ItemID.STONE_WALL),),
    TileID.WOOD_FLOOR: (LootItem(ItemID.WOOD_FLOOR),),
    TileID.STONE_FLOOR: (LootItem(ItemID.STONE_FLOOR),),
    TileID.CLOSED_WOOD_DOOR: (LootItem(ItemID.WOOD_DOOR),),
    TileID.OPEN_WOOD_DOOR: (LootItem(ItemID.WOOD_DOOR),),
    TileID.TREE_SAPLING: (LootItem(ItemID.TREE_SAPLING),),
    TileID.PALM_TREE_SAPLING: (LootItem(ItemID.PALM_TREE_SAPLING),),
    TileID.CACTUS_SAPLING: (LootItem(ItemID.CACTUS_SAPLING),),
    TileID.SHROOM_SAPLING: (LootItem(ItemID.SHROOM_SAPLING),),
    TileID.CLOUD: (LootItem(ItemID.CLOUD),),
    TileID.CLOUD_BANK: (LootItem(ItemID.CLOUD, 1.0, 2, 4),),
    TileID.WHEAT_SEEDS: (LootItem(ItemID.WHEAT_SEEDS),),
    TileID.LAPIS_ORE: (LootItem(ItemID.LAPIS, 1.0, 2, 3),),
    TileID.WEB: (LootItem(ItemID.STRING, 1.0, 2, 4),),
    TileID.THORNS: (LootItem(ItemID.WOOD, 0.5),),
    TileID.FLOOR_FUNGUS: (LootItem(ItemID.FUNGUS, 1.0, 1, 2),),
    TileID.BIG_MUSHROOM: (LootItem(ItemID.SHROOM_SAPLING, 0.8, 1, 2), LootItem(ItemID.FUNGUS, 1.0, 2, 4),
                          LootItem(ItemID.TUBER_SEEDS, 1.0, 2, 3)),
    TileID.QUARTZ_ORE: (LootItem(ItemID.QUARTZ, 1.0, 1, 3),),
    TileID.TUBER_SEEDS: (LootItem(ItemID.TUBER_SEEDS),),
    TileID.OBSIDIAN_BRICKS: (LootItem(ItemID.OBSIDIAN_WALL),),
    TileID.OBSIDIAN_FLOOR: (LootItem(ItemID.OBSIDIAN_FLOOR),),
    TileID.OBSIDIAN: (LootItem(ItemID.OBSIDIAN, 1.0, 2, 4),),
})

mob_death_loot = defaultdict(tuple)
mob_death_loot.update({
    MobID.GREEN_ZOMBIE: (LootItem(ItemID.CLOTH, 1.0, 1, 3), LootItem(ItemID.WHEAT, 0.05, 1, 1)),
    MobID.GREEN_SLIME: (LootItem(ItemID.SLIME, 1.0, 2, 4),),
    MobID.GREEN_SKELETON: (LootItem(ItemID.BONE, 1.0, 2, 3),),
    MobID.RED_ZOMBIE: (LootItem(ItemID.CLOTH, 1.0, 1, 3), LootItem(ItemID.WHEAT, 0.05, 1, 1)),
    MobID.RED_SLIME: (LootItem(ItemID.SLIME, 1.0, 2, 4),),
    MobID.RED_SKELETON: (LootItem(ItemID.BONE, 1.0, 2, 3),),
    MobID.WHITE_ZOMBIE: (LootItem(ItemID.CLOTH, 1.0, 1, 3), LootItem(ItemID.WHEAT, 0.05, 1, 1)),
    MobID.WHITE_SLIME: (LootItem(ItemID.SLIME, 1.0, 2, 4),),
    MobID.WHITE_SKELETON: (LootItem(ItemID.BONE, 1.0, 2, 3),),
    MobID.BLACK_ZOMBIE: (LootItem(ItemID.CLOTH, 1.0, 1, 3), LootItem(ItemID.WHEAT, 0.05, 1, 1)),
    MobID.BLACK_SLIME: (LootItem(ItemID.SLIME, 1.0, 2, 4),),
    MobID.BLACK_SKELETON: (LootItem(ItemID.BONE, 1.0, 2, 3), LootItem(ItemID.GOLD_APPLE, 0.02, 1, 1)),
    MobID.FLAME_SKULL: (LootItem(ItemID.BONE, 1.0, 3, 4), LootItem(ItemID.COAL, 1.0, 1, 2)),
    MobID.SPIDER: (LootItem(ItemID.STRING, 1.0, 1, 4), LootItem(ItemID.SPIDER_EYE, 0.2, 1, 8)),
    MobID.HELL_SPIDER: (LootItem(ItemID.STRING, 1.0, 1, 4), LootItem(ItemID.SPIDER_EYE, 0.2, 1, 8)),
    MobID.CLOUD_SPIDER: (LootItem(ItemID.STRING, 1.0, 1, 4), LootItem(ItemID.SPIDER_EYE, 0.2, 1, 8)),
    MobID.SHADE: (LootItem(ItemID.WORKBENCH, 0.2, 1, 1), LootItem(ItemID.ASH, 0.2, 1, 3),
                  LootItem(ItemID.PASTRY, 0.1, 1, 1), LootItem(ItemID.IRON_LANTERN, 0.1, 1, 1),
                  LootItem(ItemID.FISH_SPEAR, 0.1, 1, 1), LootItem(ItemID.FUNGUS, 0.1, 1, 3),
                  LootItem(ItemID.LAPIS, 0.05, 1, 5), LootItem(ItemID.SAND, 0.2, 1, 3),
                  LootItem(ItemID.WINDOW, 0.1, 1, 1), LootItem(ItemID.COCONUT, 0.2, 1, 2),
                  LootItem(ItemID.COCKTAIL, 0.05, 1, 1), LootItem(ItemID.DUCK_EGG, 0.1, 1, 1),
                  LootItem(ItemID.CAT_EGG, 0.1, 1, 1), LootItem(ItemID.DOG_EGG, 0.1, 1, 1),
                  LootItem(ItemID.CHICKEN_EGG, 0.1, 1, 1), LootItem(ItemID.PIG_EGG, 0.1, 1, 1),
                  ),
    MobID.DUCK: (LootItem(ItemID.DUCK_MEAT, 1.0, 1, 2),),
    MobID.DOG: (LootItem(ItemID.DUCK_MEAT, 1.0, 1, 2),),
    MobID.CAT: (LootItem(ItemID.DUCK_MEAT, 1.0, 1, 2),),
    MobID.PIG: (LootItem(ItemID.DUCK_MEAT, 1.0, 1, 2),),
    MobID.CHICKEN: (LootItem(ItemID.DUCK_MEAT, 1.0, 1, 2),),
    MobID.FAIRY: (LootItem(ItemID.FAIRY_DUST, 1.0, 1, 3), ),
    MobID.SPRITE: (LootItem(ItemID.FAIRY_DUST, 1.0, 1, 3),),
    MobID.UFO: (LootItem(ItemID.CIRCUIT, 0.7, 2, 4), LootItem(ItemID.IRON_BAR, 0.5, 1, 2),
                LootItem(ItemID.GLASS, 0.8, 1, 4), LootItem(ItemID.QUARTZ, 0.4, 1, 3),
                LootItem(ItemID.ASH, 0.4, 4, 5), LootItem(ItemID.CIRCUIT, 1.0, 1, 3),
                ),
})

fishing_loot = defaultdict(tuple)
fishing_loot.update({
    TileID.WATER: (LootItem(ItemID.FISH), LootItem(ItemID.FISH),
                   LootItem(ItemID.FISH), LootItem(ItemID.FISH),
                   LootItem(ItemID.FISH), LootItem(ItemID.FISH),
                   LootItem(ItemID.DEEP_FISH), LootItem(ItemID.DEEP_FISH),
                   LootItem(ItemID.DEEP_FISH), LootItem(ItemID.DEEP_FISH),
                   LootItem(ItemID.BONE), LootItem(ItemID.BOTTLE),
                   LootItem(ItemID.SLIME), LootItem(ItemID.STRING),
                   LootItem(ItemID.FISH), LootItem(ItemID.COCKTAIL),
                   ),
    TileID.LAVA: (
        LootItem(ItemID.FIRE_FISH), LootItem(ItemID.FIRE_FISH),
        LootItem(ItemID.FIRE_FISH), LootItem(ItemID.FIRE_FISH),
        LootItem(ItemID.FIRE_FISH), LootItem(ItemID.FIRE_FISH),
        LootItem(ItemID.FIRE_FISH), LootItem(ItemID.FIRE_FISH),
        LootItem(ItemID.FIRE_FISH), LootItem(ItemID.FIRE_FISH),
        LootItem(ItemID.BONE), LootItem(ItemID.IRON_ORE),
        LootItem(ItemID.BONE), LootItem(ItemID.IRON_ORE),
        LootItem(ItemID.BONE), LootItem(ItemID.GOLD_ORE),
        LootItem(ItemID.BONE), LootItem(ItemID.GOLD_ORE),
        LootItem(ItemID.LAPIS), LootItem(ItemID.GOLD_APPLE),
        LootItem(ItemID.GEM), LootItem(ItemID.GEM_FISH_SPEAR),
    ),
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
