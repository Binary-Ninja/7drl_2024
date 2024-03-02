#!/usr/bin/env python3
import sys
from pathlib import Path
import random
from collections import deque
from enum import Enum, auto

import pygame as pg

from tileloader import TileLoader
from world import World, set_array, get_array
from data import Point, str_2_tile, PointType, Graphic, Color
from items import Item, ItemID
from tiles import TileTag
from mobs import Mob, MobID, MobTag


class GameMode(Enum):
    MOVE = auto()
    INVENTORY = auto()
    CRAFT = auto()


NO_ITEM = "no item"


def main():
    pg.init()

    screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("7DRL 2024")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 20)

    tile_size = Point(16, 16)
    tile_loader = TileLoader(Path() / "kenney_tileset.png", tile_size)
    heart_full_img = tile_loader.get_tile(Graphic.HEART_FULL, Color.RED)
    heart_empty_img = tile_loader.get_tile(Graphic.HEART_EMPTY, Color.DARK_RED)
    stam_full_img = tile_loader.get_tile(Graphic.STAM_FULL, Color.YELLOW)
    stam_empty_img = tile_loader.get_tile(Graphic.STAM_EMPTY, Color.DARK_YELLOW)
    cursor_img = tile_loader.get_tile(Graphic.CURSOR, Color.WHITE)
    cursor_img2 = tile_loader.get_tile(Graphic.CURSOR2, Color.WHITE)

    cursor_flash_timer = pg.time.get_ticks()
    CURSOR_FLASH_FREQ = 500
    cursor_show = True
    cursor_index = 0  # what inventory item it is on

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
    set_array(player_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))

    current_item: Item | NO_ITEM = NO_ITEM
    inventory: list[Item] = [Item(ItemID.PICKUP), Item(ItemID.WORKBENCH),
                             Item(ItemID.DIRT, 23), Item(ItemID.SAND, 2),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             Item(ItemID.WOOD, 99), Item(ItemID.STONE, 100),
                             ]

    message_logs: deque[str] = deque(maxlen=10)
    message_logs.appendleft("arrow keys to")
    message_logs.appendleft("move player or")
    message_logs.appendleft("cursor")
    message_logs.appendleft("c key to use")
    message_logs.appendleft("item or select")
    message_logs.appendleft("x key to open")
    message_logs.appendleft("inventory or")
    message_logs.appendleft("interact")
    message_logs.appendleft("z key to wait")
    message_logs.appendleft("or use stairs")

    game_mode = GameMode.MOVE

    current_crafter = None  # the current crafting station in use
    crafting_list = None  # the list of recipies

    def spawn_mob(pos: PointType, mob_id: MobID):
        set_array(pos, game_world.overworld_layer.mob_array, Mob(mob_id))

    # add some test mobs
    spawn_mob((48, 48), MobID.WORKBENCH)
    for _ in range(10):
        spawn_mob((_ * 2, 0), MobID.GREEN_ZOMBIE)
        spawn_mob((_ * 2, 2), MobID.GREEN_SLIME)
        spawn_mob((_ * 2, 4), MobID.GREEN_SKELETON)
        spawn_mob((_ * 2, 6), MobID.AIR_WIZARD)

    def write_text(pos: PointType, text: str, color: tuple[int, int, int]):
        for index, char in enumerate(text):
            char_tile = tile_loader.get_tile(str_2_tile[char], color)
            screen.blit(char_tile, ((pos[0] + index) * tile_size[0],
                                    pos[1] * tile_size.y))

    def get_array_tile(pos: PointType, array: list[list]) -> pg.Surface | None:
        value = get_array(pos, array)
        if value:
            return tile_loader.get_tile(*value.graphic)

    def move_player(direction: tuple[int, int]) -> Point:
        try_pos = Point(player_pos.x + direction[0], player_pos.y + direction[1])
        move_mob = get_array(try_pos, game_world.overworld_layer.mob_array)
        if move_mob:
            if move_mob.has_tag(MobTag.PUSHABLE):
                try_space = Point(try_pos.x + direction[0], try_pos.y + direction[1])
                # check for mob collisions, then tile collisions
                try_mob = get_array(try_space, game_world.overworld_layer.mob_array)
                # there is no mob or we are out of bounds
                if not try_mob:
                    try_tile = get_array(try_space, game_world.overworld_layer.tile_array)
                    # If it isn't the void and doesn't block movement.
                    if try_tile is not None and not try_tile.has_tag(TileTag.BLOCK_MOVE):
                        set_array(try_space, game_world.overworld_layer.mob_array, move_mob)
                        set_array(try_pos, game_world.overworld_layer.mob_array, None)
                        message_logs.appendleft("you push the")
                        message_logs.appendleft(f"{move_mob.name}")
                    else:
                        message_logs.appendleft("you bump into")
                        message_logs.appendleft(f"the {move_mob.name}")
                else:
                    message_logs.appendleft("you bump into")
                    message_logs.appendleft(f"the {move_mob.name}")
            else:
                message_logs.appendleft("you bump into")
                message_logs.appendleft(f"the {move_mob.name}")
            return player_pos
        move_tile = get_array(try_pos, game_world.overworld_layer.tile_array)
        if move_tile is None or move_tile.has_tag(TileTag.BLOCK_MOVE):
            message_logs.appendleft("you bump into")
            if move_tile is None:
                message_logs.appendleft("the void")
            else:
                message_logs.appendleft(f"the {move_tile.name}")
            return player_pos
        set_array(player_pos, game_world.overworld_layer.mob_array, None)
        set_array(try_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))
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
                    if game_mode is GameMode.MOVE:
                        if player_dir == (0, -1):
                            player_pos = move_player((0, -1))
                        else:
                            player_dir = Point(0, -1)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index -= 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index -= 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_DOWN:
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (0, 1):
                            player_pos = move_player((0, 1))
                        else:
                            player_dir = Point(0, 1)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index += 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index += 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_LEFT:
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (-1, 0):
                            player_pos = move_player((-1, 0))
                        else:
                            player_dir = Point(-1, 0)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index -= 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index -= 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_RIGHT:
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (1, 0):
                            player_pos = move_player((1, 0))
                        else:
                            player_dir = Point(1, 0)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index += 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index += 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_c:
                    if game_mode is GameMode.MOVE:
                        pass  # TODO: use current item
                    elif game_mode is GameMode.INVENTORY:
                        item = inventory.pop(cursor_index)
                        if current_item != NO_ITEM:
                            inventory.insert(0, current_item)
                        current_item = item
                        cursor_index = 0
                        game_mode = GameMode.MOVE
                    else:
                        pass  # TODO: craft
                elif event.key == pg.K_x:
                    if game_mode is GameMode.INVENTORY or game_mode is GameMode.CRAFT:
                        # Cancel crafting or inventory.
                        current_crafter = None
                        crafting_list = None
                        cursor_index = 0
                        game_mode = GameMode.MOVE
                    else:
                        # We must be in move mode.
                        target_pos = Point(player_pos.x + player_dir.x,
                                           player_pos.y + player_dir.y)
                        target_mob = get_array(target_pos,
                                               game_world.overworld_layer.mob_array)
                        if target_mob and target_mob.has_tag(MobTag.CRAFTING):
                            game_mode = GameMode.CRAFT
                            current_crafter = target_mob
                            crafting_list = current_crafter.recipies
                        else:
                            game_mode = GameMode.INVENTORY
                    print(game_mode)
                    print(current_crafter)
                    print(crafting_list)
                elif event.key == pg.K_z:
                    if game_mode is GameMode.MOVE:
                        pass  # TODO: wait mechanic
                    else:
                        cursor_index = 0  # reset cursor

        # Update.
        clock.tick()

        # Update animations.
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

        # Draw facing cursor or menu cursor.
        inventory_scroll = max(0, cursor_index - 15)
        crafting_scroll = max(0, cursor_index - 9)
        if cursor_show:
            if game_mode is GameMode.MOVE:
                screen.blit(cursor_img, ((17 + player_dir.x) * tile_size.x,
                                         (17 + player_dir.y) * tile_size.y))
            elif game_mode is GameMode.INVENTORY:
                screen.blit(cursor_img2,
                            (35 * tile_size.x,
                             (cursor_index - inventory_scroll + 7) * tile_size.y))
            else:  # crafting mode
                screen.blit(cursor_img2,
                            (35 * tile_size.x,
                             (cursor_index - crafting_scroll + 13) * tile_size.y))

        # Draw UI.
        # Draw HP & Stamina.
        write_text((35, 0), "life", Color.WHITE)
        for i in range(10):
            tile = heart_empty_img if i >= player_health else heart_full_img
            screen.blit(tile, ((40 + i) * tile_size.x, 0))
        write_text((35, 1), "stam", Color.WHITE)
        for i in range(10):
            tile = stam_empty_img if i >= player_stamina else stam_full_img
            screen.blit(tile, ((40 + i) * tile_size.x, tile_size.y))

        # Draw current item and inventory.
        if game_mode is not GameMode.CRAFT:
            write_text((35, 3), "current item", Color.WHITE)
            if current_item != NO_ITEM:
                tile = tile_loader.get_tile(*current_item.graphic)
                screen.blit(tile, (36 * tile_size.x, 4 * tile_size.y))
            write_text((38, 4), str(current_item), Color.LIGHT_GRAY)
        else:
            write_text((35, 3), "current recipie", Color.WHITE)
            ingredients = crafting_list[cursor_index]
            for index, ingredient in enumerate(ingredients):
                if index == 0:
                    continue  # this is the result of the recipie
                item = Item(*ingredient)
                tile = tile_loader.get_tile(*item.graphic)
                screen.blit(tile, (36 * tile_size.x, (3 + index) * tile_size.y))
                write_text((38, 3 + index), str(item), Color.LIGHT_GRAY)

        if game_mode is not GameMode.CRAFT:
            write_text((35, 6), f"inventory {len(inventory)}", Color.WHITE)
            for index in range(16):
                real_index = index + inventory_scroll
                if real_index >= len(inventory):
                    break
                item = inventory[real_index]
                if game_mode is GameMode.INVENTORY:
                    color = Color.WHITE if real_index == cursor_index else Color.LIGHT_GRAY
                else:
                    color = Color.LIGHT_GRAY
                tile = tile_loader.get_tile(*item.graphic)
                screen.blit(tile, (36 * tile_size.x, (7 + index) * tile_size.y))
                write_text((38, 7 + index), str(item), color)
        else:
            write_text((35, 12), f"{current_crafter.name}", Color.WHITE)
            for index in range(10):
                real_index = index + crafting_scroll
                if real_index >= len(crafting_list):
                    break
                result = Item(*crafting_list[real_index][0])
                color = Color.WHITE if real_index == cursor_index else Color.LIGHT_GRAY
                tile = tile_loader.get_tile(*result.graphic)
                screen.blit(tile, (36 * tile_size.x, (13 + index) * tile_size.y))
                write_text((38, 13 + index), str(result), color)

        # Draw message logs.
        write_text((37, 24), "message log", Color.WHITE)
        for i, message in enumerate(message_logs):
            color = Color.LIGHT_GRAY if i > 1 else Color.WHITE
            write_text((35, 34 - i), message, color)

        # Display FPS.
        fps_surf = font.render(str(clock.get_fps()), True, (255, 255, 255))
        screen.blit(fps_surf, (0, screen.get_height() - fps_surf.get_height()))
        # Flip display.
        pg.display.flip()


if __name__ == "__main__":
    main()
