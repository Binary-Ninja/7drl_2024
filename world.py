import random
from collections import namedtuple

import opensimplex

from data import TileID, PointType


Layer = namedtuple("Layer", ("tile_array", "mob_array"))


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
        # World layers start out blank and are generated on demand.
        self.overworld_layer = Layer(None, None)

    def generate_overworld_layer(self):
        tile_array = generate_overworld(self.size, self.seed)
        mob_array = make_2d_array(self.size, 0)
        self.overworld_layer = Layer(tile_array, mob_array)


# World Gen functions below
def generate_overworld(size: tuple[int, int], world_seed: int) -> list[list]:
    world_map = make_2d_array(size, TileID.GRASS)
    opensimplex.seed(world_seed)
    rng = random.Random(world_seed)
    altitude_scale = 0.08
    humidity_scale = 0.08
    humidity_offset = (300, 300)
    for x in range(size[0]):
        for y in range(size[1]):
            value = opensimplex.noise2(x * altitude_scale, y * altitude_scale)
            if value < -0.2:
                world_map[x][y] = TileID.WATER
            elif value < 0:
                world_map[x][y] = TileID.SAND
            elif value < 0.5:
                humidity = opensimplex.noise2((x + humidity_offset[0]) * humidity_scale,
                                              (y + humidity_offset[1]) * humidity_scale)
                if humidity < -0.4:
                    if rng.random() > 0.95:
                        world_map[x][y] = TileID.CACTUS
                    else:
                        world_map[x][y] = TileID.SAND
                elif humidity < 0:
                    pass  # already grass
                elif humidity < 1:
                    if rng.random() + humidity > 1:
                        world_map[x][y] = TileID.TREE
            elif value < 0.9:
                world_map[x][y] = TileID.STONE
    return world_map