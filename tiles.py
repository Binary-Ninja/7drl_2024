from collections import namedtuple, defaultdict

from data import Color, Graphic, TileID, TileTag


tile_replace: dict[TileID, TileID] = {
    TileID.GRASS: TileID.DIRT,
    TileID.SAND: TileID.DIRT,
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
    TileID.OBSIDIAN_BRICKS: TileID.SAND,
    TileID.CLOUD: TileID.AIR,
    TileID.CLOUD_BANK: TileID.CLOUD,
    TileID.WHEAT_SEEDS: TileID.DIRT,
    TileID.WEB: TileID.DIRT,
    TileID.LAPIS_ORE: TileID.DIRT,
    TileID.THORNS: TileID.DIRT,
}

tile_damage = defaultdict(lambda: 0)
tile_damage.update({
    TileID.CACTUS: 1,
    TileID.CACTUS_SAPLING: 1,
    TileID.LAVA: 5,
    TileID.IRON_ORE: 3,
    TileID.GOLD_ORE: 3,
    TileID.GEM_ORE: 3,
    TileID.LAPIS_ORE: 5,
    TileID.THORNS: 2,
})

tile_drain = defaultdict(lambda: 0)
tile_drain.update({
    TileID.WEB: 1,
})

tile_grow = defaultdict(tuple)
tile_grow.update({
    TileID.WHEAT_SEEDS: (TileID.WHEAT, 0.02),
    TileID.TREE_SAPLING: (TileID.TREE, 0.05),
    TileID.PALM_TREE_SAPLING: (TileID.PALM_TREE, 0.05),
    TileID.CACTUS_SAPLING: (TileID.CACTUS, 0.05),
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
}


TileData = namedtuple("TileData",
                      ("name", "graphic", "max_health", "tags"),
                      defaults=(10, tuple(),))
tile_data = {
    None: TileData("void", (Graphic.EMPTY, Color.WHITE),),  # off map edge
    TileID.GRASS: TileData("grass", (Graphic.GRASS, Color.GREEN), 10, (TileTag.SPREAD,)),
    TileID.WINDOW: TileData("window", (Graphic.WINDOW, Color.LIGHT_BLUE), 2,
                            (TileTag.BLOCK_MOVE,)),
    TileID.WOOD_WALL: TileData("wd. wall", (Graphic.PLANKS, Color.BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.STONE_WALL: TileData("st. wall", (Graphic.BRICKS, Color.STONE), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.OBSIDIAN_BRICKS: TileData("ob. wall", (Graphic.BRICKS, Color.OBSIDIAN), 20,
                                (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.CLOUD_BANK: TileData("cloudbank", (Graphic.STONE_TILE, Color.WHITE), 20,
                                (TileTag.BLOCK_SIGHT,)),
    TileID.OPEN_WOOD_DOOR: TileData("wd. door", (Graphic.DOOR_OPEN, Color.BROWN), 10,),
    TileID.CLOSED_WOOD_DOOR: TileData("wd. door", (Graphic.DOOR_CLOSED, Color.BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.SAND: TileData("sand", (Graphic.SAND, Color.YELLOW),),
    TileID.DESERT_BONES: TileData("bones", (Graphic.DESERT_BONES, Color.WHITE), ),
    TileID.WATER: TileData("water", (Graphic.LIQUID, Color.BLUE), 10, (TileTag.LIQUID, TileTag.SPREAD)),
    TileID.STONE: TileData("stone", (Graphic.STONE_TILE, Color.STONE), 10,
                           (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.TREE: TileData("tree", (Graphic.TREE, Color.GREEN), 10,
                          (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.CACTUS: TileData("cactus", (Graphic.CACTUS, Color.GREEN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.THORNS: TileData("thorns", (Graphic.THORNS, Color.LIGHT_BROWN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.DAMAGE)),
    TileID.DIRT: TileData("dirt", (Graphic.DIRT, Color.BROWN),),
    TileID.HOLE: TileData("hole", (Graphic.HOLE, Color.DARK_BROWN),),
    TileID.FARMLAND: TileData("farmland", (Graphic.FARMLAND, Color.BROWN),),
    TileID.LAVA: TileData("lava", (Graphic.LIQUID, Color.ORANGE), 10,
                          (TileTag.DAMAGE, TileTag.LIQUID, TileTag.SPREAD, TileTag.LIGHT),),
    TileID.WHEAT: TileData("wheat", (Graphic.WHEAT, Color.YELLOW), 10,
                           (TileTag.BLOCK_SIGHT,), ),
    TileID.DOWN_STAIRS: TileData("stairs", (Graphic.DOWN_STAIRS, Color.LIGHT_GRAY),
                                 (TileTag.DOWN_STAIRS,)),
    TileID.UP_STAIRS: TileData("stairs", (Graphic.UP_STAIRS, Color.LIGHT_GRAY),
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
    TileID.WHEAT_SEEDS: TileData("wheat seeds", (Graphic.SEEDS, Color.GREEN), 10,
                             (TileTag.GROW, TileTag.CRUSH)),
    TileID.TREE_SAPLING: TileData("sapling", (Graphic.SMALL_TREE, Color.GREEN), 5,
                                 (TileTag.GROW, TileTag.BLOCK_MOVE)),
    TileID.PALM_TREE_SAPLING: TileData("sapling", (Graphic.SMALL_TREE,
                                                        Color.LIGHT_GREEN), 5,
                                 (TileTag.GROW, TileTag.BLOCK_MOVE)),
    TileID.CACTUS_SAPLING: TileData("cactus", (Graphic.SMALL_CACTUS, Color.GREEN), 5,
                                 (TileTag.GROW, TileTag.DAMAGE, TileTag.BLOCK_MOVE)),
    TileID.AIR: TileData("air", (Graphic.AIR, Color.LIGHT_BLUE), 5,
                                    (TileTag.BLOCK_MOVE,)),
    TileID.CLOUD: TileData("cloud", (Graphic.CLOUD, Color.WHITE), 10, ),
    TileID.WEB: TileData("web", (Graphic.WEB, Color.WHITE), 10, (TileTag.DRAIN,)),
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
