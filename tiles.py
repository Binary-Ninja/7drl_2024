from collections import namedtuple, defaultdict

from data import Color, Graphic, TileID, TileTag


tile_replace: dict[TileID, TileID] = {
    TileID.GRASS: TileID.DIRT,
    TileID.SAND: TileID.DIRT,
    TileID.ASH: TileID.DIRT,
    TileID.STONE: TileID.DIRT,
    TileID.TREE: TileID.GRASS,
    TileID.CACTUS: TileID.SAND,
    TileID.DIRT: TileID.HOLE,
    TileID.WHEAT: TileID.FARMLAND,
    TileID.PALM_TREE: TileID.SAND,
    TileID.IRON_ORE: TileID.DIRT,
    TileID.GOLD_ORE: TileID.DIRT,
    TileID.GEM_ORE: TileID.DIRT,
    TileID.DESERT_BONES: TileID.SAND,
    TileID.WINDOW: TileID.DIRT,
    TileID.WOOD_WALL: TileID.DIRT,
    TileID.STONE_WALL: TileID.DIRT,
    TileID.OPEN_WOOD_DOOR: TileID.DIRT,
    TileID.CLOSED_WOOD_DOOR: TileID.DIRT,
    TileID.TREE_SAPLING: TileID.GRASS,
    TileID.PALM_TREE_SAPLING: TileID.SAND,
    TileID.CACTUS_SAPLING: TileID.SAND,
    TileID.OBSIDIAN_BRICKS: TileID.DIRT,
    TileID.CLOUD: TileID.AIR,
    TileID.CLOUD_BANK: TileID.CLOUD,
    TileID.WHEAT_SEEDS: TileID.DIRT,
    TileID.WEB: TileID.DIRT,
    TileID.LAPIS_ORE: TileID.DIRT,
    TileID.THORNS: TileID.DIRT,
    TileID.BIG_MUSHROOM: TileID.FLOOR_FUNGUS,
    TileID.FLOOR_FUNGUS: TileID.DIRT,
    TileID.SHROOM_SAPLING: TileID.FLOOR_FUNGUS,
    TileID.QUARTZ_ORE: TileID.CLOUD,
    TileID.ASH_BONES: TileID.ASH,
    TileID.WOOD_FLOOR: TileID.DIRT,
    TileID.STONE_FLOOR: TileID.DIRT,
    TileID.FARMLAND: TileID.DIRT,
    TileID.TUBER_SEEDS: TileID.DIRT,
    TileID.TUBER_CROP: TileID.FARMLAND,
    TileID.WATER: TileID.HOLE,
    TileID.LAVA: TileID.HOLE,
    TileID.OBSIDIAN: TileID.HOLE,
    TileID.OBSIDIAN_FLOOR: TileID.DIRT,
    TileID.SKY_WEBS: TileID.CLOUD,
}

tile_damage = defaultdict(lambda: 0)
tile_damage.update({
    TileID.CACTUS: 1,
    TileID.CACTUS_SAPLING: 1,
    TileID.LAVA: 5,
    TileID.IRON_ORE: 3,
    TileID.GOLD_ORE: 3,
    TileID.GEM_ORE: 3,
    TileID.LAPIS_ORE: 4,
    TileID.THORNS: 2,
    TileID.QUARTZ_ORE: 5,
})

tile_drain = defaultdict(lambda: 0)
tile_drain.update({
    TileID.WEB: 1,
    TileID.SKY_WEBS: 2,
})

tile_grow = defaultdict(tuple)
tile_grow.update({
    TileID.WHEAT_SEEDS: (TileID.WHEAT, 0.02),
    TileID.TREE_SAPLING: (TileID.TREE, 0.02),
    TileID.PALM_TREE_SAPLING: (TileID.PALM_TREE, 0.02),
    TileID.CACTUS_SAPLING: (TileID.CACTUS, 0.02),
    TileID.SHROOM_SAPLING: (TileID.BIG_MUSHROOM, 0.02),
    TileID.TUBER_SEEDS: (TileID.TUBER_CROP, 0.02),
})

tile_spread = defaultdict(tuple)
tile_spread.update({
    TileID.GRASS: (TileID.DIRT, 0.01),
    TileID.WATER: (TileID.HOLE, 1),
    TileID.LAVA: (TileID.HOLE, 0.25),
})

tile_light = {
    TileID.LAVA: 1,
    TileID.LAPIS_ORE: 1,
    TileID.BIG_MUSHROOM: 1,
    TileID.SHROOM_SAPLING: 1,
}


TileData = namedtuple("TileData",
                      ("name", "graphic", "max_health", "tags"),
                      defaults=(10, tuple(),))
tile_data = {
    None: TileData("void", (Graphic.EMPTY, Color.WHITE),),  # off map edge
    TileID.GRASS: TileData("grass", (Graphic.GRASS, Color.GREEN), 10, (TileTag.SPREAD,)),
    TileID.FLOOR_FUNGUS: TileData("fungus", (Graphic.GRASS2, Color.LIGHT_BLUE), 10,),
    TileID.WOOD_FLOOR: TileData("wd.floor", (Graphic.FLOOR1, Color.FLOOR_BROWN), 10, ),
    TileID.OBSIDIAN_FLOOR: TileData("ob.floor", (Graphic.FLOOR2, Color.DARK_OBSIDIAN), 40, ),
    TileID.STONE_FLOOR: TileData("st.floor", (Graphic.FLOOR2, Color.DARK_GRAY), 10, ),
    TileID.WINDOW: TileData("window", (Graphic.WINDOW, Color.LIGHT_BLUE), 2,
                            (TileTag.BLOCK_MOVE,)),
    TileID.WOOD_WALL: TileData("wd. wall", (Graphic.PLANKS, Color.BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.STONE_WALL: TileData("st. wall", (Graphic.BRICKS, Color.STONE), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.OBSIDIAN_BRICKS: TileData("ob. wall", (Graphic.BRICKS, Color.OBSIDIAN), 40,
                                (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.CLOUD_BANK: TileData("cloudbank", (Graphic.STONE_TILE, Color.WHITE), 20,
                                (TileTag.BLOCK_SIGHT,)),
    TileID.OPEN_WOOD_DOOR: TileData("wd. door", (Graphic.DOOR_OPEN, Color.BROWN), 10,),
    TileID.CLOSED_WOOD_DOOR: TileData("wd. door", (Graphic.DOOR_CLOSED, Color.BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.SAND: TileData("sand", (Graphic.SAND, Color.YELLOW),),
    TileID.ASH: TileData("ash", (Graphic.SAND, Color.MED_GRAY), ),
    TileID.DESERT_BONES: TileData("bones", (Graphic.DESERT_BONES, Color.WHITE), ),
    TileID.ASH_BONES: TileData("bones", (Graphic.DESERT_BONES, Color.WHITE), ),
    TileID.WATER: TileData("water", (Graphic.LIQUID, Color.BLUE), 10, (TileTag.LIQUID, TileTag.SPREAD)),
    TileID.STONE: TileData("stone", (Graphic.STONE_TILE, Color.STONE), 10,
                           (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.TREE: TileData("tree", (Graphic.TREE, Color.GREEN), 10,
                          (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.BIG_MUSHROOM: TileData("shroom", (Graphic.TREE2, Color.LIGHT_BLUE), 10,
                          (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.LIGHT)),
    TileID.CACTUS: TileData("cactus", (Graphic.CACTUS, Color.GREEN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.THORNS: TileData("thorns", (Graphic.THORNS, Color.LIGHT_BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.DAMAGE)),
    TileID.DIRT: TileData("dirt", (Graphic.DIRT, Color.BROWN),),
    TileID.OBSIDIAN: TileData("obsidian", (Graphic.OBSIDIAN, Color.OBSIDIAN), 40),
    TileID.HOLE: TileData("hole", (Graphic.HOLE, Color.DARK_BROWN),),
    TileID.FARMLAND: TileData("farmland", (Graphic.FARMLAND, Color.BROWN), 10, (TileTag.CRUSH,)),
    TileID.LAVA: TileData("lava", (Graphic.LIQUID, Color.ORANGE), 10,
                          (TileTag.DAMAGE, TileTag.LIQUID, TileTag.SPREAD, TileTag.LIGHT),),
    TileID.WHEAT: TileData("wheat", (Graphic.WHEAT, Color.YELLOW), 10,
                           (TileTag.BLOCK_SIGHT,), ),
    TileID.TUBER_CROP: TileData("tubers", (Graphic.CROP2, Color.LIGHT_BLUE), 10,
                           tuple(), ),
    TileID.DOWN_STAIRS: TileData("stairs", (Graphic.DOWN_STAIRS, Color.LIGHT_GRAY), 10,
                                 (TileTag.DOWN_STAIRS,)),
    TileID.UP_STAIRS: TileData("stairs", (Graphic.UP_STAIRS, Color.LIGHT_GRAY), 10,
                               (TileTag.UP_STAIRS,)),
    TileID.PALM_TREE: TileData("palm", (Graphic.PALM_TREE, Color.LIGHT_GREEN), 10,
                               (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.IRON_ORE: TileData("iron ore", (Graphic.ORE, Color.IRON), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.GOLD_ORE: TileData("gold ore", (Graphic.ORE, Color.GOLD), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.GEM_ORE: TileData("gem ore", (Graphic.ORE, Color.GEM), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.LAPIS_ORE: TileData("lapis ore", (Graphic.ORE, Color.BLUE), 30,
                              (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE, TileTag.LIGHT)),
    TileID.QUARTZ_ORE: TileData("quartz ore", (Graphic.ORE, Color.WHITE), 40,
                               (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE,)),
    TileID.WHEAT_SEEDS: TileData("wheat seeds", (Graphic.SEEDS, Color.GREEN), 10,
                             (TileTag.GROW, TileTag.CRUSH)),
    TileID.TUBER_SEEDS: TileData("tuber seeds", (Graphic.SEEDS2, Color.LIGHT_BLUE), 10,
                                 (TileTag.GROW, TileTag.CRUSH)),
    TileID.TREE_SAPLING: TileData("sapling", (Graphic.SMALL_TREE, Color.GREEN), 5,
                                 (TileTag.GROW, TileTag.BLOCK_MOVE)),
    TileID.SHROOM_SAPLING: TileData("sapling", (Graphic.SMALL_TREE, Color.LIGHT_BLUE), 5,
                                  (TileTag.GROW, TileTag.BLOCK_MOVE, TileTag.LIGHT)),
    TileID.PALM_TREE_SAPLING: TileData("sapling", (Graphic.SMALL_TREE,
                                                        Color.LIGHT_GREEN), 5,
                                 (TileTag.GROW, TileTag.BLOCK_MOVE)),
    TileID.CACTUS_SAPLING: TileData("cactus", (Graphic.SMALL_CACTUS, Color.GREEN), 5,
                                 (TileTag.GROW, TileTag.DAMAGE, TileTag.BLOCK_MOVE)),
    TileID.AIR: TileData("air", (Graphic.AIR, Color.LIGHT_BLUE), 5,
                                    (TileTag.BLOCK_MOVE,)),
    TileID.CLOUD: TileData("cloud", (Graphic.CLOUD, Color.WHITE), 10, ),
    TileID.WEB: TileData("web", (Graphic.WEB, Color.WHITE), 10, (TileTag.DRAIN,)),
    TileID.SKY_WEBS: TileData("web", (Graphic.WEB, Color.WHITE), 10, (TileTag.DRAIN,)),
}


class Tile:
    def __init__(self, tileid: TileID):
        self.id = tileid
        self.tile_data = tile_data[self.id]
        self.name = self.tile_data.name
        self.graphic = self.tile_data.graphic
        self.max_health = self.tile_data.max_health
        self.health = self.max_health
        self.tags = self.tile_data.tags

    def has_tag(self, tag: TileTag) -> bool:
        return tag in self.tags
