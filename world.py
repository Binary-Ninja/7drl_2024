import random
from collections import namedtuple
from typing import Callable

import opensimplex

from tiles import Tile, TileID
from data import PointType


Layer = namedtuple("Layer", ("tile_array", "mob_array", "mem_array"))

STAIR_BORDER_PAD = 5
STAIR_STAIR_PAD = 5


def distance_within(a: PointType, b: PointType, dist: int | float) -> bool:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 <= dist ** 2


def distance_within_any(a: PointType, b: list[PointType], dist: float | int) -> bool:
    for p in b:
        if distance_within(a, p, dist):
            return True
    return False


def make_2d_array(size: tuple[int, int], default) -> list[list]:
    """Create 2D array of specified size filled with value 'default'."""
    return [[default for y in range(size[1])] for x in range(size[0])]


def get_array(pos: PointType, array: list[list]):
    """Return what the 2D array holds at pos, or None if out of bounds."""
    # Handle negative indices.
    if pos[0] < 0 or pos[1] < 0:
        return
    try:
        return array[int(pos[0])][int(pos[1])]
    except IndexError:
        return


def set_array(pos: PointType, array: list[list], value) -> bool:
    """Set the contents of array at pos, returning False if out of bounds."""
    # Handle negative indices.
    if pos[0] < 0 or pos[1] < 0:
        return False
    try:
        array[int(pos[0])][int(pos[1])] = value
        return True
    except IndexError:
        return False


class World:
    """Container of layers."""
    def __init__(self, size: tuple[int, int], world_seed: int):
        self.size = size
        assert (size[0] >= 50 and size[1] >= 50), "Minimum world size is 50x50"
        self.seed = world_seed
        self.mob_cap = (self.size[0] * self.size[1]) // 50
        # Layers are generated when called.
        self.overworld_layer = None
        self.cave_layer = None
        self.cavern_layer = None
        self.hell_layer = None
        self.sky_layer = None

    def generate_layers(self):
        yield "generating paradise..."
        self.sky_layer, sky_stairs = self.generate_layer(generate_sky, [])
        yield "generating overworld..."
        self.overworld_layer, over_stairs = self.generate_layer(generate_overworld, sky_stairs)
        yield "generating caves..."
        self.cave_layer, cave_stairs = self.generate_layer(generate_caves, over_stairs)
        yield "generating caverns..."
        self.cavern_layer, cavern_stairs = self.generate_layer(generate_caverns, cave_stairs)
        yield "generating underworld..."
        self.hell_layer, _ = self.generate_layer(generate_hell, cavern_stairs)

    def generate_layer(self, gen_func: Callable, upstairs: list) -> tuple[Layer, list]:
        tile_array, stairs = gen_func(self.size, self.seed, upstairs)
        mob_array = make_2d_array(self.size, None)
        mem_array = make_2d_array(self.size, None)
        return Layer(tile_array, mob_array, mem_array), stairs


# World Gen functions below
def generate_overworld(size: tuple[int, int], world_seed: int, upstairs: list) -> tuple[list[list], list]:
    world_map = make_2d_array(size, Tile(TileID.GRASS))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    humidity_scale = 0.07
    humidity_offset = (300, 300)
    number_of_stairs = round((size[0] * size[1]) // 1500)
    down_stairs: list[tuple[int, int]] = []
    for x in range(size[0]):
        for y in range(size[1]):
            value = opensimplex.noise2(x * altitude_scale, y * altitude_scale)
            humidity = opensimplex.noise2((x + humidity_offset[0]) * humidity_scale,
                                          (y + humidity_offset[1]) * humidity_scale)
            if value < -0.2:
                world_map[x][y] = Tile(TileID.WATER)
            elif value < 0:
                if rng.random() > 0.95 and humidity >= -0.4:
                    world_map[x][y] = Tile(TileID.PALM_TREE)
                else:
                    world_map[x][y] = Tile(TileID.SAND)
            elif value < 0.5:
                if humidity < -0.4:
                    desert_detail = rng.random()
                    if desert_detail > 0.98:
                        world_map[x][y] = Tile(TileID.DESERT_BONES)
                    elif desert_detail > 0.95:
                        world_map[x][y] = Tile(TileID.CACTUS)
                    else:
                        world_map[x][y] = Tile(TileID.SAND)
                elif humidity < 0:
                    pass  # already grass
                elif humidity < 1:
                    if rng.random() + humidity > 1:
                        world_map[x][y] = Tile(TileID.TREE)
            elif value < 1:
                world_map[x][y] = Tile(TileID.STONE)
    for point in upstairs:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    world_map[point[0]][point[1]] = Tile(TileID.UP_STAIRS)
                else:
                    world_map[point[0] + x][point[1] + y] = Tile(TileID.OBSIDIAN_BRICKS)
    for _ in range(number_of_stairs):
        stair_not_done = True
        while stair_not_done:
            point = (random.randint(STAIR_BORDER_PAD, size[0] - STAIR_BORDER_PAD - 1),
                     random.randint(STAIR_BORDER_PAD, size[1] - STAIR_BORDER_PAD - 1))
            if distance_within_any(point, upstairs, STAIR_STAIR_PAD):
                continue
            stone_count = 0
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if x == y == 0:
                        continue
                    if world_map[point[0] + x][point[1] + y].id == TileID.STONE:
                        stone_count += 1
            if 3 < stone_count < 7:
                world_map[point[0]][point[1]] = Tile(TileID.DOWN_STAIRS)
                down_stairs.append(point)
                stair_not_done = False
    return world_map, down_stairs


def generate_caves(size: tuple[int, int], world_seed: int, upstairs: list) -> tuple[list[list], list]:
    world_map = make_2d_array(size, Tile(TileID.DIRT))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    altitude_offset = (400, 400)
    ore_scale = 0.2
    ore_offset = (100, 100)
    biome_scale = 0.1
    biome_offset = (0, 0)
    number_of_stairs = round((size[0] * size[1]) // 1500)
    down_stairs: list[tuple[int, int]] = []
    for x in range(size[0]):
        for y in range(size[1]):
            altitude = opensimplex.noise2((x + altitude_offset[0]) * altitude_scale,
                                          (y + altitude_offset[1]) * altitude_scale)
            ore = opensimplex.noise2((x + ore_offset[0]) * ore_scale,
                                     (y + ore_offset[1]) * ore_scale)
            biome = opensimplex.noise2((x + biome_offset[0]) * biome_scale,
                                     (y + biome_offset[1]) * biome_scale)
            if altitude < 0:
                if biome < -0.3 and rng.random() + biome < 0.2:
                    world_map[x][y] = Tile(TileID.WEB)
                elif biome < 0.5:
                    if rng.random() > 0.98:
                        world_map[x][y] = Tile(TileID.THORNS)
                    else:
                        pass  # already dirt
                else:
                    world_map[x][y] = Tile(TileID.SAND)
            elif altitude < 0.7:
                if ore < -0.5:
                    world_map[x][y] = Tile(TileID.IRON_ORE)
                else:
                    world_map[x][y] = Tile(TileID.STONE)
            else:
                world_map[x][y] = Tile(TileID.LAPIS_ORE)
    for point in upstairs:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    world_map[point[0]][point[1]] = Tile(TileID.UP_STAIRS)
                else:
                    world_map[point[0] + x][point[1] + y] = Tile(TileID.DIRT)
    for _ in range(number_of_stairs):
        stair_not_done = True
        while stair_not_done:
            point = (random.randint(STAIR_BORDER_PAD, size[0] - STAIR_BORDER_PAD - 1),
                     random.randint(STAIR_BORDER_PAD, size[1] - STAIR_BORDER_PAD - 1))
            if distance_within_any(point, upstairs, STAIR_STAIR_PAD):
                continue
            stone_count = 0
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if x == y == 0:
                        continue
                    if world_map[point[0] + x][point[1] + y].id in (TileID.STONE, TileID.IRON_ORE, TileID.LAPIS_ORE):
                        stone_count += 1
            if 3 < stone_count < 7:
                world_map[point[0]][point[1]] = Tile(TileID.DOWN_STAIRS)
                down_stairs.append(point)
                stair_not_done = False
    return world_map, down_stairs


def generate_caverns(size: tuple[int, int], world_seed: int, upstairs: list) -> tuple[list[list], list]:
    world_map = make_2d_array(size, Tile(TileID.DIRT))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    altitude_offset = (500, 500)
    ore_scale = 0.2
    ore_offset = (250, 250)
    biome_scale = 0.1
    biome_offset = (0, 0)
    water_scale = 0.08
    water_offset = (300, 300)
    number_of_stairs = round((size[0] * size[1]) // 1500)
    down_stairs: list[tuple[int, int]] = []
    for x in range(size[0]):
        for y in range(size[1]):
            altitude = opensimplex.noise2((x + altitude_offset[0]) * altitude_scale,
                                          (y + altitude_offset[1]) * altitude_scale)
            ore = opensimplex.noise2((x + ore_offset[0]) * ore_scale,
                                     (y + ore_offset[1]) * ore_scale)
            biome = opensimplex.noise2((x + biome_offset[0]) * biome_scale,
                                     (y + biome_offset[1]) * biome_scale)
            water = opensimplex.noise2((x + water_offset[0]) * water_scale,
                                     (y + water_offset[1]) * water_scale)
            if altitude < 0:
                if biome < -0.3:
                    if rng.random() + biome > 0.2:
                        world_map[x][y] = Tile(TileID.BIG_MUSHROOM)
                    else:
                        world_map[x][y] = Tile(TileID.FLOOR_FUNGUS)
                elif biome < 0.5:
                    if rng.random() > 0.98:
                        world_map[x][y] = Tile(TileID.BIG_MUSHROOM)
                    else:
                        pass  # already dirt
                else:
                    world_map[x][y] = Tile(TileID.SAND)
            elif altitude < 0.7:
                if ore < -0.5:
                    world_map[x][y] = Tile(TileID.GOLD_ORE)
                else:
                    world_map[x][y] = Tile(TileID.STONE)
            else:
                world_map[x][y] = Tile(TileID.LAPIS_ORE)
            if water < -0.2:
                world_map[x][y] = Tile(TileID.WATER)
    for point in upstairs:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    world_map[point[0]][point[1]] = Tile(TileID.UP_STAIRS)
                else:
                    world_map[point[0] + x][point[1] + y] = Tile(TileID.DIRT)
    for _ in range(number_of_stairs):
        stair_not_done = True
        while stair_not_done:
            point = (random.randint(STAIR_BORDER_PAD, size[0] - STAIR_BORDER_PAD - 1),
                     random.randint(STAIR_BORDER_PAD, size[1] - STAIR_BORDER_PAD - 1))
            if distance_within_any(point, upstairs, STAIR_STAIR_PAD):
                continue
            stone_count = 0
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if x == y == 0:
                        continue
                    if world_map[point[0] + x][point[1] + y].id in (TileID.STONE, TileID.GOLD_ORE, TileID.LAPIS_ORE):
                        stone_count += 1
            if 3 < stone_count < 7:
                world_map[point[0]][point[1]] = Tile(TileID.DOWN_STAIRS)
                down_stairs.append(point)
                stair_not_done = False
    return world_map, down_stairs


def generate_hell(size: tuple[int, int], world_seed: int, upstairs: list) -> tuple[list[list], list]:
    world_map = make_2d_array(size, Tile(TileID.DIRT))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    altitude_offset = (700, 700)
    ore_scale = 0.2
    ore_offset = (600, 600)
    biome_scale = 0.1
    biome_offset = (0, 0)
    water_scale = 0.08
    water_offset = (450, 450)
    for x in range(size[0]):
        for y in range(size[1]):
            altitude = opensimplex.noise2((x + altitude_offset[0]) * altitude_scale,
                                          (y + altitude_offset[1]) * altitude_scale)
            ore = opensimplex.noise2((x + ore_offset[0]) * ore_scale,
                                     (y + ore_offset[1]) * ore_scale)
            biome = opensimplex.noise2((x + biome_offset[0]) * biome_scale,
                                     (y + biome_offset[1]) * biome_scale)
            water = opensimplex.noise2((x + water_offset[0]) * water_scale,
                                     (y + water_offset[1]) * water_scale)
            if altitude < 0:
                if biome < -0.3:
                    if rng.random() + biome < 0.2:
                        world_map[x][y] = Tile(TileID.WEB)
                elif biome < 0.2:
                    pass  # dirt
                else:
                    if rng.random() > 0.9:
                        world_map[x][y] = Tile(TileID.LAVA)
                    else:
                        world_map[x][y] = Tile(TileID.ASH)
            elif altitude < 0.7:
                if ore < -0.5:
                    world_map[x][y] = Tile(TileID.GEM_ORE)
                else:
                    world_map[x][y] = Tile(TileID.STONE)
            else:
                world_map[x][y] = Tile(TileID.LAPIS_ORE)
            if water < -0.2:
                world_map[x][y] = Tile(TileID.LAVA)
    for point in upstairs:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    world_map[point[0]][point[1]] = Tile(TileID.UP_STAIRS)
                else:
                    world_map[point[0] + x][point[1] + y] = Tile(TileID.DIRT)
    return world_map, []  # hell doesn't go down any further


def generate_sky(size: tuple[int, int], world_seed: int, upstairs: list) -> tuple[list[list], list]:
    world_map = make_2d_array(size, Tile(TileID.CLOUD))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    humidity_scale = 0.07
    humidity_offset = (300, 300)
    number_of_stairs = round((size[0] * size[1]) // 1500)
    down_stairs: list[tuple[int, int]] = []
    for x in range(size[0]):
        for y in range(size[1]):
            value = opensimplex.noise2(x * altitude_scale, y * altitude_scale)
            humidity = opensimplex.noise2((x + humidity_offset[0]) * humidity_scale,
                                          (y + humidity_offset[1]) * humidity_scale)
            if value < 0:
                world_map[x][y] = Tile(TileID.AIR)
            elif value < 0.5:
                if humidity < -0.4:
                    if rng.random() > 0.9:
                        world_map[x][y] = Tile(TileID.QUARTZ_ORE)
                    else:
                        world_map[x][y] = Tile(TileID.CLOUD)
                elif humidity < 0:
                    pass  # cloud
                elif humidity < 1:
                    if rng.random() + humidity > 1.2:
                        world_map[x][y] = Tile(TileID.AIR)
            elif value < 1:
                world_map[x][y] = Tile(TileID.CLOUD_BANK)
    for _ in range(number_of_stairs):
        point = (random.randint(STAIR_BORDER_PAD, size[0] - STAIR_BORDER_PAD - 1),
                 random.randint(STAIR_BORDER_PAD, size[1] - STAIR_BORDER_PAD - 1))
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    world_map[point[0]][point[1]] = Tile(TileID.DOWN_STAIRS)
                else:
                    world_map[point[0] + x][point[1] + y] = Tile(TileID.CLOUD)
        down_stairs.append(point)
    return world_map, down_stairs
