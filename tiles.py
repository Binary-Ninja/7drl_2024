from collections import namedtuple, defaultdict

from data import Color, Graphic, TileID, TileTag, ItemID


tile_replace = {
    TileID.GRASS: (TileID.DIRT, ItemID.WHEAT_SEEDS),
    TileID.SAND: (TileID.DIRT, ItemID.SAND),
    TileID.STONE: (TileID.DIRT, ItemID.STONE),
    TileID.TREE: (TileID.GRASS, ItemID.WOOD),
    TileID.CACTUS: (TileID.SAND, ItemID.WOOD),
    TileID.DIRT: (TileID.HOLE, ItemID.DIRT),
    TileID.WHEAT: (TileID.FARMLAND, ItemID.WHEAT),
    TileID.PALM_TREE: (TileID.SAND, ItemID.WOOD),
    TileID.IRON_ORE: (TileID.DIRT, ItemID.IRON_ORE),
    TileID.GOLD_ORE: (TileID.DIRT, ItemID.GOLD_ORE),
    TileID.GEM_ORE: (TileID.DIRT, ItemID.GEM),
}

tile_damage = defaultdict(lambda: 0)
tile_damage.update({
    TileID.CACTUS: 1,
    TileID.LAVA: 5,
    TileID.IRON_ORE: 3,
    TileID.GOLD_ORE: 3,
    TileID.GEM_ORE: 3,
})


TileData = namedtuple("TileData",
                      ("name", "graphic", "max_health", "tags"),
                      defaults=(10, tuple(),))
tile_data = {
    None: TileData("void", (Graphic.EMPTY, Color.WHITE),),  # off map edge
    TileID.GRASS: TileData("grass", (Graphic.GRASS, Color.GREEN),),
    TileID.SAND: TileData("sand", (Graphic.SAND, Color.YELLOW),),
    TileID.WATER: TileData("water", (Graphic.LIQUID, Color.BLUE),),
    TileID.STONE: TileData("stone", (Graphic.STONE_TILE, Color.STONE), 10,
                           (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.TREE: TileData("tree", (Graphic.TREE, Color.GREEN), 10,
                          (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.CACTUS: TileData("cactus", (Graphic.CACTUS, Color.GREEN), 10,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.DIRT: TileData("dirt", (Graphic.DIRT, Color.BROWN),),
    TileID.HOLE: TileData("hole", (Graphic.LIQUID, Color.DARK_BROWN),),
    TileID.FARMLAND: TileData("farmland", (Graphic.FARMLAND, Color.BROWN),),
    TileID.LAVA: TileData("lava", (Graphic.LIQUID, Color.ORANGE), (TileTag.DAMAGE,),),
    TileID.WHEAT: TileData("wheat", (Graphic.WHEAT, Color.YELLOW), ),
    TileID.DOWN_STAIRS: TileData("stairs", (Graphic.DOWN_STAIRS, Color.LIGHT_GRAY),
                                 (TileTag.DOWN_STAIRS,)),
    TileID.UP_STAIRS: TileData("stairs", (Graphic.UP_STAIRS, Color.LIGHT_GRAY),
                               (TileTag.UP_STAIRS,)),
    TileID.PALM_TREE: TileData("palm", (Graphic.PALM_TREE, Color.GREEN), 10,
                               (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.IRON_ORE: TileData("iron ore", (Graphic.ORE, Color.IRON), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.GOLD_ORE: TileData("gold ore", (Graphic.ORE, Color.GOLD), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
    TileID.GEM_ORE: TileData("gem ore", (Graphic.ORE, Color.GEM), 20,
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT, TileTag.DAMAGE)),
}


class Tile:
    def __init__(self, tileid: TileID):
        self.id = tileid
        self.tile_data = tile_data[self.id]
        self.name = self.tile_data.name
        self.graphic = self.tile_data.graphic
        self.health = self.tile_data.max_health
        self.tags = self.tile_data.tags

    def has_tag(self, tag: TileTag) -> bool:
        return tag in self.tags
