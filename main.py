#!/usr/bin/env python3
import sys
from pathlib import Path
import random

import pygame as pg

from tileloader import TileLoader
from world import World, set_array, get_array
from data import MobID, Point, MobData, tile_graphics


def main():
    pg.init()

    screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("7DRL 2024")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 20)

    tile_size = Point(16, 16)
    tile_loader = TileLoader(Path() / "kenney_tileset.png", tile_size)
    player_tile = tile_loader.get_tile((25, 0))

    world_seed = random.getrandbits(64)
    world_seed = 1234
    print(world_seed)
    game_world = World((100, 100), world_seed)
    game_world.generate_overworld_layer()

    player_pos = Point(game_world.size[0] // 2, game_world.size[1] // 2)
    set_array(player_pos, game_world.overworld_layer.mob_array, MobData(MobID.PLAYER, 10))

    def get_world_tile(tx, ty) -> pg.Surface | None:
        tile_id = get_array((tx, ty), game_world.overworld_layer.tile_array)
        if tile_id is not None:
            return tile_loader.get_tile(*tile_graphics[tile_id])

    while True:
        # Handle events.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        # Update.
        clock.tick()

        # Draw.
        screen.fill((0, 0, 0))

        # Display world.
        for x in range(35):
            for y in range(35):
                if tile := get_world_tile(x, y):
                    screen.blit(tile, (x * tile_size.x, y * tile_size.y))

        # Display FPS.
        fps_surf = font.render(str(clock.get_fps()), True, (255, 255, 255))
        screen.blit(fps_surf, (0, screen.get_height() - fps_surf.get_height()))
        # Flip display.
        pg.display.flip()


if __name__ == "__main__":
    main()
