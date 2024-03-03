from collections import namedtuple
from enum import Enum, auto

Point = namedtuple("Point", ["x", "y"])

PointType = tuple[int, int] | Point


class Color:
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (64, 255, 64)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (128, 128, 0)
    BLUE = (0, 0, 255)
    STONE = (170, 170, 170)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    MOB_GREEN = (128, 255, 128)
    BROWN = (170, 85, 0)
    DARK_BROWN = (32, 16, 0)
    ORANGE = (255, 128, 0)
    IRON = (230, 230, 230)
    GOLD = (255, 215, 0)
    GEM = (200, 0, 255)
    DARK_GRAY = (64, 64, 64)
    LIGHT_BROWN = (200, 200, 170)
    LIGHT_BLUE = (0, 100, 255)


class Graphic:
    GRASS = (5, 0)
    SAND = (2, 0)
    LIQUID = (8, 5)
    STONE_TILE = (1, 17)
    TREE = (4, 2)
    CACTUS = (6, 1)
    FARMLAND = (12, 6)
    DOWN_STAIRS = (3, 6)
    UP_STAIRS = (2, 6)
    WHEAT = (17, 6)
    PALM_TREE = (7, 2)
    ORE = (1, 2)
    DESERT_BONES = (0, 15)
    SMALL_TREE = (2, 1)
    SMALL_CACTUS = (7, 1)

    WINDOW = (1, 4)
    PLANKS = (13, 16)
    BRICKS = (10, 17)
    DOOR_CLOSED = (8, 9)
    DOOR_OPEN = (9, 9)

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
    OVEN = (8, 21)
    FURNACE = (47, 4)
    ANVIL = (14, 15)
    LANTERN = (44, 4)
    TORCH = (3, 15)

    DIRT = (6, 0)
    STONE_ITEM = (5, 2)
    WOOD = (18, 6)
    PICKUP = (41, 0)
    EMPTY_HANDS = (41, 1)
    APPLE = (33, 18)
    PEAR = (34, 18)
    BOTTLE = (33, 19)
    SEEDS = (14, 6)
    PICKAXE = (43, 5)
    SWORD = (32, 8)
    SHOVEL = (42, 5)
    HOE = (44, 5)
    AXE = (42, 7)
    GEM = (32, 10)
    COCONUT = (27, 21)
    SLIME_ITEM = (17, 12)
    CLOTH = (47, 6)
    INGOT = (34, 10)
    GLASS = (41, 13)
    BREAD = (47, 7)
    PIE = (37, 2)
    BONE = (32, 12)


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
    "H": (42, 10),
    "S": (42, 12),

}


class MobID(Enum):
    PLAYER = 1
    GREEN_ZOMBIE = 2
    GREEN_SLIME = 3
    GREEN_SKELETON = 4
    AIR_WIZARD = 5
    WORKBENCH = 6
    OVEN = 7
    FURNACE = 8
    ANVIL = 9
    WOOD_LANTERN = 10
    TORCH = 11


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
    WOOD_SHOVEL = 12
    WOOD_AXE = 13
    WOOD_HOE = 14
    WHEAT = 15
    IRON_ORE = 16
    GOLD_ORE = 17
    GEM = 18
    COCONUT = 19
    COAL = 20
    CLOTH = 21
    SLIME = 22
    IRON_BAR = 23
    GOLD_BAR = 24
    GLASS = 25
    BREAD = 26
    APPLE_PIE = 27
    OVEN = 28
    FURNACE = 29
    ANVIL = 30
    WOOD_LANTERN = 31
    TORCH = 32
    BONE = 33
    WINDOW = 34
    WOOD_WALL = 35
    STONE_WALL = 36
    WOOD_DOOR = 37
    GOLD_APPLE = 38
    POKE_PEAR = 39
    COCKTAIL = 40
    TREE_SAPLING = 41
    PALM_TREE_SAPLING = 42
    CACTUS_SAPLING = 43


class ItemTag(Enum):
    STACKABLE = auto()
    PICKUP = auto()
    SPAWN_MOB = auto()
    HEAL = auto()
    BREAK_TILE = auto()
    PLACE_TILE = auto()
    DAMAGE_MOBS = auto()
    STAMINA = auto()


class TileID(Enum):
    GRASS = 1
    SAND = 2
    WATER = 3
    STONE = 4
    TREE = 5
    CACTUS = 6
    DIRT = 7
    HOLE = 8
    FARMLAND = 9
    LAVA = 10
    WHEAT = 11
    DOWN_STAIRS = 12
    UP_STAIRS = 13
    PALM_TREE = 14
    IRON_ORE = 15
    GOLD_ORE = 16
    GEM_ORE = 17
    DESERT_BONES = 18
    WINDOW = 19
    STONE_WALL = 20
    WOOD_WALL = 21
    OPEN_WOOD_DOOR = 22
    CLOSED_WOOD_DOOR = 23
    WHEAT_SEEDS = 24
    TREE_SAPLING = 25
    PALM_TREE_SAPLING = 26
    CACTUS_SAPLING = 27


class TileTag(Enum):
    BLOCK_SIGHT = auto()
    BLOCK_MOVE = auto()
    DAMAGE = auto()
    DOWN_STAIRS = auto()
    UP_STAIRS = auto()
    LIQUID = auto()
    LIGHT = auto()
    GROW = auto()
    CRUSH = auto()
