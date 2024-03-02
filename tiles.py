from enum import Enum, auto
from collections import namedtuple

from data import Color, Graphic


class TileID(Enum):
    GRASS = 1
    SAND = 2
    WATER = 3
    STONE = 4
    TREE = 5
    CACTUS = 6


class TileTag(Enum):
    BLOCK_SIGHT = auto()
    BLOCK_MOVE = auto()


TileData = namedtuple("TileData", ("name", "graphic", "tags"))
tile_data = {
    None: TileData("void", (Graphic.EMPTY, Color.WHITE), tuple()),  # off map edge
    TileID.GRASS: TileData("grass", (Graphic.GRASS, Color.GREEN), tuple()),
    TileID.SAND: TileData("sand", (Graphic.SAND, Color.YELLOW), tuple()),
    TileID.WATER: TileData("water", (Graphic.LIQUID, Color.BLUE), tuple()),
    TileID.STONE: TileData("stone", (Graphic.STONE_TILE, Color.STONE),
                           (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.TREE: TileData("tree", (Graphic.TREE, Color.GREEN),
                          (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
    TileID.CACTUS: TileData("cactus", (Graphic.CACTUS, Color.GREEN),
                            (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT)),
}


class Tile:
    def __init__(self, tileid: TileID):
        self.id = tileid
        self.tile_data = tile_data[self.id]
        self.name = self.tile_data.name
        self.graphic = self.tile_data.graphic
        self.tags = self.tile_data.tags

    def has_tag(self, tag: TileTag) -> bool:
        return tag in self.tags
