from collections import namedtuple, defaultdict

from data import Color, Graphic, MobID, ItemID, ItemTag, TileID

item_to_mob = defaultdict(lambda: None)
item_to_mob.update({
    MobID.WORKBENCH: ItemID.WORKBENCH,
    MobID.OVEN: ItemID.OVEN,
    MobID.FURNACE: ItemID.FURNACE,
    MobID.ANVIL: ItemID.ANVIL,
    MobID.WOOD_LANTERN: ItemID.WOOD_LANTERN,
    MobID.IRON_LANTERN: ItemID.IRON_LANTERN,
    MobID.GOLD_LANTERN: ItemID.GOLD_LANTERN,
    MobID.GEM_LANTERN: ItemID.GEM_LANTERN,
    MobID.TORCH: ItemID.TORCH,
    MobID.BED: ItemID.BED,
    MobID.BOMB: ItemID.BOMB,
    MobID.RED_BOMB: ItemID.RED_BOMB,
    MobID.WHITE_BOMB: ItemID.WHITE_BOMB,
})

item_light = defaultdict(lambda: 0)
item_light.update({
    ItemID.TORCH: 3,
    ItemID.WOOD_LANTERN: 6,
    ItemID.IRON_LANTERN: 10,
    ItemID.GOLD_LANTERN: 14,
    ItemID.GEM_LANTERN: 18,
    ItemID.LAPIS: 3,
})

ItemData = namedtuple("ItemData", ("name", "graphic", "tags", "data"),
                      defaults=(tuple(), tuple()))
item_data = {
    ItemID.WORKBENCH: ItemData("workbench", (Graphic.WORKBENCH, Color.BROWN),
                               (ItemTag.SPAWN_MOB,), {
            "mobid": MobID.WORKBENCH,
                               }),
    ItemID.CAULDRON: ItemData("cauldron", (Graphic.CAULDRON, Color.MED_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.CAULDRON,
                               }),
    ItemID.BOMB: ItemData("bomb", (Graphic.BOMB, Color.MED_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.BOMB,
                               }),
    ItemID.RED_BOMB: ItemData("megabomb", (Graphic.BOMB, Color.RED),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.RED_BOMB,
                               }),
    ItemID.WHITE_BOMB: ItemData("nuke", (Graphic.BOMB, Color.WHITE),
                              (ItemTag.SPAWN_MOB,), {
                                  "mobid": MobID.WHITE_BOMB,
                              }),
    ItemID.LOOM: ItemData("loom", (Graphic.LOOM, Color.LIGHT_BROWN),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.LOOM,
                               }),
    ItemID.SPAWN_EGG_GREEN_ZOMBIE: ItemData("spawn egg", (Graphic.EGG, Color.MOB_GREEN),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.SPRITE,
                               }),
    ItemID.DUCK_EGG: ItemData("spawn egg", (Graphic.EGG, Color.LIGHT_BROWN),
                                            (ItemTag.SPAWN_MOB,), {
                                                "mobid": MobID.DUCK,
                                            }),
    ItemID.CHICKEN_EGG: ItemData("spawn egg", (Graphic.EGG, Color.LIGHT_BROWN),
                              (ItemTag.SPAWN_MOB,), {
                                  "mobid": MobID.CHICKEN,
                              }),
    ItemID.DOG_EGG: ItemData("spawn egg", (Graphic.EGG, Color.LIGHT_BROWN),
                              (ItemTag.SPAWN_MOB,), {
                                  "mobid": MobID.DOG,
                              }),
    ItemID.CAT_EGG: ItemData("spawn egg", (Graphic.EGG, Color.LIGHT_BROWN),
                              (ItemTag.SPAWN_MOB,), {
                                  "mobid": MobID.CAT,
                              }),
    ItemID.PIG_EGG: ItemData("spawn egg", (Graphic.EGG, Color.LIGHT_BROWN),
                              (ItemTag.SPAWN_MOB,), {
                                  "mobid": MobID.PIG,
                              }),
    ItemID.DIRT: ItemData("dirt", (Graphic.DIRT, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.DIRT, "base": (TileID.HOLE, TileID.WATER, TileID.LAVA)
                          }),
    ItemID.OBSIDIAN: ItemData("obsidian", (Graphic.OBSIDIAN, Color.OBSIDIAN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.OBSIDIAN, "base": (TileID.HOLE,)
                          }),
    ItemID.WATER_BUCKET: ItemData("water bucket", (Graphic.BUCKET, Color.BLUE),
                          (ItemTag.PLACE_TILE,), {
                              "place": TileID.WATER, "base": (TileID.HOLE,), "stamina_cost": 3,
                          }),
    ItemID.LAVA_BUCKET: ItemData("lava bucket", (Graphic.BUCKET, Color.ORANGE),
                          (ItemTag.PLACE_TILE,), {
                              "place": TileID.LAVA, "base": (TileID.HOLE,), "stamina_cost": 3,
                          }),
    ItemID.FUNGUS: ItemData("fungus", (Graphic.GRASS2, Color.LIGHT_BLUE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.FLOOR_FUNGUS, "base": (TileID.DIRT, )
                          }),
    ItemID.WINDOW: ItemData("window", (Graphic.WINDOW, Color.LIGHT_BLUE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.WINDOW, "base": (TileID.DIRT, TileID.SAND,
                                                               TileID.GRASS,
                                                               TileID.ASH, TileID.FLOOR_FUNGUS,
                                                               )
                          }),
    ItemID.OBSIDIAN_FLOOR: ItemData("ob.floor", (Graphic.FLOOR3, Color.DARK_OBSIDIAN),
                            (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                "place": TileID.OBSIDIAN_FLOOR, "base": (TileID.DIRT, TileID.SAND,
                                                                 TileID.GRASS,
                                                                 TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                 )
                            }),
    ItemID.OBSIDIAN_WALL: ItemData("ob. wall", (Graphic.BRICKS, Color.OBSIDIAN),
                            (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                "place": TileID.OBSIDIAN_BRICKS, "base": (TileID.DIRT, TileID.SAND,
                                                                 TileID.GRASS,
                                                                 TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                 )
                            }),
    ItemID.WOOD_WALL: ItemData("wd. wall", (Graphic.PLANKS, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.WOOD_WALL, "base": (TileID.DIRT, TileID.GRASS,
                                                                  TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                  TileID.SAND)
                          }),
    ItemID.WOOD_FLOOR: ItemData("wd.floor", (Graphic.FLOOR1, Color.FLOOR_BROWN),
                               (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                   "place": TileID.WOOD_FLOOR, "base": (TileID.DIRT, TileID.GRASS,
                                                                       TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                       TileID.SAND)
                               }),
    ItemID.STONE_FLOOR: ItemData("st.floor", (Graphic.FLOOR2, Color.DARK_GRAY),
                               (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                   "place": TileID.STONE_FLOOR, "base": (TileID.DIRT, TileID.GRASS,
                                                                       TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                       TileID.SAND)
                               }),
    ItemID.STONE_WALL: ItemData("st. wall", (Graphic.BRICKS, Color.STONE),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.STONE_WALL, "base": (TileID.DIRT, TileID.GRASS,
                                                                   TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                   TileID.SAND)
                          }),
    ItemID.WOOD_DOOR: ItemData("wd. door", (Graphic.DOOR_CLOSED, Color.BROWN),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.CLOSED_WOOD_DOOR, "base": (TileID.DIRT,
                                                                         TileID.ASH, TileID.FLOOR_FUNGUS,
                                                                    TileID.GRASS,
                                                                    TileID.SAND)
                          }),
    ItemID.STONE: ItemData("stone", (Graphic.STONE_ITEM, Color.STONE),
                           (ItemTag.STACKABLE,), ),
    ItemID.CIRCUIT: ItemData("circuit", (Graphic.ALIEN_TECH, Color.GREEN),
                           (ItemTag.STACKABLE,), ),
    ItemID.SPACESHIP: ItemData("spaceship", (Graphic.UFO2, Color.LIGHT_GREEN),
                             tuple(), ),
    ItemID.FAIRY_DUST: ItemData("pixiedust", (Graphic.FULL_BOTTLE, Color.PINK),
                           (ItemTag.STACKABLE,), ),
    ItemID.STRING: ItemData("string", (Graphic.STRING, Color.WHITE),
                           (ItemTag.STACKABLE,), ),
    ItemID.SAND: ItemData("sand", (Graphic.SAND, Color.YELLOW),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
            "place": TileID.SAND, "base": (TileID.DIRT,)
                          }),
    ItemID.ASH: ItemData("ash", (Graphic.SAND, Color.MED_GRAY),
                          (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                              "place": TileID.ASH, "base": (TileID.DIRT,)
                          }),
    ItemID.WOOD: ItemData("wood", (Graphic.WOOD, Color.BROWN), (ItemTag.STACKABLE,), ),
    ItemID.BONE: ItemData("bone", (Graphic.BONE, Color.WHITE), (ItemTag.STACKABLE,), ),
    ItemID.PICKUP: ItemData("pickup", (Graphic.PICKUP, Color.BROWN), (ItemTag.PICKUP,)),
    ItemID.APPLE: ItemData("apple", (Graphic.APPLE, Color.RED),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
            "heal": 1,
                               "stamina_cost": 1,
                           }),
    ItemID.BOILED_EGG: ItemData("boiled egg", (Graphic.EGG, Color.WHITE),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 5,
                               "stamina_cost": 1,
                           }),
    ItemID.TUBER: ItemData("tuber", (Graphic.CARROT, Color.LIGHT_BLUE),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": -1,
                               "stamina_cost": 0,
                           }),
    ItemID.COOKED_TUBER: ItemData("tubemeat", (Graphic.CARROT, Color.BLUE),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 4,
                               "stamina_cost": 2,
                           }),
    ItemID.DUCK_MEAT: ItemData("pet meat", (Graphic.MEAT2, Color.LIGHT_BROWN),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": -3,
                               "stamina_cost": 0,
                           }),
    ItemID.PASTRY: ItemData("pastry", (Graphic.PIE, Color.LIGHT_BLUE),
                                  (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                                      "heal": 5,
                                      "stamina_cost": 0,
            "stamina": 2,
                                  }),
    ItemID.COOKED_DUCK_MEAT: ItemData("pet steak", (Graphic.MEAT2, Color.BROWN),
                            (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                                "heal": 6,
                                "stamina_cost": 0,
                                "stamina": 3,
                            }),
    ItemID.SPIDER_EYE: ItemData("eye", (Graphic.EYE, Color.RED),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": -3,
                               "stamina_cost": 1,
                           }),
    ItemID.FISH: ItemData("fish", (Graphic.FISH, Color.LIGHT_BLUE),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 2,
                               "stamina_cost": 4,
                           }),
    ItemID.DEEP_FISH: ItemData("blobfish", (Graphic.FISH, Color.LIGHT_GRAY),
                           (ItemTag.STACKABLE, ItemTag.HEAL), {
                               "heal": 2,
                               "stamina_cost": 2,
                           }),
    ItemID.FIRE_FISH: ItemData("firefish", (Graphic.FISH, Color.ORANGE),
                           (ItemTag.STACKABLE, ItemTag.STAMINA, ItemTag.HEAL), {
                               "heal": -2,
                               "stamina_cost": 0,
            "stamina": 8,
                           }),
    ItemID.COOKED_FISH: ItemData("fish meat", (Graphic.MEAT, Color.LIGHT_BLUE),
                          (ItemTag.STACKABLE, ItemTag.HEAL), {
                              "heal": 3,
                              "stamina_cost": 1,
                          }),
    ItemID.COOKED_DEEP_FISH: ItemData("bfish meat", (Graphic.MEAT, Color.LIGHT_GRAY),
                               (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                                   "heal": 1,
                                   "stamina_cost": 0, "stamina": 1,
                               }),
    ItemID.WHEAT_SEEDS: ItemData("wh. seeds", (Graphic.SEEDS, Color.GREEN),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE),{
            "place": TileID.WHEAT_SEEDS, "base": (TileID.FARMLAND,),
                                 }),
    ItemID.TUBER_SEEDS: ItemData("tb. seeds", (Graphic.SEEDS2, Color.LIGHT_BLUE),
                                 (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                     "place": TileID.TUBER_SEEDS, "base": (TileID.FARMLAND,),
                                 }),
    ItemID.FISH_SPEAR: ItemData("fishspear", (Graphic.FISHING_SPEAR, Color.BROWN),
                               (ItemTag.FISH,), {
                                   "fishable": (TileID.WATER, ),
                                   "stamina_cost": 4,
            "fish_chance": 0.1,
                               }),
    ItemID.IRON_FISH_SPEAR: ItemData("i.fishspear", (Graphic.FISHING_SPEAR, Color.IRON),
                               (ItemTag.FISH,), {
                                   "fishable": (TileID.WATER, TileID.LAVA),
                                   "stamina_cost": 3,
                                   "fish_chance": 0.15,
                               }),
    ItemID.GOLD_FISH_SPEAR: ItemData("g.fishspear", (Graphic.FISHING_SPEAR, Color.GOLD),
                                     (ItemTag.FISH,), {
                                         "fishable": (TileID.WATER, TileID.LAVA),
                                         "stamina_cost": 2,
                                         "fish_chance": 0.2,
                                     }),
    ItemID.GEM_FISH_SPEAR: ItemData("gm.fishspear", (Graphic.FISHING_SPEAR, Color.GEM),
                                     (ItemTag.FISH,), {
                                         "fishable": (TileID.WATER, TileID.LAVA),
                                         "stamina_cost": 1,
                                         "fish_chance": 0.25,
                                     }),
    ItemID.WOOD_PICK: ItemData("wood pick", (Graphic.PICKAXE, Color.BROWN),
                               (ItemTag.BREAK_TILE,), {
            "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.CLOUD_BANK, TileID.STONE_FLOOR),
                                   "tile_damage": 2,
                                   "stamina_cost": 5,
                               }),
    ItemID.WOOD_SWORD: ItemData("wood sword", (Graphic.SWORD, Color.BROWN),
                                (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE), {
            "mob_damage": 2,
                                    "stamina_cost": 5,
                                    "breakable": (TileID.WEB,), "tile_damage": 2,
                                }),
    ItemID.EMPTY_HANDS: ItemData("empty hands", (Graphic.EMPTY_HANDS, Color.YELLOW),
                                 (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE, ItemTag.PICKUP), {
            "mob_damage": 1, "breakable": (TileID.TREE, TileID.CACTUS, TileID.PALM_TREE,
                                           TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                           TileID.SHROOM_SAPLING, TileID.WINDOW,
                                           ),
                                     "tile_damage": 1,
                                     "stamina_cost": 2,
                                 }),
    ItemID.WOOD_AXE: ItemData("wood axe", (Graphic.AXE, Color.BROWN),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW, TileID.THORNS,
                                                 TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                                 TileID.SHROOM_SAPLING, TileID.WOOD_FLOOR,
                                                 ),
                                   "tile_damage": 2,
                                  "stamina_cost": 5,
                               }),
    ItemID.BUCKET: ItemData("bucket", (Graphic.BUCKET, Color.IRON),
                              (ItemTag.BREAK_TILE,), {
                                  "breakable": (TileID.WATER, TileID.LAVA,
                                                ),
                                  "tile_damage": 10,
                                  "stamina_cost": 3,
                              }),
    ItemID.WOOD_HOE: ItemData("wood hoe", (Graphic.HOE, Color.BROWN),
                              (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
            "breakable": (TileID.WHEAT, TileID.TUBER_CROP), "tile_damage": 10,
                                  "stamina_cost": 5,
                               }),
    ItemID.WOOD_SHOVEL: ItemData("wood shovel", (Graphic.SHOVEL, Color.BROWN),
                                 (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.DIRT, TileID.SAND,
                                                 TileID.GRASS, TileID.FARMLAND,
                                                 TileID.DESERT_BONES, TileID.CLOUD, TileID.FLOOR_FUNGUS,
                                                 TileID.ASH, TileID.ASH_BONES,
                                                 ),
                                   "tile_damage": 10,
            "stamina_cost": 5,
                               }),
    ItemID.WHEAT: ItemData("wheat", (Graphic.WHEAT, Color.YELLOW),
                           (ItemTag.STACKABLE,), ),
    ItemID.IRON_ORE: ItemData("i. ore", (Graphic.STONE_ITEM, Color.IRON),
                              (ItemTag.STACKABLE,), ),
    ItemID.LAPIS: ItemData("lapis", (Graphic.STONE_ITEM, Color.BLUE),
                              (ItemTag.STACKABLE, ItemTag.LIGHT), ),
    ItemID.QUARTZ: ItemData("quartz", (Graphic.CRYSTAL, Color.WHITE),
                           (ItemTag.STACKABLE,), ),
    ItemID.GOLD_ORE: ItemData("g. ore", (Graphic.STONE_ITEM, Color.GOLD),
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
    ItemID.IRON_BAR: ItemData("i. bar", (Graphic.INGOT, Color.IRON),
                           (ItemTag.STACKABLE,), ),
    ItemID.GOLD_BAR: ItemData("g. bar", (Graphic.INGOT, Color.GOLD),
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
    ItemID.FURNACE: ItemData("furnace", (Graphic.FURNACE, Color.MED_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.FURNACE,
                               }),
    ItemID.ANVIL: ItemData("anvil", (Graphic.ANVIL, Color.LIGHT_GRAY),
                               (ItemTag.SPAWN_MOB,), {
                                   "mobid": MobID.ANVIL,
                               }),
    ItemID.WOOD_LANTERN: ItemData("wood lantern", (Graphic.LANTERN, Color.BROWN),
                               (ItemTag.SPAWN_MOB, ItemTag.LIGHT), {
                                   "mobid": MobID.WOOD_LANTERN,
                               }),
    ItemID.IRON_LANTERN: ItemData("iron lantern", (Graphic.LANTERN, Color.IRON),
                                  (ItemTag.SPAWN_MOB, ItemTag.LIGHT), {
                                      "mobid": MobID.IRON_LANTERN,
                                  }),
    ItemID.GOLD_LANTERN: ItemData("gold lantern", (Graphic.LANTERN, Color.GOLD),
                                  (ItemTag.SPAWN_MOB, ItemTag.LIGHT), {
                                      "mobid": MobID.GOLD_LANTERN,
                                  }),
    ItemID.GEM_LANTERN: ItemData("gem lantern", (Graphic.LANTERN, Color.GEM),
                                  (ItemTag.SPAWN_MOB, ItemTag.LIGHT), {
                                      "mobid": MobID.GEM_LANTERN,
                                  }),
    ItemID.BED: ItemData("bed", (Graphic.BED, Color.RED),
                                 (ItemTag.SPAWN_MOB,), {
                                     "mobid": MobID.BED,
                                 }),
    ItemID.TORCH: ItemData("torch", (Graphic.TORCH_ITEM, Color.YELLOW),
                               (ItemTag.SPAWN_MOB, ItemTag.STACKABLE, ItemTag.LIGHT), {
                                   "mobid": MobID.TORCH,
                               }),
    ItemID.GOLD_APPLE: ItemData("gold apple", (Graphic.APPLE, Color.GOLD),
                           (ItemTag.STACKABLE, ItemTag.HEAL, ItemTag.STAMINA), {
                               "heal": 10,
                               "stamina_cost": 0,
            "stamina": 10,
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
    ItemID.SHROOM_SAPLING: ItemData("sapling", (Graphic.SMALL_TREE, Color.LIGHT_BLUE),
                                  (ItemTag.STACKABLE, ItemTag.PLACE_TILE), {
                                      "place": TileID.SHROOM_SAPLING, "base": (TileID.FLOOR_FUNGUS,),
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
                                (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE), {
                                    "mob_damage": 3,
                                    "stamina_cost": 4,
                                     "breakable": (TileID.WEB,), "tile_damage": 3,
                                }),
    ItemID.STONE_PICK: ItemData("stone pick", (Graphic.PICKAXE, Color.STONE),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                 TileID.CLOUD_BANK, TileID.STONE_FLOOR),
                                    "tile_damage": 3,
                                   "stamina_cost": 4,
                               }),
    ItemID.STONE_AXE: ItemData("stone axe", (Graphic.AXE, Color.STONE),
                              (ItemTag.BREAK_TILE,), {
                                  "breakable": (TileID.TREE, TileID.CACTUS,
                                                TileID.PALM_TREE, TileID.WOOD_WALL,
                                                TileID.OPEN_WOOD_DOOR,
                                                TileID.CLOSED_WOOD_DOOR,
                                                TileID.WINDOW, TileID.THORNS,
                                                TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                                TileID.SHROOM_SAPLING, TileID.WOOD_FLOOR,
                                                ),
                                  "tile_damage": 3,
                                  "stamina_cost": 4,
                              }),
    ItemID.STONE_SHOVEL: ItemData("stone shovel", (Graphic.SHOVEL, Color.STONE),
                                 (ItemTag.BREAK_TILE,), {
                                     "breakable": (TileID.DIRT, TileID.SAND,
                                                   TileID.GRASS, TileID.FARMLAND,
                                                   TileID.DESERT_BONES, TileID.CLOUD, TileID.FLOOR_FUNGUS,
                                                   TileID.ASH, TileID.ASH_BONES,
                                                   ),
                                     "tile_damage": 10,
                                     "stamina_cost": 4,
                                 }),
    ItemID.STONE_HOE: ItemData("stone hoe", (Graphic.HOE, Color.STONE),
                              (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                  "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                  "breakable": (TileID.WHEAT, TileID.TUBER_CROP), "tile_damage": 10,
                                  "stamina_cost": 4,
                              }),
    ItemID.IRON_SWORD: ItemData("iron sword", (Graphic.SWORD, Color.IRON),
                                 (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE), {
                                     "mob_damage": 4,
                                     "stamina_cost": 3,
                                    "breakable": (TileID.WEB,), "tile_damage": 4,
                                 }),
    ItemID.IRON_PICK: ItemData("iron pick", (Graphic.PICKAXE, Color.IRON),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.CLOUD_BANK, TileID.STONE_FLOOR),
                                    "tile_damage": 4,
                                    "stamina_cost": 3,
                                }),
    ItemID.IRON_AXE: ItemData("iron axe", (Graphic.AXE, Color.IRON),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW, TileID.THORNS,
                                                 TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                                 TileID.SHROOM_SAPLING, TileID.WOOD_FLOOR,
                                                 ),
                                   "tile_damage": 4,
                                   "stamina_cost": 3,
                               }),
    ItemID.IRON_SHOVEL: ItemData("iron shovel", (Graphic.SHOVEL, Color.IRON),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD, TileID.FLOOR_FUNGUS,
                                                    TileID.ASH, TileID.ASH_BONES,
                                                    ),
                                      "tile_damage": 10,
                                      "stamina_cost": 3,
                                  }),
    ItemID.IRON_HOE: ItemData("iron hoe", (Graphic.HOE, Color.IRON),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT, TileID.TUBER_CROP), "tile_damage": 10,
                                   "stamina_cost": 3,
                               }),
    ItemID.GOLD_SWORD: ItemData("gold sword", (Graphic.SWORD, Color.GOLD),
                                 (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE), {
                                     "mob_damage": 5,
                                     "stamina_cost": 2,
                                    "breakable": (TileID.WEB,), "tile_damage": 5,
                                 }),
    ItemID.GOLD_PICK: ItemData("gold pick", (Graphic.PICKAXE, Color.GOLD),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.GEM_ORE, TileID.CLOUD_BANK,
                                                  TileID.LAPIS_ORE, TileID.STONE_FLOOR),
                                    "tile_damage": 5,
                                    "stamina_cost": 2,
                                }),
    ItemID.GOLD_AXE: ItemData("gold axe", (Graphic.AXE, Color.GOLD),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW, TileID.THORNS,
                                                 TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                                 TileID.SHROOM_SAPLING, TileID.WOOD_FLOOR,
                                                 ),
                                   "tile_damage": 5,
                                   "stamina_cost": 2,
                               }),
    ItemID.GOLD_SHOVEL: ItemData("gold shovel", (Graphic.SHOVEL, Color.GOLD),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD, TileID.FLOOR_FUNGUS,
                                                    TileID.ASH, TileID.ASH_BONES,
                                                    ),
                                      "tile_damage": 10,
                                      "stamina_cost": 2,
                                  }),
    ItemID.GOLD_HOE: ItemData("gold hoe", (Graphic.HOE, Color.GOLD),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT, TileID.TUBER_CROP), "tile_damage": 10,
                                   "stamina_cost": 2,
                               }),
    ItemID.GEM_SWORD: ItemData("gem sword", (Graphic.SWORD, Color.GEM),
                                 (ItemTag.DAMAGE_MOBS, ItemTag.BREAK_TILE), {
                                     "mob_damage": 10,
                                     "stamina_cost": 1,
            "breakable": (TileID.WEB,), "tile_damage": 10,
                                 }),
    ItemID.GEM_PICK: ItemData("gem pick", (Graphic.PICKAXE, Color.GEM),
                                (ItemTag.BREAK_TILE,), {
                                    "breakable": (TileID.STONE, TileID.STONE_WALL, TileID.WINDOW, TileID.IRON_ORE,
                                                  TileID.GOLD_ORE, TileID.GEM_ORE, TileID.OBSIDIAN_BRICKS,
                                                  TileID.CLOUD_BANK, TileID.LAPIS_ORE, TileID.QUARTZ_ORE,
                                                  TileID.STONE_FLOOR, TileID.OBSIDIAN_FLOOR, TileID.OBSIDIAN,
                                                  ),
                                    "tile_damage": 10,
                                    "stamina_cost": 1,
                                }),
    ItemID.GEM_AXE: ItemData("gem axe", (Graphic.AXE, Color.GEM),
                               (ItemTag.BREAK_TILE,), {
                                   "breakable": (TileID.TREE, TileID.CACTUS,
                                                 TileID.PALM_TREE, TileID.WOOD_WALL,
                                                 TileID.OPEN_WOOD_DOOR,
                                                 TileID.CLOSED_WOOD_DOOR,
                                                 TileID.WINDOW, TileID.THORNS,
                                                 TileID.TREE_SAPLING, TileID.PALM_TREE_SAPLING, TileID.CACTUS_SAPLING,
                                                 TileID.SHROOM_SAPLING, TileID.WOOD_FLOOR,
                                                 ),
                                   "tile_damage": 10,
                                   "stamina_cost": 1,
                               }),
    ItemID.GEM_SHOVEL: ItemData("gem shovel", (Graphic.SHOVEL, Color.GEM),
                                  (ItemTag.BREAK_TILE,), {
                                      "breakable": (TileID.DIRT, TileID.SAND,
                                                    TileID.GRASS, TileID.FARMLAND,
                                                    TileID.DESERT_BONES, TileID.CLOUD, TileID.FLOOR_FUNGUS,
                                                    TileID.ASH, TileID.ASH_BONES,
                                                    ),
                                      "tile_damage": 10,
                                      "stamina_cost": 1,
                                  }),
    ItemID.GEM_HOE: ItemData("gem hoe", (Graphic.HOE, Color.GEM),
                               (ItemTag.PLACE_TILE, ItemTag.BREAK_TILE), {
                                   "place": TileID.FARMLAND, "base": (TileID.DIRT,),
                                   "breakable": (TileID.WHEAT, TileID.TUBER_CROP), "tile_damage": 10,
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
