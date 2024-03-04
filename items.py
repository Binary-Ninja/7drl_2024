from collections import namedtuple, defaultdict

from data import Color, Graphic, MobID, ItemID, ItemTag, TileID

item_to_mob = defaultdict(lambda: None)
item_to_mob.update({
    MobID.WORKBENCH: ItemID.WORKBENCH,
    MobID.OVEN: ItemID.OVEN,
    MobID.FURNACE: ItemID.FURNACE,
    MobID.ANVIL: ItemID.ANVIL,
    MobID.WOOD_LANTERN: ItemID.WOOD_LANTERN,
    MobID.TORCH: ItemID.TORCH,
})

ItemData = namedtuple("ItemData", ("name", "graphic", "tags", "data"),
                      defaults=(tuple(), tuple()))
item_data = {
    ItemID.WORKBENCH: ItemData("workbench", (Graphic.WORKBENCH, Color.BROWN),
                               (ItemTag.SPAWN_MOB,), {
            "mobid": MobID.WORKBENCH,
                               }),
    ItemID.DIRT: ItemData("dirt", (Graphic.DIRT, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.DIRT, "base": (TileID.HOLE, TileID.WATER)
                          }),
    ItemID.WINDOW: ItemData("window", (Graphic.WINDOW, Color.LIGHT_BLUE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.WINDOW, "base": (TileID.DIRT, TileID.SAND,
                                                               TileID.GRASS)
                          }),
    ItemID.WOOD_WALL: ItemData("wood wall", (Graphic.PLANKS, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.WOOD_WALL, "base": (TileID.DIRT, TileID.GRASS,
                                                                  TileID.SAND)
                          }),
    ItemID.STONE_WALL: ItemData("stone wall", (Graphic.BRICKS, Color.STONE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.STONE_WALL, "base": (TileID.DIRT, TileID.GRASS,
                                                                   TileID.SAND)
                          }),
    ItemID.WOOD_DOOR: ItemData("wood door", (Graphic.DOOR_CLOSED, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.CLOSED_WOOD_DOOR, "base": (TileID.DIRT,
                                                                    TileID.GRASS,
                                                                    TileID.SAND)
                          }),
    ItemID.STONE: ItemData("stone", (Graphic.STONE_ITEM, Color.STONE),
                           (ItemTag.STACKABLE,), ),
    ItemID.SAND: ItemData("sand", (Graphic.SAND, Color.YELLOW),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
            "place": TileID.SAND, "base": (TileID.DIRT,)
                          }),
    ItemID.WOOD: ItemData("wood", (Graphic.WOOD, Color.BROWN), (ItemTag.STACKABLE,), ),
    ItemID.BONE: ItemData("bone", (Graphic.BONE, Color.WHITE), (ItemTag.STACKABLE,), ),
    ItemID.PICKUP: ItemData("pickup", (Graphic.PICKUP, Color.BROWN), (ItemTag.PICKUP,)),
    ItemID.APPLE: ItemData("apple", (Graphic.APPLE, Color.RED),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
            "heal": 1,
                               "stamina_cost": 1,
                           }),
    ItemID.WHEAT_SEEDS: ItemData("wheat seeds", (Graphic.SEEDS, Color.GREEN),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE),{
            "place": TileID.WHEAT_SEEDS, "base": (TileID.FARMLAND,),
                                 }),
    ItemID.WOOD_PICK: ItemData("wood pick", (Graphic.PICKAXE, Color.BROWN),
                               (ItemTag.BREAK_TILE,), {
            "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.CLOUD_BANK), "tile_damage": 2,
                                   "stamina_cost": 5,
                               }),
    ItemID.WOOD_SWORD: ItemData("wood sword", (Graphic.SWORD, Color.BROWN),
                                (ItemTag.DAMAGE_MOBS,), {
            "mob_damage": 2,
                                    "stamina_cost": 5,
                                }),
    ItemID.EMPTY_HANDS: ItemData("empty hands", (Graphic.EMPTY_HANDS, Color.YELLOW),
                                 (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE, ItemTag.PICKUP), {
            "mob_damage": 1, "breakable": (TileID.TREE, TileID.CACTUS, TileID.PALM_TREE),
                                     "tile_damage": 1,
                                     "stamina_cost": 1,
                                 }),
    ItemID.WOOD_AXE: ItemData("wood axe", (Graphic.AXE, Color.BROWN),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW),
                                   "tile_damage": 2,
                                  "stamina_cost": 5,
                               }),
    ItemID.WOOD_HOE: ItemData("wood hoe", (Graphic.HOE, Color.BROWN),
                              (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
            "breakable": (TileID.WHEAT,), "tile_damage": 10,
                                  "stamina_cost": 5,
                               }),
    ItemID.WOOD_SHOVEL: ItemData("wood shovel", (Graphic.SHOVEL, Color.BROWN),
                                 (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.DIRT, TileID.SAND,
                                                 TileID.GRASS, TileID.FARMLAND,
                                                 TileID.DESERT_BONES, TileID.CLOUD),
                                   "tile_damage": 10,
            "stamina_cost": 5,
                               }),
    ItemID.WHEAT: ItemData("wheat", (Graphic.WHEAT, Color.YELLOW),
                           (ItemTag.STACKABLE,), ),
    ItemID.IRON_ORE: ItemData("iron ore", (Graphic.STONE_ITEM, Color.IRON),
                              (ItemTag.STACKABLE,), ),
    ItemID.GOLD_ORE: ItemData("gold ore", (Graphic.STONE_ITEM, Color.GOLD),
                           (ItemTag.STACKABLE,), ),
    ItemID.GEM: ItemData("gem", (Graphic.GEM, Color.GEM),
                         (ItemTag.STACKABLE,), ),
    ItemID.COCONUT: ItemData("coconut", (Graphic.COCONUT, Color.BROWN),
                             (ItemTag.STACKABLE, ItemTag.STAMINA), {
                               "stamina": 3,
                           }),
    ItemID.COAL: ItemData("coal", (Graphic.STONE_ITEM, Color.DARK_GRAY),
                           (ItemTag.STACKABLE,), ),
    ItemID.CLOTH: ItemData("cloth", (Graphic.CLOTH, Color.MOB_GREEN),
                           (ItemTag.STACKABLE,), ),
    ItemID.SLIME: ItemData("slime", (Graphic.SLIME_ITEM, Color.MOB_GREEN),
                           (ItemTag.STACKABLE,), ),
    ItemID.IRON_BAR: ItemData("iron bar", (Graphic.INGOT, Color.IRON),
                           (ItemTag.STACKABLE,), ),
    ItemID.GOLD_BAR: ItemData("gold bar", (Graphic.INGOT, Color.GOLD),
                           (ItemTag.STACKABLE,), ),
    ItemID.GLASS: ItemData("glass", (Graphic.GLASS, Color.WHITE),
                           (ItemTag.STACKABLE,), ),
    ItemID.BREAD: ItemData("bread", (Graphic.BREAD, Color.LIGHT_BROWN),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 3,
                               "stamina_cost": 3,
                           }),
    ItemID.APPLE_PIE: ItemData("pie", (Graphic.PIE, Color.LIGHT_BROWN),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 5,
                               "stamina_cost": 3,
                           }),
    ItemID.OVEN: ItemData("oven", (Graphic.OVEN, Color.LIGHT_BROWN),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.OVEN,
                               }),
    ItemID.FURNACE: ItemData("furnace", (Graphic.FURNACE, Color.LIGHT_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.FURNACE,
                               }),
    ItemID.ANVIL: ItemData("anvil", (Graphic.ANVIL, Color.LIGHT_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.ANVIL,
                               }),
    ItemID.WOOD_LANTERN: ItemData("wood lantern", (Graphic.LANTERN, Color.BROWN),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.WOOD_LANTERN,
                               }),
    ItemID.TORCH: ItemData("torch", (Graphic.TORCH, Color.YELLOW),
                               (ItemTag.SPAWN_MOB, ItemTag.STACKABLE), {
                                   "mobid": MobID.TORCH,
                               }),
    ItemID.GOLD_APPLE: ItemData("gold apple", (Graphic.APPLE, Color.GOLD),
                           (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                               "heal": 5,
                               "stamina_cost": 0,
            "stamina": 5,
                           }),
    ItemID.POKE_PEAR: ItemData("pokepear", (Graphic.PEAR, Color.YELLOW),
                           (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                               "heal": 2,
                               "stamina_cost": 0,
            "stamina": 2,
                           }),
    ItemID.COCKTAIL: ItemData("cocktail", (Graphic.FULL_BOTTLE, Color.ORANGE),
                               (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                                   "heal": 1,
                                   "stamina_cost": 0,
                                   "stamina": 4,
                               }),
    ItemID.TREE_SAPLING: ItemData("sapling", (Graphic.SMALL_TREE, Color.GREEN),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                     "place": TileID.TREE_SAPLING, "base": (TileID.GRASS,),
                                 }),
    ItemID.PALM_TREE_SAPLING: ItemData("sapling", (Graphic.SMALL_TREE,
                                                        Color.LIGHT_GREEN),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                     "place": TileID.PALM_TREE_SAPLING,
                                           "base": (TileID.SAND,),
                                 }),
    ItemID.CACTUS_SAPLING: ItemData("cactus", (Graphic.SMALL_CACTUS, Color.GREEN),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                     "place": TileID.CACTUS_SAPLING, "base": (TileID.SAND,),
                                 }),
    ItemID.BOTTLE: ItemData("bottle", (Graphic.EMPTY_BOTTLE, Color.WHITE),
                           (ItemTag.STACKABLE,), ),
    ItemID.STONE_SWORD: ItemData("stone sword", (Graphic.SWORD, Color.STONE),
                                (ItemTag.DAMAGE_MOBS,), {
                                    "mob_damage": 3,
                                    "stamina_cost": 4,
                                }),
    ItemID.STONE_PICK: ItemData("stone pick", (Graphic.PICKAXE, Color.STONE),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                 TileID.CLOUD_BANK),
                                    "tile_damage": 3,
                                   "stamina_cost": 4,
                               }),
    ItemID.STONE_AXE: ItemData("stone axe", (Graphic.AXE, Color.STONE),
                              (ItemTag.BREAK_TILE,), {
                                  "breakable": (TileID.TREE, TileID.CACTUS,
                                                TileID.PALM_TREE, TileID.WOOD_WALL,
                                                TileID.OPEN_WOOD_DOOR,
                                                TileID.CLOSED_WOOD_DOOR,
                                                TileID.WINDOW),
                                  "tile_damage": 3,
                                  "stamina_cost": 4,
                              }),
    ItemID.STONE_SHOVEL: ItemData("stone shovel", (Graphic.SHOVEL, Color.STONE),
                                 (ItemTag.BREAK_TILE,), {
                                     "breakable": (TileID.DIRT, TileID.SAND,
                                                   TileID.GRASS, TileID.FARMLAND,
                                                   TileID.DESERT_BONES, TileID.CLOUD),
                                     "tile_damage": 10,
                                     "stamina_cost": 4,
                                 }),
    ItemID.STONE_HOE: ItemData("stone hoe", (Graphic.HOE, Color.STONE),
                              (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                  "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                  "breakable": (TileID.WHEAT,), "tile_damage": 10,
                                  "stamina_cost": 4,
                              }),
    ItemID.IRON_SWORD: ItemData("iron sword", (Graphic.SWORD, Color.IRON),
                                 (ItemTag.DAMAGE_MOBS,), {
                                     "mob_damage": 4,
                                     "stamina_cost": 3,
                                 }),
    ItemID.IRON_PICK: ItemData("iron pick", (Graphic.PICKAXE, Color.IRON),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.CLOUD_BANK),
                                    "tile_damage": 4,
                                    "stamina_cost": 3,
                                }),
    ItemID.IRON_AXE: ItemData("iron axe", (Graphic.AXE, Color.IRON),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW),
                                   "tile_damage": 4,
                                   "stamina_cost": 3,
                               }),
    ItemID.IRON_SHOVEL: ItemData("iron shovel", (Graphic.SHOVEL, Color.IRON),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD),
                                      "tile_damage": 10,
                                      "stamina_cost": 3,
                                  }),
    ItemID.IRON_HOE: ItemData("iron hoe", (Graphic.HOE, Color.IRON),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT,), "tile_damage": 10,
                                   "stamina_cost": 3,
                               }),
    ItemID.GOLD_SWORD: ItemData("gold sword", (Graphic.SWORD, Color.GOLD),
                                 (ItemTag.DAMAGE_MOBS,), {
                                     "mob_damage": 5,
                                     "stamina_cost": 2,
                                 }),
    ItemID.GOLD_PICK: ItemData("gold pick", (Graphic.PICKAXE, Color.GOLD),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.GEM_ORE, TileID.CLOUD_BANK),
                                    "tile_damage": 5,
                                    "stamina_cost": 2,
                                }),
    ItemID.GOLD_AXE: ItemData("gold axe", (Graphic.AXE, Color.GOLD),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW),
                                   "tile_damage": 5,
                                   "stamina_cost": 2,
                               }),
    ItemID.GOLD_SHOVEL: ItemData("gold shovel", (Graphic.SHOVEL, Color.GOLD),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD),
                                      "tile_damage": 10,
                                      "stamina_cost": 2,
                                  }),
    ItemID.GOLD_HOE: ItemData("gold hoe", (Graphic.HOE, Color.GOLD),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT,), "tile_damage": 10,
                                   "stamina_cost": 2,
                               }),
    ItemID.GEM_SWORD: ItemData("gem sword", (Graphic.SWORD, Color.GEM),
                                 (ItemTag.DAMAGE_MOBS,), {
                                     "mob_damage": 10,
                                     "stamina_cost": 1,
                                 }),
    ItemID.GEM_PICK: ItemData("gem pick", (Graphic.PICKAXE, Color.GEM),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.GEM_ORE, TileID.OBSIDIAN_BRICKS,
                                                  TileID.CLOUD_BANK),
                                    "tile_damage": 10,
                                    "stamina_cost": 1,
                                }),
    ItemID.GEM_AXE: ItemData("gem axe", (Graphic.AXE, Color.GEM),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW),
                                   "tile_damage": 10,
                                   "stamina_cost": 1,
                               }),
    ItemID.GEM_SHOVEL: ItemData("gem shovel", (Graphic.SHOVEL, Color.GEM),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD),
                                      "tile_damage": 10,
                                      "stamina_cost": 1,
                                  }),
    ItemID.GEM_HOE: ItemData("gem hoe", (Graphic.HOE, Color.GEM),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT,), "tile_damage": 10,
                                   "stamina_cost": 1,
                               }),
    ItemID.CLOUD: ItemData("cloud", (Graphic.CLOUD, Color.WHITE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.CLOUD, "base": (TileID.AIR,)
                          }),
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
