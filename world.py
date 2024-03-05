import random
from collections import namedtuple

import opensimplex

from tiles import Tile, TileID
from data import PointType


Layer = namedtuple("Layer", ("tile_array", "mob_array", "mem_array"))


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
        self.seed = world_seed
        self.mob_cap = (self.size[0] * self.size[1]) // 50
        # World layers start out blank and are generated on demand.
        self.overworld_layer = Layer(None, None, None)
        self.cave_layer = Layer(None, None, None)

    def generate_overworld_layer(self):
        tile_array = generate_caves(self.size, self.seed)
        mob_array = make_2d_array(self.size, None)
        mem_array = make_2d_array(self.size, False)
        self.overworld_layer = Layer(tile_array, mob_array, mem_array)

    def generate_caves(self):
        tile_array = generate_caves(self.size, self.seed)
        mob_array = make_2d_array(self.size, None)
        mem_array = make_2d_array(self.size, False)
        self.cave_layer = Layer(tile_array, mob_array, mem_array)


# World Gen functions below
def generate_overworld(size: tuple[int, int], world_seed: int) -> list[list]:
    world_map = make_2d_array(size, Tile(TileID.GRASS))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    humidity_scale = 0.07
    humidity_offset = (300, 300)
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
    return world_map


def generate_caves(size: tuple[int, int], world_seed: int) -> list[list]:
    world_map = make_2d_array(size, Tile(TileID.DIRT))
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    altitude_offset = (400, 400)
    ore_scale = 0.2
    ore_offset = (100, 100)
    biome_scale = 0.1
    biome_offset = (0, 0)
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
                    world_map[x][y] = Tile(TileID.DIRT)
                else:
                    world_map[x][y] = Tile(TileID.WHEAT_SEEDS)
            elif altitude < 0.7:
                if ore < -0.5:
                    world_map[x][y] = Tile(TileID.IRON_ORE)
                else:
                    world_map[x][y] = Tile(TileID.STONE)
            else:
                world_map[x][y] = Tile(TileID.LAPIS_ORE)
    return world_map
