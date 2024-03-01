from enum import Enum, IntEnum, StrEnum, auto
from collections import defaultdict, namedtuple

import pygame as pg

Point = namedtuple("Point", ["x", "y"])

PointType = tuple[int, int] | pg.Vector2 | Point


class MobID(IntEnum):
    PLAYER = 1
    GREEN_ZOMBIE = 2
    GREEN_SLIME = 3
    GREEN_SKELETON = 4
    AIR_WIZARD = 5


MobData = namedtuple("MobData", ("id", "health"))


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
    DARK_YELLOW = (128, 128, 0)
    BLUE = (0, 0, 255)
    STONE = (170, 170, 170)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    MOB_GREEN = (64, 200, 64)


class Tile(Enum):
    PLAYER = (25, 0)
    ZOMBIE = (24, 9)
    SLIME = (27, 8)
    SKELETON = (29, 6)
    AIR_WIZARD = (24, 1)

    HEART_FULL = (42, 10)
    HEART_EMPTY = (40, 10)
    STAM_FULL = (42, 12)
    STAM_EMPTY = (40, 12)

    CURSOR = (36, 12)


str_2_tile = {
    "0": (35, 17),
    "1": (36, 17),
    "2": (37, 17),
    "3": (38, 17),
    "4": (39, 17),
    "5": (40, 17),
    "6": (41, 17),
    "7": (42, 17),
    "8": (43, 17),
    "9": (44, 17),
    "a": (35, 18),
    "b": (36, 18),
    "c": (37, 18),
    "d": (38, 18),
    "e": (39, 18),
    "f": (40, 18),
    "g": (41, 18),
    "h": (42, 18),
    "i": (43, 18),
    "j": (44, 18),
    "k": (45, 18),
    "l": (46, 18),
    "m": (47, 18),
    "n": (35, 19),
    "o": (36, 19),
    "p": (37, 19),
    "q": (38, 19),
    "r": (39, 19),
    "s": (40, 19),
    "t": (41, 19),
    "u": (42, 19),
    "v": (43, 19),
    "w": (44, 19),
    "x": (45, 19),
    "y": (46, 19),
    "z": (47, 19),
    " ": (0, 0),

}

tile_graphics = {
    TileID.GRASS: ((5, 0), Colors.GREEN.value),
    TileID.SAND: ((2, 0), Colors.YELLOW.value),
    TileID.WATER: ((8, 5), Colors.BLUE.value),
    TileID.STONE: ((1, 17), Colors.STONE.value),
    TileID.TREE: ((4, 2), Colors.GREEN.value),
    TileID.CACTUS: ((6, 1), Colors.GREEN.value),
}

mob_graphics = {
    MobID.PLAYER: (Tile.PLAYER.value, Colors.WHITE.value),
    MobID.GREEN_ZOMBIE: (Tile.ZOMBIE.value, Colors.MOB_GREEN.value),
    MobID.GREEN_SLIME: (Tile.SLIME.value, Colors.MOB_GREEN.value),
    MobID.GREEN_SKELETON: (Tile.SKELETON.value, Colors.MOB_GREEN.value),
    MobID.AIR_WIZARD: (Tile.AIR_WIZARD.value, Colors.RED.value),
}

tile_tags = defaultdict(tuple)
tile_tags.update({
    TileID.TREE: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.STONE: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.CACTUS: (TileTag.BLOCK_MOVE, TileTag.BLOCK_SIGHT),
    TileID.WATER: (TileTag.BLOCK_MOVE,),
})
