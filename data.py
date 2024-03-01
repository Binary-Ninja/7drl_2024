from enum import Enum, IntEnum, StrEnum, auto
from collections import defaultdict

import pygame as pg

PointType = tuple[int, int] | pg.Vector2


class TileID(IntEnum):
    # Not using auto makes it easier to keep track of consistent values.
    # Not using zero makes all TileIDs truthy.
    GRASS = 1
    SAND = 2
    WATER = 3
    STONE = 4
    TREE = 5
    CACTUS = 6


class TileTag(StrEnum):
    BLOCK_SIGHT = auto()
    BLOCK_MOVE = auto()


class Colors(Enum):
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    STONE = (170, 170, 170)


tile_graphics = {
    TileID.GRASS: ((5, 0), Colors.GREEN.value),
    TileID.SAND: ((2, 0), Colors.YELLOW.value),
    TileID.WATER: ((8, 5), Colors.BLUE.value),
    TileID.STONE: ((1, 17), Colors.STONE.value),
    TileID.TREE: ((4, 2), Colors.GREEN.value),
    TileID.CACTUS: ((6, 1), Colors.GREEN.value),
}

tile_tags = defaultdict(tuple)
tile_tags.update({
    TileID.TREE: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.STONE: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.CACTUS: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.WATER: (TileTag.BLOCK_MOVE,),
})
