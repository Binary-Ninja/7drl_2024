from collections import namedtuple
from enum import Enum, auto

Point = namedtuple("Point", ["x", "y"])

PointType = tuple[int, int] | Point


class Color:
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (64, 200, 64)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (128, 128, 0)
    BLUE = (0, 0, 255)
    STONE = (170, 170, 170)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (200, 200, 200)
    MED_GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    DARK_RED = (128, 0, 0)
    MOB_GREEN = (128, 255, 128)
    MOB_RED = (255, 128, 128)
    MOB_WHITE = (200, 200, 200)
    MOB_BLACK = (64, 64, 64)
    BROWN = (170, 85, 0)
    DARK_BROWN = (32, 16, 0)
    FLOOR_BROWN = (64, 32, 0)
    ORANGE = (255, 128, 0)
    IRON = (230, 230, 230)
    GOLD = (255, 215, 0)
    GEM = (255, 0, 255)
    DARK_GRAY = (64, 64, 64)
    LIGHT_BROWN = (200, 200, 170)
    LIGHT_BLUE = (100, 100, 255)
    OBSIDIAN = (150, 0, 210)
    DARK_OBSIDIAN = (75, 0, 100)
    PINK = (255, 100, 255)


class Graphic:
    GRASS = (5, 0)
    SAND = (2, 0)
    LIQUID = (8, 5)
    HOLE = (8, 5)
    STONE_TILE = (1, 17)
    TREE = (4, 2)
    CACTUS = (6, 1)
    FARMLAND = (12, 6)
    DOWN_STAIRS = (3, 6)
    UP_STAIRS = (2, 6)
    WHEAT = (17, 6)
    CROP2 = (16, 6)
    PALM_TREE = (7, 2)
    ORE = (1, 2)
    DESERT_BONES = (0, 15)
    SMALL_TREE = (2, 1)
    SMALL_CACTUS = (7, 1)
    AIR = (8, 5)
    CLOUD = (7, 0)
    WEB = (2, 15)
    GRASS2 = (1, 0)
    TREE2 = (4, 1)
    THORNS = (6, 2)
    OBSIDIAN = (4, 0)
    BOOKCASE = (3, 7)

    WINDOW = (1, 4)
    PLANKS = (13, 16)
    BRICKS = (10, 17)
    DOOR_CLOSED = (8, 9)
    DOOR_OPEN = (9, 9)
    FLOOR1 = (16, 0)
    FLOOR2 = (17, 0)
    FLOOR3 = (48, 9)
    FLOOR4 = (48, 12)

    PLAYER = (25, 0)
    ZOMBIE = (24, 9)
    SLIME = (27, 8)
    SKELETON = (29, 6)
    AIR_WIZARD = (24, 1)
    SPIDER = (28, 5)
    BAT = (26, 8)
    SKULL = (38, 11)
    SHADE = (24, 7)
    DUCK = (25, 7)
    FAIRY = (31, 5)
    CHICKEN = (26, 7)
    DOG = (31, 7)
    CAT = (30, 7)
    PIG = (29, 7)
    UFO = (14, 20)
    UFO2 = (14, 19)
    DEVIL = (27, 2)

    HEART_FULL = (42, 10)
    HEART_EMPTY = (40, 10)
    STAM_FULL = (42, 12)
    STAM_EMPTY = (40, 12)
    POTION_EFFECT = (35, 11)

    CURSOR = (36, 12)
    CURSOR2 = (29, 21)
    EMPTY = (0, 0)

    WORKBENCH = (14, 9)
    OVEN = (8, 21)
    FURNACE = (47, 4)
    ANVIL = (14, 15)
    LANTERN = (44, 4)
    TORCH = (3, 15)
    TORCH2 = (4, 15)
    TORCH3 = (5, 15)
    BED = (5, 8)
    CAULDRON = (5, 14)
    SKULL_BOOKS = (4, 7)
    LOOM = (44, 9)
    BOMB = (45, 9)

    BUCKET = (47, 3)
    DIRT = (6, 0)
    STONE_ITEM = (5, 2)
    TORCH_ITEM = (43, 3)
    TORCH_ITEM2 = (42, 3)
    WOOD = (18, 6)
    PICKUP = (41, 0)
    EMPTY_HANDS = (41, 1)
    APPLE = (33, 18)
    PEAR = (34, 18)
    CARROT = (34, 20)
    BOTTLE = (33, 19)
    SEEDS = (14, 6)
    SEEDS2 = (13, 6)
    PICKAXE = (43, 5)
    SWORD = (32, 8)
    SHOVEL = (42, 5)
    FISHING_SPEAR = (41, 5)
    HOE = (44, 5)
    AXE = (42, 7)
    GEM = (32, 10)
    COCONUT = (27, 21)
    SLIME_ITEM = (17, 12)
    CLOTH = (47, 6)
    INGOT = (20, 15)
    CRYSTAL = (34, 10)
    GLASS = (41, 13)
    BREAD = (47, 7)
    PIE = (37, 2)
    BONE = (32, 12)
    EMPTY_BOTTLE = (32, 14)
    FULL_BOTTLE = (32, 13)
    EGG = (34, 17)
    STRING = (11, 14)
    FISH = (33, 17)
    MEAT = (33, 16)
    EYE = (41, 3)
    MEAT2 = (34, 19)
    ALIEN_TECH = (21, 12)
    BOOK = (45, 5)
    STAFF = (32, 5)


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
    "*": (38, 20),
    "#": (35, 20),
    "H": (42, 10),
    "S": (42, 12),
    ".": (46, 17),
    ":": (45, 17),
    ">": (29, 20),
    "/": (39, 20),

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
    IRON_LANTERN = 12
    GOLD_LANTERN = 13
    GEM_LANTERN = 14
    RED_ZOMBIE = 15
    RED_SLIME = 16
    RED_SKELETON = 17
    WHITE_ZOMBIE = 18
    WHITE_SLIME = 19
    WHITE_SKELETON = 20
    BLACK_ZOMBIE = 21
    BLACK_SLIME = 22
    BLACK_SKELETON = 23
    BED = 24
    BAT = 25
    FLAME_SKULL = 26
    SPIDER = 27
    HELL_SPIDER = 28
    SHADE = 29
    DUCK = 30
    FAIRY = 31
    CHICKEN = 32
    DOG = 33
    CAT = 34
    PIG = 35
    CLOUD_SPIDER = 36
    LOOM = 37
    SPRITE = 38
    BOMB = 39
    RED_BOMB = 40
    CAULDRON = 41
    WHITE_BOMB = 42
    UFO = 43
    SCRINIUM = 44
    DEVIL = 45
    BOOKCASE = 46
    SKY_TORCH = 47
    GOLD_TORCH = 48


class MobTag(Enum):
    PUSHABLE = auto()
    CRAFTING = auto()
    AI_FOLLOW = auto()
    AI_SHOOT = auto()
    AI_JUMP = auto()
    AI_WANDER = auto()
    AI_SPIDER = auto()
    AI_FLEE = auto()
    DAMAGE = auto()
    NO_DESPAWN = auto()
    BED = auto()
    SWAPPABLE = auto()
    AI_AIR_WIZARD = auto()
    EXPLODE = auto()
    ALWAYS_SIM = auto()
    FURNITURE = auto()


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
    BOTTLE = 44
    STONE_SWORD = 45
    STONE_PICK = 46
    STONE_AXE = 47
    STONE_SHOVEL = 48
    STONE_HOE = 49
    IRON_SWORD = 50
    IRON_PICK = 51
    IRON_AXE = 52
    IRON_SHOVEL = 53
    IRON_HOE = 54
    GOLD_SWORD = 55
    GOLD_PICK = 56
    GOLD_AXE = 57
    GOLD_SHOVEL = 58
    GOLD_HOE = 59
    GEM_SWORD = 60
    GEM_PICK = 61
    GEM_AXE = 62
    GEM_SHOVEL = 63
    GEM_HOE = 64
    CLOUD = 65
    IRON_LANTERN = 66
    GOLD_LANTERN = 67
    GEM_LANTERN = 68
    SPAWN_EGG_GREEN_ZOMBIE = 69
    LAPIS = 70
    BED = 71
    STRING = 72
    FISH = 73
    DEEP_FISH = 74
    FIRE_FISH = 75
    COOKED_FISH = 76
    COOKED_DEEP_FISH = 77
    FISH_SPEAR = 78
    IRON_FISH_SPEAR = 79
    GOLD_FISH_SPEAR = 80
    GEM_FISH_SPEAR = 81
    SPIDER_EYE = 82
    FUNGUS = 83
    SHROOM_SAPLING = 84
    TUBER = 85
    COOKED_TUBER = 86
    PASTRY = 87
    ASH = 88
    DUCK_EGG = 89
    DUCK_MEAT = 90
    COOKED_DUCK_MEAT = 91
    BOILED_EGG = 92
    FAIRY_DUST = 93
    QUARTZ = 94
    CAT_EGG = 95
    DOG_EGG = 96
    PIG_EGG = 97
    CHICKEN_EGG = 98
    WOOD_FLOOR = 99
    STONE_FLOOR = 100
    TUBER_SEEDS = 101
    BUCKET = 102
    WATER_BUCKET = 103
    LAVA_BUCKET = 104
    OBSIDIAN = 105
    OBSIDIAN_FLOOR = 106
    OBSIDIAN_WALL = 108
    LOOM = 109
    BOMB = 110
    RED_BOMB = 111
    CAULDRON = 112
    WHITE_BOMB = 113
    CIRCUIT = 114
    SPACESHIP = 115
    FERTILIZER = 116
    SCRINIUM = 117
    BOOK = 118
    WEB_STAFF = 119
    MAGIC_EYE = 120
    SWIM_POTION = 121
    LAVA_POTION = 123
    INVISIBLE_POTION = 124
    STAMINA_POTION = 125
    IRONSKIN_POTION = 126
    SPEED_POTION = 127
    HEALTH_POTION = 128
    SWIM_LAVA_POTION = 129
    HOVER_POTION = 130
    GOLDSKIN_POTION = 131
    GEMSKIN_POTION = 132
    BOOKCASE = 133
    SKY_TORCH = 134
    GOLD_TORCH = 135
    CLOUD_FLOOR = 136
    CLOUD_BRICKS = 137
    CLOUD_DOOR = 138
    SKY_WINDOW = 139
    OBSIDIAN_DOOR = 140
    LAVA_WALK_POTION = 141


class ItemTag(Enum):
    STACKABLE = auto()
    PICKUP = auto()
    SPAWN_MOB = auto()
    HEAL = auto()
    BREAK_TILE = auto()
    PLACE_TILE = auto()
    DAMAGE_MOBS = auto()
    STAMINA = auto()
    LIGHT = auto()
    FISH = auto()
    POTION = auto()


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
    OBSIDIAN_BRICKS = 28
    AIR = 29
    CLOUD = 30
    CLOUD_BANK = 31
    WEB = 32
    LAPIS_ORE = 33
    THORNS = 34
    FLOOR_FUNGUS = 35
    BIG_MUSHROOM = 36
    SHROOM_SAPLING = 37
    ASH = 38
    QUARTZ_ORE = 39
    ASH_BONES = 40
    WOOD_FLOOR = 41
    STONE_FLOOR = 42
    TUBER_SEEDS = 43
    TUBER_CROP = 44
    OBSIDIAN = 45
    OBSIDIAN_FLOOR = 46
    SKY_WEBS = 47
    CLOUD_FLOOR = 48
    CLOUD_BRICKS = 49
    CLOUD_DOOR_OPEN = 50
    CLOUD_DOOR_CLOSED = 51
    SKY_WINDOW = 52
    OBSIDIAN_DOOR_OPEN = 53
    OBSIDIAN_DOOR_CLOSED = 54
    COAL_ORE = 55


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
    SPREAD = auto()
    DRAIN = auto()
