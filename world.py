import random

import opensimplex

from data import TileID, PointType


def get(pos: PointType, layer: list[list]):
    """Return what the 2D array holds at pos, or None if out of bounds."""
    # Handle negative indices.
    if pos[0] < 0 or pos[1] < 0:
        return
    try:
        return layer[int(pos[0])][int(pos[1])]
    except IndexError:
        return


def generate_overworld(size: tuple[int, int], world_seed: int) -> list[list]:
    world_map = [[TileID.GRASS for y in range(size[1])] for x in range(size[0])]
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
