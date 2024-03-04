from collections import namedtuple

from data import Color, Graphic, MobID, MobTag
from items import ItemID


# First item is the result, the rest are the ingredients.
recipies = {
    MobID.WORKBENCH: (
        ((ItemID.WORKBENCH, 1), (ItemID.WOOD, 10)),
        ((ItemID.OVEN, 1), (ItemID.STONE, 10)),
        ((ItemID.FURNACE, 1), (ItemID.STONE, 20)),
        ((ItemID.ANVIL, 1), (ItemID.IRON_BAR, 5)),
        ((ItemID.WOOD_LANTERN, 1), (ItemID.WOOD, 5), (ItemID.SLIME, 4), (ItemID.CLOTH, 2)),
        ((ItemID.TORCH, 2), (ItemID.WOOD, 2), (ItemID.COAL, 1)),
        ((ItemID.WOOD_SWORD, 1), (ItemID.WOOD, 5)),
        ((ItemID.WOOD_PICK, 1), (ItemID.WOOD, 5)),
        ((ItemID.WOOD_AXE, 1), (ItemID.WOOD, 5)),
        ((ItemID.WOOD_SHOVEL, 1), (ItemID.WOOD, 5)),
        ((ItemID.WOOD_HOE, 1), (ItemID.WOOD, 5)),
        ((ItemID.STONE_SWORD, 1), (ItemID.WOOD, 5), (ItemID.STONE, 5)),
        ((ItemID.STONE_PICK, 1), (ItemID.WOOD, 5), (ItemID.STONE, 5)),
        ((ItemID.STONE_AXE, 1), (ItemID.WOOD, 5), (ItemID.STONE, 5)),
        ((ItemID.STONE_SHOVEL, 1), (ItemID.WOOD, 5), (ItemID.STONE, 5)),
        ((ItemID.STONE_HOE, 1), (ItemID.WOOD, 5), (ItemID.STONE, 5)),
        ((ItemID.WINDOW, 1), (ItemID.WOOD, 2), (ItemID.GLASS, 4)),
        ((ItemID.WOOD_WALL, 1), (ItemID.WOOD, 4)),
        ((ItemID.WOOD_DOOR, 1), (ItemID.WOOD, 8)),
        ((ItemID.STONE_WALL, 1), (ItemID.STONE, 4)),
        ((ItemID.COCKTAIL, 1), (ItemID.BOTTLE, 1), (ItemID.APPLE, 1), (ItemID.COCONUT, 1), (ItemID.POKE_PEAR, 1)),
    ),
    MobID.OVEN: (
        ((ItemID.BREAD, 1), (ItemID.WHEAT, 5)),
        ((ItemID.APPLE_PIE, 1), (ItemID.WHEAT, 5), (ItemID.APPLE, 5)),
        ((ItemID.GOLD_APPLE, 1), (ItemID.APPLE, 1), (ItemID.GOLD_BAR, 15)),
    ),
    MobID.FURNACE: (
        ((ItemID.GLASS, 1), (ItemID.SAND, 4), (ItemID.COAL, 1)),
        ((ItemID.BOTTLE, 1), (ItemID.GLASS, 2), (ItemID.COAL, 1)),
        ((ItemID.IRON_BAR, 1), (ItemID.IRON_ORE, 4), (ItemID.COAL, 1)),
        ((ItemID.GOLD_BAR, 1), (ItemID.GOLD_ORE, 4), (ItemID.COAL, 1)),
    ),
    MobID.ANVIL: (
        ((ItemID.IRON_SWORD, 1), (ItemID.WOOD, 5), (ItemID.IRON_BAR, 5)),
        ((ItemID.IRON_PICK, 1), (ItemID.WOOD, 5), (ItemID.IRON_BAR, 5)),
        ((ItemID.IRON_AXE, 1), (ItemID.WOOD, 5), (ItemID.IRON_BAR, 5)),
        ((ItemID.IRON_SHOVEL, 1), (ItemID.WOOD, 5), (ItemID.IRON_BAR, 5)),
        ((ItemID.IRON_HOE, 1), (ItemID.WOOD, 5), (ItemID.IRON_BAR, 5)),
        ((ItemID.GOLD_SWORD, 1), (ItemID.WOOD, 5), (ItemID.GOLD_BAR, 5)),
        ((ItemID.GOLD_PICK, 1), (ItemID.WOOD, 5), (ItemID.GOLD_BAR, 5)),
        ((ItemID.GOLD_AXE, 1), (ItemID.WOOD, 5), (ItemID.GOLD_BAR, 5)),
        ((ItemID.GOLD_SHOVEL, 1), (ItemID.WOOD, 5), (ItemID.GOLD_BAR, 5)),
        ((ItemID.GOLD_HOE, 1), (ItemID.WOOD, 5), (ItemID.GOLD_BAR, 5)),
        ((ItemID.GEM_SWORD, 1), (ItemID.WOOD, 5), (ItemID.GEM, 50)),
        ((ItemID.GEM_PICK, 1), (ItemID.WOOD, 5), (ItemID.GEM, 50)),
        ((ItemID.GEM_AXE, 1), (ItemID.WOOD, 5), (ItemID.GEM, 50)),
        ((ItemID.GEM_SHOVEL, 1), (ItemID.WOOD, 5), (ItemID.GEM, 50)),
        ((ItemID.GEM_HOE, 1), (ItemID.WOOD, 5), (ItemID.GEM, 50)),
    ),
}


MobData = namedtuple("MobData", ("name", "graphic", "max_health", "tags",
                                 "recipies", "light"), defaults=(10, tuple(), None, 0))
mob_data = {
    MobID.PLAYER: MobData("player", (Graphic.PLAYER, Color.WHITE), 10, tuple(), tuple(), 3),
    MobID.GREEN_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_GREEN), 10, (MobTag.AI_FOLLOW,)),
    MobID.GREEN_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_GREEN), 10, (MobTag.AI_JUMP,)),
    MobID.GREEN_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_GREEN), 10,
                                  (MobTag.PUSHABLE, MobTag.AI_SHOOT)),
    MobID.AIR_WIZARD: MobData("air wizard", (Graphic.AIR_WIZARD, Color.RED), 100),
    MobID.WORKBENCH: MobData("workbench", (Graphic.WORKBENCH, Color.BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING), recipies[MobID.WORKBENCH]),
    MobID.OVEN: MobData("oven", (Graphic.OVEN, Color.LIGHT_BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING), recipies[MobID.OVEN]),
    MobID.FURNACE: MobData("furnace", (Graphic.FURNACE, Color.LIGHT_GRAY), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING), recipies[MobID.FURNACE]),
    MobID.ANVIL: MobData("anvil", (Graphic.ANVIL, Color.LIGHT_GRAY), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING), recipies[MobID.ANVIL]),
    MobID.WOOD_LANTERN: MobData("wood lantern", (Graphic.LANTERN, Color.BROWN), 10,
                             (MobTag.PUSHABLE, ), tuple(), 10),
    MobID.TORCH: MobData("torch", (Graphic.TORCH, Color.YELLOW), 8,
                             (MobTag.PUSHABLE, ), tuple(), 5),
}


class Mob:
    def __init__(self, mobid: MobID):
        self.id = mobid
        self.mob_data = mob_data[self.id]
        self.name = self.mob_data.name
        self.graphic = self.mob_data.graphic
        self.health = self.mob_data.max_health
        self.tags = self.mob_data.tags
        self.recipies = self.mob_data.recipies
        self.light = self.mob_data.light

    def has_tag(self, tag: MobTag) -> bool:
        return tag in self.tags
