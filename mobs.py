from collections import namedtuple, defaultdict

from data import Color, Graphic, MobID, MobTag, Point
from items import ItemID


# First item is the result, the rest are the ingredients.
recipies = {
    MobID.WORKBENCH: (
        ((ItemID.WORKBENCH, 1), (ItemID.WOOD, 10)),
        ((ItemID.OVEN, 1), (ItemID.STONE, 10)),
        ((ItemID.FURNACE, 1), (ItemID.STONE, 20)),
        ((ItemID.ANVIL, 1), (ItemID.IRON_BAR, 5)),
        ((ItemID.WOOD_LANTERN, 1), (ItemID.WOOD, 5), (ItemID.SLIME, 4), (ItemID.CLOTH, 2), (ItemID.GLASS, 4)),
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
        ((ItemID.STRING, 4), (ItemID.CLOTH, 1), ),
        ((ItemID.CLOTH, 1), (ItemID.STRING, 4)),
        ((ItemID.BED, 1), (ItemID.WOOD, 10), (ItemID.CLOTH, 10)),
        ((ItemID.WOOD_WALL, 1), (ItemID.WOOD, 4)),
        ((ItemID.WOOD_DOOR, 1), (ItemID.WOOD, 8)),
        ((ItemID.STONE_WALL, 1), (ItemID.STONE, 4)),
        ((ItemID.COCKTAIL, 1), (ItemID.BOTTLE, 1), (ItemID.APPLE, 1), (ItemID.COCONUT, 1), (ItemID.POKE_PEAR, 1)),
    ),
    MobID.OVEN: (
        ((ItemID.BREAD, 1), (ItemID.WHEAT, 5), (ItemID.WOOD, 2)),
        ((ItemID.COOKED_TUBER, 1), (ItemID.TUBER, 1), (ItemID.WOOD, 2)),
        ((ItemID.APPLE_PIE, 1), (ItemID.WHEAT, 5), (ItemID.APPLE, 5), (ItemID.WOOD, 2)),
        ((ItemID.PASTRY, 1), (ItemID.COOKED_TUBER, 5), (ItemID.WHEAT, 5), (ItemID.WOOD, 2)),
        ((ItemID.COOKED_FISH, 1), (ItemID.FISH, 1), (ItemID.WOOD, 2)),
        ((ItemID.COOKED_DEEP_FISH, 1), (ItemID.DEEP_FISH, 1), (ItemID.WOOD, 2)),
        ((ItemID.COOKED_DUCK_MEAT, 1), (ItemID.DUCK_MEAT, 1), (ItemID.WOOD, 2)),
        ((ItemID.BOILED_EGG, 1), (ItemID.DUCK_EGG, 1), (ItemID.WOOD, 2)),
    ),
    MobID.FURNACE: (
        ((ItemID.GLASS, 1), (ItemID.SAND, 4), (ItemID.COAL, 1)),
        ((ItemID.BOTTLE, 1), (ItemID.GLASS, 2), (ItemID.COAL, 1)),
        ((ItemID.WINDOW, 1), (ItemID.GLASS, 4),),
        ((ItemID.IRON_BAR, 1), (ItemID.IRON_ORE, 4), (ItemID.COAL, 1)),
        ((ItemID.GOLD_BAR, 1), (ItemID.GOLD_ORE, 4), (ItemID.COAL, 1)),
        ((ItemID.GOLD_APPLE, 1), (ItemID.APPLE, 1), (ItemID.GOLD_BAR, 15), (ItemID.COAL, 2)),
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
        ((ItemID.IRON_LANTERN, 1), (ItemID.IRON_BAR, 5), (ItemID.SLIME, 4), (ItemID.CLOTH, 2), (ItemID.GLASS, 4)),
        ((ItemID.GOLD_LANTERN, 1), (ItemID.GOLD_BAR, 5), (ItemID.SLIME, 4), (ItemID.CLOTH, 2), (ItemID.GLASS, 4)),
        ((ItemID.GEM_LANTERN, 1), (ItemID.GEM, 25), (ItemID.SLIME, 4), (ItemID.CLOTH, 2), (ItemID.GLASS, 4)),
    ),
}

mob_damage = {
    MobID.GREEN_ZOMBIE: 1,
    MobID.GREEN_SLIME: 1,
    MobID.GREEN_SKELETON: 1,
    MobID.RED_ZOMBIE: 2,
    MobID.RED_SLIME: 2,
    MobID.RED_SKELETON: 2,
    MobID.WHITE_ZOMBIE: 3,
    MobID.WHITE_SLIME: 3,
    MobID.WHITE_SKELETON: 3,
    MobID.BLACK_ZOMBIE: 4,
    MobID.BLACK_SLIME: 4,
    MobID.BLACK_SKELETON: 4,
    MobID.AIR_WIZARD: 5,
    MobID.BAT: 0,
    MobID.FLAME_SKULL: 2,
    MobID.SPIDER: 2,
    MobID.HELL_SPIDER: 3,
    MobID.CLOUD_SPIDER: 4,
    MobID.FAIRY: 3,
}

mob_ai_timer = defaultdict(lambda: 1)
mob_ai_timer.update({
    MobID.GREEN_ZOMBIE: 3,
    MobID.GREEN_SLIME: 3,
    MobID.GREEN_SKELETON: 2,
    MobID.RED_ZOMBIE: 3,
    MobID.RED_SLIME: 3,
    MobID.RED_SKELETON: 2,
    MobID.WHITE_ZOMBIE: 3,
    MobID.WHITE_SLIME: 3,
    MobID.WHITE_SKELETON: 3,
    MobID.BLACK_ZOMBIE: 3,
    MobID.BLACK_SLIME: 2,
    MobID.BLACK_SKELETON: 4,
    MobID.AIR_WIZARD: 2,
    MobID.BAT: 1,
    MobID.FLAME_SKULL: 1,
    MobID.SPIDER: 1,
    MobID.HELL_SPIDER: 1,
    MobID.SHADE: 1,
    MobID.FAIRY: 1,
})


MobData = namedtuple("MobData", ("name", "graphic", "max_health", "tags",
                                 "recipies", "light"), defaults=(10, tuple(), None, 0))
mob_data = {
    MobID.PLAYER: MobData("player", (Graphic.PLAYER, Color.WHITE), 10, (MobTag.NO_DESPAWN,), tuple(), 0),
    MobID.BAT: MobData("bat", (Graphic.BAT, Color.BROWN), 5, (MobTag.AI_WANDER,)),
    MobID.DUCK: MobData("duck", (Graphic.DUCK, Color.YELLOW), 2, (MobTag.AI_FOLLOW, MobTag.SWAPPABLE)),
    MobID.DOG: MobData("dog", (Graphic.DOG, Color.BROWN), 2, (MobTag.AI_FOLLOW, MobTag.SWAPPABLE)),
    MobID.CAT: MobData("cat", (Graphic.CAT, Color.ORANGE), 2, (MobTag.AI_FOLLOW, MobTag.SWAPPABLE)),
    MobID.PIG: MobData("pig", (Graphic.PIG, Color.PINK), 2, (MobTag.AI_FOLLOW, MobTag.SWAPPABLE)),
    MobID.CHICKEN: MobData("chicken", (Graphic.CHICKEN, Color.WHITE), 2, (MobTag.AI_FOLLOW, MobTag.SWAPPABLE)),
    MobID.SHADE: MobData("shade", (Graphic.SHADE, Color.BLUE), 20, (MobTag.AI_FLEE, MobTag.NO_DESPAWN), tuple(), 1),
    MobID.FLAME_SKULL: MobData("fireskull", (Graphic.SKULL, Color.YELLOW), 20, (MobTag.AI_WANDER, MobTag.DAMAGE,),
                               tuple(), 1),
    MobID.FAIRY: MobData("pixie", (Graphic.FAIRY, Color.PINK), 5, (MobTag.AI_WANDER, MobTag.DAMAGE, MobTag.NO_DESPAWN),
                               tuple(), 1),
    MobID.SPIDER: MobData("spider", (Graphic.SPIDER, Color.MED_GRAY), 10, (MobTag.AI_SPIDER, MobTag.DAMAGE,)),
    MobID.HELL_SPIDER: MobData("hellspider", (Graphic.SPIDER, Color.RED), 10, (MobTag.AI_SPIDER, MobTag.DAMAGE)),
    MobID.CLOUD_SPIDER: MobData("skyspider", (Graphic.SPIDER, Color.LIGHT_BLUE), 10, (MobTag.AI_SPIDER, MobTag.DAMAGE,
                                                                                      MobTag.NO_DESPAWN)),
    MobID.GREEN_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_GREEN), 10, (MobTag.AI_FOLLOW, MobTag.DAMAGE)),
    MobID.GREEN_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_GREEN), 5, (MobTag.AI_JUMP, MobTag.DAMAGE)),
    MobID.GREEN_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_GREEN), 10,
                                  (MobTag.PUSHABLE, MobTag.AI_SHOOT, MobTag.DAMAGE)),
    MobID.RED_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_RED), 10, (MobTag.AI_FOLLOW, MobTag.DAMAGE)),
    MobID.RED_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_RED), 5, (MobTag.AI_JUMP, MobTag.DAMAGE)),
    MobID.RED_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_RED), 10,
                                  (MobTag.PUSHABLE, MobTag.AI_SHOOT, MobTag.DAMAGE)),
    MobID.WHITE_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_WHITE), 10, (MobTag.AI_FOLLOW, MobTag.DAMAGE)),
    MobID.WHITE_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_WHITE), 5, (MobTag.AI_JUMP, MobTag.DAMAGE)),
    MobID.WHITE_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_WHITE), 10,
                                  (MobTag.PUSHABLE, MobTag.AI_SHOOT, MobTag.DAMAGE)),
    MobID.BLACK_ZOMBIE: MobData("zombie", (Graphic.ZOMBIE, Color.MOB_BLACK), 10, (MobTag.AI_FOLLOW, MobTag.DAMAGE,
                                                                                  MobTag.NO_DESPAWN)),
    MobID.BLACK_SLIME: MobData("slime", (Graphic.SLIME, Color.MOB_BLACK), 5, (MobTag.AI_JUMP, MobTag.DAMAGE,
                                                                              MobTag.NO_DESPAWN)),
    MobID.BLACK_SKELETON: MobData("skeleton", (Graphic.SKELETON, Color.MOB_BLACK), 10,
                                  (MobTag.PUSHABLE, MobTag.AI_SHOOT, MobTag.DAMAGE, MobTag.NO_DESPAWN)),
    MobID.AIR_WIZARD: MobData("air wizard", (Graphic.AIR_WIZARD, Color.RED), 100, (MobTag.DAMAGE, MobTag.NO_DESPAWN)),
    MobID.WORKBENCH: MobData("workbench", (Graphic.WORKBENCH, Color.BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING, MobTag.NO_DESPAWN), recipies[MobID.WORKBENCH]),
    MobID.OVEN: MobData("oven", (Graphic.OVEN, Color.LIGHT_BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING, MobTag.NO_DESPAWN), recipies[MobID.OVEN]),
    MobID.FURNACE: MobData("furnace", (Graphic.FURNACE, Color.LIGHT_GRAY), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING, MobTag.NO_DESPAWN), recipies[MobID.FURNACE]),
    MobID.ANVIL: MobData("anvil", (Graphic.ANVIL, Color.LIGHT_GRAY), 10,
                             (MobTag.PUSHABLE, MobTag.CRAFTING, MobTag.NO_DESPAWN), recipies[MobID.ANVIL]),
    MobID.WOOD_LANTERN: MobData("wood lantern", (Graphic.LANTERN, Color.BROWN), 10,
                             (MobTag.PUSHABLE, MobTag.NO_DESPAWN), tuple(), 6),
    MobID.TORCH: MobData("torch", (Graphic.TORCH, Color.YELLOW), 8,
                             (MobTag.PUSHABLE, MobTag.NO_DESPAWN), tuple(), 3),
    MobID.IRON_LANTERN: MobData("iron lantern", (Graphic.LANTERN, Color.IRON), 10,
                                (MobTag.PUSHABLE, MobTag.NO_DESPAWN), tuple(), 10),
    MobID.GOLD_LANTERN: MobData("gold lantern", (Graphic.LANTERN, Color.GOLD), 10,
                                (MobTag.PUSHABLE, MobTag.NO_DESPAWN), tuple(), 14),
    MobID.GEM_LANTERN: MobData("gem lantern", (Graphic.LANTERN, Color.GEM), 10,
                                (MobTag.PUSHABLE, MobTag.NO_DESPAWN), tuple(), 18),
    MobID.BED: MobData("bed", (Graphic.BED, Color.RED), 10,
                               (MobTag.PUSHABLE, MobTag.NO_DESPAWN, MobTag.BED), tuple(),),
}


class Mob:
    def __init__(self, mobid: MobID):
        self.id = mobid
        self.mob_data = mob_data[self.id]
        self.name = self.mob_data.name
        self.graphic = self.mob_data.graphic
        self.max_health = self.mob_data.max_health
        self.health = self.max_health
        self.tags = self.mob_data.tags
        self.recipies = self.mob_data.recipies
        self.light = self.mob_data.light
        self.target_space = None
        self.last_dir = Point(0, -1)  # assume the last direction was up
        self.state = 'wander'
        self.ai_tick = 0
        self.ai_timer = mob_ai_timer[self.id]

    def has_tag(self, tag: MobTag) -> bool:
        return tag in self.tags
