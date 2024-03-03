from collections import namedtuple

from data import Color, Graphic, TileID, TileTag, ItemID


tile_replace = {
    TileID.GRASS: (TileID.DIRT, ItemID.WHEAT_SEEDS),
    TileID.SAND: (TileID.DIRT, ItemID.SAND),
    TileID.STONE: (TileID.DIRT, ItemID.STONE),
    TileID.TREE: (TileID.GRASS, ItemID.WOOD),
    TileID.CACTUS: (TileID.SAND, ItemID.WOOD),
    TileID.DIRT: (TileID.HOLE, ItemID.DIRT),
}


TileData = namedtuple("TileData", ("name", "graphic", "max_health", "tags"),
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
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.DIRT: TileData("dirt", (Graphic.DIRT, Color.BROWN),),
    TileID.HOLE: TileData("hole", (Graphic.LIQUID, Color.DARK_BROWN),),
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
