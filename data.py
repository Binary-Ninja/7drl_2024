from collections import namedtuple
from enum import Enum, auto

Point = namedtuple("Point", ["x", "y"])

PointType = tuple[int, int] | Point


class Color:
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (128, 128, 0)
    BLUE = (0, 0, 255)
    STONE = (170, 170, 170)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    MOB_GREEN = (64, 200, 64)
    BROWN = (170, 85, 0)
    DARK_BROWN = (100, 50, 0)


class Graphic:
    GRASS = (5, 0)
    SAND = (2, 0)
    LIQUID = (8, 5)
    STONE_TILE = (1, 17)
    TREE = (4, 2)
    CACTUS = (6, 1)

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
    CURSOR2 = (29, 21)
    EMPTY = (0, 0)

    WORKBENCH = (14, 9)
    DIRT = (6, 0)
    STONE_ITEM = (5, 2)
    WOOD = (18, 6)
    PICKUP = (41, 0)
    EMPTY_HANDS = (41, 1)
    APPLE = (33, 18)
    SEEDS = (14, 6)
    PICKAXE = (43, 5)
    SWORD = (32, 8)


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
    "+": (36, 20),
    "-": (37, 20),

}


class MobID(Enum):
    PLAYER = 1
    GREEN_ZOMBIE = 2
    GREEN_SLIME = 3
    GREEN_SKELETON = 4
    AIR_WIZARD = 5
    WORKBENCH = 6


class MobTag(Enum):
    PUSHABLE = auto()
    CRAFTING = auto()


class ItemID(Enum):
    WORKBENCH = 1
    DIRT = 2
    STONE = 3
    SAND = 4
    WOOD = 5
    PICKUP = 6
    APPLE = 7
    WHEAT_SEEDS = 8
    WOOD_PICK = 9
    WOOD_SWORD = 10
    EMPTY_HANDS = 11


class ItemTag(Enum):
    STACKABLE = auto()
    PICKUP = auto()
    SPAWN_MOB = auto()
    HEAL = auto()
    BREAK_TILE = auto()
    PLACE_TILE = auto()
    DAMAGE_MOBS = auto()


class TileID(Enum):
    GRASS = 1
    SAND = 2
    WATER = 3
    STONE = 4
    TREE = 5
    CACTUS = 6
    DIRT = 7
    HOLE = 8


class TileTag(Enum):
    BLOCK_SIGHT = auto()
    BLOCK_MOVE = auto()
