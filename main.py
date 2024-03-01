#!/usr/bin/env python3
import sys
from pathlib import Path
import random

import pygame as pg

from tileloader import TileLoader
from world import World, set_array, get_array
from data import (MobID, Point, MobData, tile_graphics, str_2_tile, Colors, Tile,
                  PointType, TileTag, tile_tags, mob_graphics)


def main():
    pg.init()

    screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("7DRL 2024")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 20)

    tile_size = Point(16, 16)
    tile_loader = TileLoader(Path() / "kenney_tileset.png", tile_size)
    heart_full_img = tile_loader.get_tile(Tile.HEART_FULL.value, Colors.RED.value)
    heart_empty_img = tile_loader.get_tile(Tile.HEART_EMPTY.value, Colors.DARK_RED.value)
    stam_full_img = tile_loader.get_tile(Tile.STAM_FULL.value, Colors.YELLOW.value)
    stam_empty_img = tile_loader.get_tile(Tile.STAM_EMPTY.value, Colors.DARK_YELLOW.value)
    cursor_img = tile_loader.get_tile(Tile.CURSOR.value, Colors.WHITE.value)

    cursor_flash_timer = pg.time.get_ticks()
    CURSOR_FLASH_FREQ = 500
    cursor_show = True

    world_seed = random.getrandbits(64)
    world_seed = 1234
    print(world_seed)
    game_world = World((100, 100), world_seed)
    game_world.generate_overworld_layer()

    player_vision = 17
    player_health = 10
    player_stamina = 10
    player_dir = Point(0, -1)
    player_pos = Point(game_world.size[0] // 2, game_world.size[1] // 2)
    set_array(player_pos, game_world.overworld_layer.mob_array, MobData(MobID.PLAYER, 10))

    def spawn_mob(pos: PointType, mob_id: MobID):
        set_array(pos, game_world.overworld_layer.mob_array, MobData(mob_id, 10))

    # add some test mobs
    for _ in range(10):
        spawn_mob((_ * 2, 0), MobID.GREEN_ZOMBIE)
        spawn_mob((_ * 2, 2), MobID.GREEN_SLIME)
        spawn_mob((_ * 2, 4), MobID.GREEN_SKELETON)
        spawn_mob((_ * 2, 6), MobID.AIR_WIZARD)

    def write_text(pos: PointType, text: str, color):
        for index, char in enumerate(text):
            char_tile = tile_loader.get_tile(str_2_tile[char], color)
            screen.blit(char_tile, ((pos[0] + index) * tile_size[0],
                                    pos[1] * tile_size.y))

    def get_array_tile(pos: PointType, array: list[list]) -> pg.Surface | None:
        value = get_array(pos, array)
        if value:
            if isinstance(value, MobData):
                return tile_loader.get_tile(*mob_graphics[value.id])
            return tile_loader.get_tile(*tile_graphics[value])

    def move_player(direction: tuple[int, int]) -> Point:
        try_pos = Point(player_pos.x + direction[0], player_pos.y + direction[1])
        move_mob = get_array(try_pos, game_world.overworld_layer.mob_array)
        if move_mob:
            return player_pos
        move_tile = get_array(try_pos, game_world.overworld_layer.tile_array)
        if move_tile is None or TileTag.BLOCK_MOVE in tile_tags[move_tile]:
            return player_pos
        set_array(player_pos, game_world.overworld_layer.mob_array, 0)
        set_array(try_pos, game_world.overworld_layer.mob_array, MobData(MobID.PLAYER, 10))
        return try_pos

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
                elif event.key == pg.K_UP:
                    cursor_show = True
                    if player_dir == (0, -1):
                        player_pos = move_player((0, -1))
                    else:
                        player_dir = Point(0, -1)
                elif event.key == pg.K_DOWN:
                    cursor_show = True
                    if player_dir == (0, 1):
                        player_pos = move_player((0, 1))
                    else:
                        player_dir = Point(0, 1)
                elif event.key == pg.K_LEFT:
                    cursor_show = True
                    if player_dir == (-1, 0):
                        player_pos = move_player((-1, 0))
                    else:
                        player_dir = Point(-1, 0)
                elif event.key == pg.K_RIGHT:
                    cursor_show = True
                    if player_dir == (1, 0):
                        player_pos = move_player((1, 0))
                    else:
                        player_dir = Point(1, 0)

        # Update.
        clock.tick()

        if pg.time.get_ticks() - cursor_flash_timer >= CURSOR_FLASH_FREQ:
            cursor_flash_timer = pg.time.get_ticks()
            cursor_show = not cursor_show

        # Draw.
        screen.fill((0, 0, 0))

        # Display world.
        dx = 0
        for x in range(-player_vision, player_vision + 1):
            dy = 0
            for y in range(-player_vision, player_vision + 1):
                mob = get_array_tile((player_pos.x + x, player_pos.y + y),
                                     game_world.overworld_layer.mob_array)
                if mob:
                    screen.blit(mob, (dx * tile_size.x, dy * tile_size.y))
                else:
                    tile = get_array_tile((player_pos.x + x, player_pos.y + y),
                                          game_world.overworld_layer.tile_array)
                    if tile:
                        screen.blit(tile, (dx * tile_size.x, dy * tile_size.y))
                dy += 1
            dx += 1

        # Draw facing cursor.
        if cursor_show:
            screen.blit(cursor_img, ((17 + player_dir.x) * tile_size.x,
                                     (17 + player_dir.y) * tile_size.y))

        # Draw UI.
        write_text((35, 0), "life", Colors.WHITE.value)
        for i in range(10):
            tile = heart_empty_img if i >= player_health else heart_full_img
            screen.blit(tile, ((40 + i) * tile_size[0], 0))
        write_text((35, 1), "stam", Colors.WHITE.value)
        for i in range(10):
            tile = stam_empty_img if i >= player_stamina else stam_full_img
            screen.blit(tile, ((40 + i) * tile_size[0], tile_size[1]))

        # Display FPS.
        fps_surf = font.render(str(clock.get_fps()), True, (255, 255, 255))
        screen.blit(fps_surf, (0, screen.get_height() - fps_surf.get_height()))
        # Flip display.
        pg.display.flip()


if __name__ == "__main__":
    main()
