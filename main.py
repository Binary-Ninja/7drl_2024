#!/usr/bin/env python3
import math
import sys
from pathlib import Path
import random
from collections import deque
from enum import Enum, auto
from typing import Sequence

import pygame as pg

from tileloader import TileLoader
from world import World, set_array, get_array, make_2d_array
from data import (Point, str_2_tile, PointType, Graphic, Color, ItemID, ItemTag,
                  TileTag, MobID, MobTag)
from items import Item, item_to_mob, item_light
from mobs import Mob, mob_damage
from tiles import Tile, tile_replace, tile_damage, TileID, tile_grow, tile_spread, tile_light, tile_drain
from loots import tile_break_loot, resolve_loot, mob_death_loot, fishing_loot


def distance_within(a: PointType, b: PointType, dist: int | float) -> bool:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 <= dist ** 2


def distance_squared(a: PointType, b: PointType) -> float | int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


class GameMode(Enum):
    MOVE = auto()
    INVENTORY = auto()
    CRAFT = auto()


NO_ITEM = Item(ItemID.EMPTY_HANDS)

MOB_SIM_DISTANCE = 25
MAX_VIEW_DIST = 25
CHASE_DISTANCE = 10  # when zombies sense you
JUMP_DISTANCE = 8  # when slimes sense you
SKELETON_SHOOT_RADIUS = 5
SKELETON_SIGHT_RADIUS = 12  # when skeletons sense you
SPIDER_CHASE_RADIUS = 10  # when spiders sense you
SHADE_FLEE_RADIUS = 5  # when shades see you
DOG_FOLLOW_RADIUS = 12
CURSOR_FLASH_FREQ = 500
STAM_FLASH_FREQ = 200

player_vision = 17
player_light_radius = 2.5
player_health = 10
player_stamina = 10
regen_stam = True
do_calc_light_map = True
light_map: list[list[bool]] = []
path_to_player: dict[tuple, tuple] = {}

tile_size = Point(16, 16)
tile_loader = TileLoader(Path() / "kenney_tileset.png", tile_size)


def main_menu(screen) -> dict:
    options = {"size": (100, 100), "day_cycle_len": 500, "mob_spawn": 0.2}
    start_game = False
    clock = pg.time.Clock()

    cursor_img = tile_loader.get_tile(Graphic.CURSOR2, Color.WHITE)
    cursor_flash_timer = pg.time.get_ticks()
    global CURSOR_FLASH_FREQ
    cursor_show = True
    cursor_index = 0

    menu_options = (
        (("world size - 75*75", (75, 75)), ("world size - 100*100", (100, 100)),
         ("world size - 150*150", (150, 150)), ("world size - 200*200", (200, 200))),
        (("day length - 200", 200), ("day length - 350", 350), ("day length - 500", 500), ("day length - 650", 650)),
        (("# of mob spawns - few", 0.05), ("# of mob spawns - some", 0.1),
         ("# of mob spawns - many", 0.2), ("# of mob spawns - annoying", 0.4)),
    )

    choice_index = [1, 2, 2]

    index_2_option = {0: "size", 1: "day_cycle_len", 2: "mob_spawn"}

    def write_text(pos: PointType, text: str, color: tuple[int, int, int]):
        for index, char in enumerate(text):
            char_tile = tile_loader.get_tile(str_2_tile[char], color)
            screen.blit(char_tile, ((pos[0] + index) * tile_size.x,
                                    pos[1] * tile_size.y))

    while not start_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_UP:
                    cursor_index -= 1
                    cursor_index %= len(menu_options)
                    cursor_show = True
                elif event.key == pg.K_DOWN:
                    cursor_index += 1
                    cursor_index %= len(menu_options)
                    cursor_show = True
                elif event.key == pg.K_LEFT:
                    choice_index[cursor_index] -= 1
                    choice_index[cursor_index] %= len(menu_options[cursor_index])
                    options[index_2_option[cursor_index]] = menu_options[cursor_index][choice_index[cursor_index]][1]
                elif event.key == pg.K_RIGHT:
                    choice_index[cursor_index] += 1
                    choice_index[cursor_index] %= len(menu_options[cursor_index])
                    options[index_2_option[cursor_index]] = menu_options[cursor_index][choice_index[cursor_index]][1]
                elif event.key == pg.K_c:
                    start_game = True
        # Update.
        clock.tick()

        # Cursor flash.
        if pg.time.get_ticks() - cursor_flash_timer >= CURSOR_FLASH_FREQ:
            cursor_flash_timer = pg.time.get_ticks()
            cursor_show = not cursor_show

        # Draw.
        screen.fill((0, 0, 0))

        # Draw the static text.
        write_text((0, 0), f"{'outlast 7drl 2024':^50}", Color.WHITE)
        write_text((0, 2), f"{'up and down arrow to select setting':^50}", Color.WHITE)
        write_text((0, 3), f"{'left and right arrow to cycle setting':^50}", Color.WHITE)
        write_text((0, 4), f"{'press c to generate new world':^50}", Color.WHITE)

        write_text((0, 22), f"{'credits':^50}", Color.WHITE)
        write_text((0, 23), f"{'sprites by kenney.nl':^50}", Color.LIGHT_GRAY)
        write_text((0, 24), f"{'sound effects by sfxr.me':^50}", Color.LIGHT_GRAY)
        write_text((0, 25), f"{'music':^50}", Color.LIGHT_GRAY)
        write_text((0, 26), f"{'inspired by minicraft by markus persson':^50}", Color.LIGHT_GRAY)
        write_text((0, 27), f"{'code by binary-ninja.itch.io':^50}", Color.LIGHT_GRAY)

        write_text((0, 29), f"{'controls':^50}", Color.WHITE)
        write_text((0, 30), f"{'arrow keys to navigate menus and move player':^50}", Color.LIGHT_GRAY)
        write_text((0, 31), f"{'c key to use current item or select menu option':^50}", Color.LIGHT_GRAY)
        write_text((0, 32), f"{'x key to open inventory or interact':^50}", Color.LIGHT_GRAY)
        write_text((0, 33), f"{'z key to advance the world time or use staircases':^50}", Color.LIGHT_GRAY)
        write_text((0, 34), f"{'escape key to quit the game and go to main menu':^50}", Color.LIGHT_GRAY)

        # Draw settings.
        for index, setting in enumerate(menu_options):
            color = Color.WHITE if index == cursor_index else Color.LIGHT_GRAY
            write_text((15, 8 + (index * 2)), setting[choice_index[index]][0], color)

        # Draw cursor.
        if cursor_show:
            screen.blit(cursor_img, (14 * tile_size.x, (8 + (cursor_index * 2)) * tile_size.y))

        # Flip display.
        pg.display.flip()
    return options


def main(screen, settings):

    clock = pg.time.Clock()
    font = pg.font.Font(None, 20)
    game_is_going = True

    global tile_size
    global tile_loader
    heart_full_img = tile_loader.get_tile(Graphic.HEART_FULL, Color.RED)
    heart_empty_img = tile_loader.get_tile(Graphic.HEART_EMPTY, Color.DARK_RED)
    stam_full_img = tile_loader.get_tile(Graphic.STAM_FULL, Color.YELLOW)
    stam_empty_img = tile_loader.get_tile(Graphic.STAM_EMPTY, Color.DARK_YELLOW)
    cursor_img = tile_loader.get_tile(Graphic.CURSOR, Color.WHITE)
    cursor_img2 = tile_loader.get_tile(Graphic.CURSOR2, Color.WHITE)

    cursor_flash_timer = pg.time.get_ticks()
    global CURSOR_FLASH_FREQ
    cursor_show = True

    stam_flash_timer = pg.time.get_ticks()
    global STAM_FLASH_FREQ
    stam_flash = True

    cursor_index = 0  # what inventory item it is on

    world_time = 0
    do_a_game_tick = False

    day_cycle_timer = world_time
    DAY_CYCLE_LENGTH = settings["day_cycle_len"]
    night_time = False
    level_is_dark = False
    number_of_mobs = 0  # TODO: dont forget to update this to load on layer load when i add world layers
    MOB_SPAWN_CHANCE = settings["mob_spawn"]
    MOB_DESPAWN_CHANCE = 0.05

    def write_text(pos: PointType, text: str, color: tuple[int, int, int]):
        for index, char in enumerate(text):
            char_tile = tile_loader.get_tile(str_2_tile[char], color)
            screen.blit(char_tile, ((pos[0] + index) * tile_size.x,
                                    pos[1] * tile_size.y))

    world_seed = random.getrandbits(64)
    # world_seed = 1234
    world_size = Point(*settings["size"])
    game_world = World(world_size, world_seed)

    for loading_text in game_world.generate_layers():
        # Make sure the player knows the game hasn't frozen.
        screen.fill((0, 0, 0))
        write_text((0, 35 // 2), f"{loading_text:^50}", Color.WHITE)
        # Call the events so the OS doesn't think we froze.
        pg.event.get()
        # Update display so changes are seen before mext world gen.
        pg.display.flip()

    current_layer_index = 1
    current_layer_key = {
        0: game_world.sky_layer,
        1: game_world.overworld_layer,
        2: game_world.cave_layer,
        3: game_world.cavern_layer,
        4: game_world.hell_layer,
    }
    current_layer = current_layer_key[current_layer_index]

    mob_spawn_per_layer = {
        0: (MobID.FAIRY, MobID.BLACK_ZOMBIE, MobID.BLACK_SLIME, MobID.BLACK_SKELETON),
        1: (MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON),
        2: (MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON,
            MobID.RED_ZOMBIE, MobID.RED_SLIME, MobID.RED_SKELETON, MobID.BAT,
            ),
        3: (MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON,
            MobID.RED_ZOMBIE, MobID.RED_SLIME, MobID.RED_SKELETON, MobID.BAT,
            MobID.WHITE_ZOMBIE, MobID.WHITE_SLIME, MobID.WHITE_SKELETON, MobID.SHADE,
            ),
        4: (MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON,
            MobID.RED_ZOMBIE, MobID.RED_SLIME, MobID.RED_SKELETON, MobID.BAT,
            MobID.WHITE_ZOMBIE, MobID.WHITE_SLIME, MobID.WHITE_SKELETON, MobID.SHADE,
            MobID.BLACK_ZOMBIE, MobID.BLACK_SLIME, MobID.BLACK_SKELETON, MobID.FLAME_SKULL,
            MobID.BAT, MobID.SHADE, MobID.FLAME_SKULL,
            ),
    }

    def count_mobs(given_array: list[list]) -> int:
        # this might actually be (y, x), but I don't care
        count = 0
        for x in range(len(given_array)):
            for y in range(len(given_array[0])):
                mob = given_array[x][y]
                if mob is None:
                    continue
                # Only count the hostile mobs.
                if mob.id in (MobID.BAT, MobID.SHADE, MobID.FLAME_SKULL, MobID.FAIRY, MobID.SPIDER, MobID.HELL_SPIDER,
                              MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON,
                              MobID.RED_ZOMBIE, MobID.RED_SLIME, MobID.RED_SKELETON,
                              MobID.WHITE_ZOMBIE, MobID.WHITE_SLIME, MobID.WHITE_SKELETON,
                              MobID.BLACK_ZOMBIE, MobID.BLACK_SLIME, MobID.BLACK_SKELETON,
                              ):
                    count += 1
        return count

    global do_calc_light_map
    global player_vision
    global path_to_player
    global light_map
    do_fov = True
    global player_health
    global player_stamina
    global regen_stam
    player_dir = Point(0, -1)
    player_pos = (0, 0)
    while player_pos == (0, 0):
        x_range = (18, world_size.x - 19)
        y_range = (18, world_size.y - 19)
        try_spawn = Point(random.randint(*x_range), random.randint(*y_range))
        try_tile = get_array(try_spawn, game_world.overworld_layer.tile_array)
        if try_tile.has_tag(TileTag.BLOCK_MOVE) or try_tile.has_tag(TileTag.LIQUID):
            continue
        player_pos = try_spawn
        set_array(player_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))
        break

    player_is_dead = False
    current_item: Item | NO_ITEM = NO_ITEM
    inventory: list[Item] = [Item(ItemID.WORKBENCH),
                             Item(ItemID.GEM_PICK), Item(ItemID.GEM_SWORD),
                             # Item(ItemID.GEM_SHOVEL, 1), Item(ItemID.SAND, 99),
                             # Item(ItemID.GEM_FISH_SPEAR, 1), Item(ItemID.BED, 1),
                             # Item(ItemID.WOOD, 100), Item(ItemID.OVEN, 1),
                             # # Item(ItemID.WINDOW, 100), Item(ItemID.STONE_WALL, 99),
                             # # Item(ItemID.WOOD_DOOR, 100), Item(ItemID.WHEAT_SEEDS, 99),
                             # Item(ItemID.PIG_EGG, 100), Item(ItemID.GEM_LANTERN, 1),
                             ]

    message_logs: deque[str] = deque(maxlen=10)
    message_logs.appendleft("escape to quit")
    message_logs.appendleft("arrow keys to")
    message_logs.appendleft("navigate")
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

    just_broken_a_tile = False
    displayed_empty_hands_message = False
    just_placed_a_tile = False
    displayed_no_use_message = False
    skelly_got_em = False

    def line_of_sight(start: PointType, end: PointType) -> bool:
        start, end = Point(*start), Point(*end)
        dx, dy = end.x - start.x, end.y - start.y
        nx, ny = math.fabs(dx), math.fabs(dy)
        sign_x, sign_y = 1 if dx > 0 else -1, 1 if dy > 0 else -1

        p = pg.Vector2(*start)
        ix = iy = 0

        while ix < nx - 1 or iy < ny - 1:
            if (1 + 2 * ix) * ny < (1 + 2 * iy) * nx:
                p.x += sign_x
                ix += 1
            else:
                p.y += sign_y
                iy += 1
            tile = get_array((int(p.x), int(p.y)), current_layer.tile_array)
            if tile is None or tile.has_tag(TileTag.BLOCK_SIGHT):
                return False
        return True

    def calc_fov(start: Point, radius: int, master=None) -> list[list[bool]]:
        fov_field = make_2d_array((radius * 2 + 1, radius * 2 + 1), False)
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                real_pos = Point(start.x + x, start.y + y)
                if radius == 1:
                    if master is not None:
                        set_array((real_pos.x, real_pos.y), master, True)
                    else:
                        fov_field[x][y] = True
                elif distance_within(start, real_pos, radius + 0.5):
                    if master is not None:
                        if line_of_sight(start, real_pos):
                            set_array(real_pos, master, True)
                    else:
                        fov_field[x][y] = line_of_sight(start, real_pos)
        return fov_field

    fov_field = calc_fov(player_pos, MAX_VIEW_DIST)

    def calc_lightmap():
        global light_map
        light_map = make_2d_array(world_size, False)
        for x in range(world_size.x):
            for y in range(world_size.y):
                light_mob = current_layer.mob_array[x][y]
                if light_mob and light_mob.light > 0:
                    calc_fov(Point(x, y), light_mob.light, light_map)
                light_tile = current_layer.tile_array[x][y]
                if light_tile.has_tag(TileTag.LIGHT):
                    calc_fov(Point(x, y), tile_light[light_tile.id], light_map)

    def reduce_stamina(amount: int) -> bool:
        global player_stamina, regen_stam
        if player_stamina - amount < 0:
            return False
        else:
            player_stamina -= amount
            regen_stam = False
            return True

    def add_to_inventory(item: Item, invent: list[Item]) -> None:
        if item.has_tag(ItemTag.STACKABLE):
            for invent_item in invent:
                if invent_item.id is item.id:
                    invent_item.count += item.count
                    break
            else:
                invent.insert(0, item)
        else:
            invent.insert(0, item)

    def remove_from_inventory(item: tuple[ItemID, int], invent: list[Item]) -> Item | None:
        for index, invent_item in enumerate(invent):
            if invent_item.id is item[0]:
                if not invent_item.has_tag(ItemTag.STACKABLE):
                    return invent.pop(index)
                else:
                    invent_item.count -= item[1]
                    if invent_item.count <= 0:
                        return invent.pop(index)
                    return

    def craftable(needed: Sequence[tuple[ItemID, int]],
                  have: list[Item]) -> bool:
        for item_id, count in needed:
            for item in have:
                if item.id is item_id and item.count >= count:
                    break
            else:
                return False
        return True

    def get_array_tile(pos: PointType, array: list[list], dark: bool = False) -> pg.Surface | None:
        value = get_array(pos, array)
        if value:
            tile, color = value.graphic
            if dark:
                color = tuple(pg.Color(color).lerp((0, 0, 0), 0.75))
            return tile_loader.get_tile(tile, color)

    def move_player(direction: tuple[int, int]) -> Point:
        global player_health, light_map, player_stamina, regen_stam, do_calc_light_map
        swapped = False
        try_pos = Point(player_pos.x + direction[0], player_pos.y + direction[1])
        move_mob = get_array(try_pos, current_layer.mob_array)
        if move_mob:
            if move_mob.has_tag(MobTag.PUSHABLE):
                try_space = Point(try_pos.x + direction[0], try_pos.y + direction[1])
                # check for mob collisions, then tile collisions
                try_mob = get_array(try_space, current_layer.mob_array)
                # there is no mob or we are out of bounds
                if not try_mob:
                    try_tile = get_array(try_space, current_layer.tile_array)
                    # If it isn't the void and doesn't block movement.
                    if try_tile is not None and not try_tile.has_tag(TileTag.BLOCK_MOVE):
                        message_logs.appendleft("you push the")
                        message_logs.appendleft(f"{move_mob.name}")
                        set_array(try_pos, current_layer.mob_array, None)
                        if try_tile.has_tag(TileTag.LIQUID):
                            message_logs.appendleft("it sinks into")
                            message_logs.appendleft(f"the {try_tile.name}")
                        else:
                            set_array(try_space,
                                      current_layer.mob_array, move_mob)
                            if try_tile.has_tag(TileTag.CRUSH):
                                set_array(try_space, current_layer.tile_array,
                                          Tile(tile_replace[try_tile.id]))
                                message_logs.appendleft("it crushes the")
                                message_logs.appendleft(f"{try_tile.name}")
                        if move_mob.light > 0:
                            do_calc_light_map = True
                    else:
                        message_logs.appendleft("you bump into")
                        message_logs.appendleft(f"the {move_mob.name}")
                else:
                    message_logs.appendleft("you bump into")
                    message_logs.appendleft(f"the {move_mob.name}")
            elif move_mob.has_tag(MobTag.SWAPPABLE):
                swapped = True
                try_tile = get_array(try_pos, current_layer.tile_array)
                player_tile = get_array(player_pos, current_layer.tile_array)
                set_array(try_pos, current_layer.mob_array, Mob(MobID.PLAYER))
                message_logs.appendleft("you swap places")
                message_logs.appendleft(f"with {move_mob.name}")
                if try_tile.has_tag(TileTag.CRUSH):
                    set_array(try_pos, current_layer.tile_array,
                              Tile(tile_replace[try_tile.id]))
                    message_logs.appendleft("you crush the")
                    message_logs.appendleft(f"{try_tile.name}")
                if player_tile.id != TileID.LAVA:
                    set_array(player_pos, current_layer.mob_array, move_mob)
                else:
                    message_logs.appendleft(f"{move_mob.name} sinks")
                    message_logs.appendleft("into the lava")
                    set_array(player_pos, current_layer.mob_array, None)
            else:
                message_logs.appendleft("you bump into")
                message_logs.appendleft(f"the {move_mob.name}")
            if not swapped:
                return player_pos
            else:
                return try_pos
        move_tile = get_array(try_pos, current_layer.tile_array)
        if move_tile is None:
            message_logs.appendleft("you stare into")
            message_logs.appendleft("the abyss")
            return player_pos
        if move_tile.id == TileID.AIR:
            message_logs.appendleft("you teeter on")
            message_logs.appendleft("the clouds edge")
            return player_pos
        damage = tile_damage[move_tile.id]
        drain = tile_drain[move_tile.id]
        if move_tile.has_tag(TileTag.BLOCK_MOVE):
            message_logs.appendleft("you bump into")
            message_logs.appendleft(f"the {move_tile.name}")
            if move_tile.has_tag(TileTag.DAMAGE):
                message_logs.appendleft("it hurts you")
                message_logs.appendleft(f"for -{damage}H")
                player_health -= damage
                player_health = max(0, player_health)
            if move_tile.has_tag(TileTag.DRAIN):
                message_logs.appendleft("it drains your")
                message_logs.appendleft(f"stamina -{drain}S")
                player_stamina -= drain
                player_stamina = max(0, player_stamina)
                regen_stam = False
            return player_pos
        if move_tile.has_tag(TileTag.DAMAGE):
            message_logs.appendleft(f"the {move_tile.name}")
            message_logs.appendleft(f"hurts you -{damage}H")
            player_health -= damage
            player_health = max(0, player_health)
        if move_tile.has_tag(TileTag.DRAIN):
            message_logs.appendleft(f"the {move_tile.name}")
            message_logs.appendleft(f"slows you -{drain}S")
            player_stamina -= drain
            player_stamina = max(0, player_stamina)
            regen_stam = False
        if move_tile.has_tag(TileTag.LIQUID):
            player_stamina -= 1
            if player_stamina <= 0:
                player_health -= 1
                player_health = max(0, player_health)
                message_logs.appendleft("you are sinking")
                message_logs.appendleft(f"in {move_tile.name} -1H")
            player_stamina = max(0, player_stamina)
            regen_stam = False
        if move_tile.has_tag(TileTag.CRUSH):
            set_array(try_pos, current_layer.tile_array, Tile(tile_replace[move_tile.id]))
            for item in resolve_loot(tile_break_loot[move_tile.id]):
                add_to_inventory(item, inventory)
                message_logs.appendleft("you crush the")
                message_logs.appendleft(f"{move_tile.name}")
        set_array(player_pos, current_layer.mob_array, None)
        set_array(try_pos, current_layer.mob_array, Mob(MobID.PLAYER))
        return try_pos

    while game_is_going:
        # Handle events.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    game_is_going = False
                elif event.key == pg.K_SPACE:
                    level_is_dark = not level_is_dark
                elif event.key == pg.K_f:
                    do_fov = not do_fov
                elif event.key == pg.K_w:
                    player_health = 10
                    player_stamina = 10
                elif event.key == pg.K_UP:
                    if player_is_dead:
                        continue
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (0, -1):
                            do_a_game_tick = True
                            player_pos = move_player((0, -1))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            player_dir = Point(0, -1)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index -= 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index -= 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_DOWN:
                    if player_is_dead:
                        continue
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (0, 1):
                            do_a_game_tick = True
                            player_pos = move_player((0, 1))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            player_dir = Point(0, 1)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index += 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index += 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_LEFT:
                    if player_is_dead:
                        continue
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (-1, 0):
                            do_a_game_tick = True
                            player_pos = move_player((-1, 0))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            player_dir = Point(-1, 0)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index -= 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index -= 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_RIGHT:
                    if player_is_dead:
                        continue
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (1, 0):
                            do_a_game_tick = True
                            player_pos = move_player((1, 0))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            player_dir = Point(1, 0)
                    elif game_mode is GameMode.INVENTORY:
                        cursor_index += 1
                        cursor_index %= len(inventory)
                    else:
                        cursor_index += 1
                        cursor_index %= len(crafting_list)
                elif event.key == pg.K_c:
                    if player_is_dead:
                        game_is_going = False
                        continue
                    if game_mode is GameMode.MOVE:
                        do_a_game_tick = True
                        target_pos = Point(player_pos.x + player_dir.x,
                                           player_pos.y + player_dir.y)
                        target_mob = get_array(target_pos,
                                               current_layer.mob_array)
                        target_tile = get_array(target_pos,
                                                current_layer.tile_array)
                        if current_item.tags == (ItemTag.STACKABLE,):
                            message_logs.appendleft("you cannot use")
                            message_logs.appendleft(f"the {current_item.name}")
                        if current_item is NO_ITEM and target_mob is None and \
                                target_tile.id not in current_item.data["breakable"]:
                            message_logs.appendleft("your hands are")
                            message_logs.appendleft("empty")
                            displayed_empty_hands_message = True
                        if current_item.has_tag(ItemTag.SPAWN_MOB):
                            # if there is no mob, spawn one in
                            mob = Mob(current_item.data["mobid"])
                            if target_mob is None and \
                                    not target_tile.has_tag(TileTag.BLOCK_MOVE) and \
                                    not target_tile.has_tag(TileTag.LIQUID):
                                if reduce_stamina(1):
                                    set_array(target_pos,
                                              current_layer.mob_array, mob)
                                    current_item.count -= 1
                                    if current_item.count <= 0:
                                        current_item = NO_ITEM
                                        inventory.remove(NO_ITEM)
                                        displayed_empty_hands_message = True
                                    message_logs.appendleft("you place the")
                                    message_logs.appendleft(f"{mob.name}")
                                    if mob.light > 0:
                                        do_calc_light_map = True
                                else:
                                    message_logs.appendleft("you do not have")
                                    message_logs.appendleft("the stamina")
                            else:
                                message_logs.appendleft("you cannot put")
                                message_logs.appendleft(f"{mob.name} here")
                        if current_item.has_tag(ItemTag.PICKUP):
                            if target_mob is not None:
                                item = item_to_mob[target_mob.id]
                                if item is not None:
                                    if reduce_stamina(1):
                                        item = Item(item)
                                        add_to_inventory(current_item, inventory)
                                        current_item = item
                                        set_array(target_pos,
                                                  current_layer.mob_array,
                                                  None)
                                        message_logs.appendleft("you pick up the")
                                        message_logs.appendleft(f"{item.name}")
                                        if target_mob.light > 0:
                                            do_calc_light_map = True
                                    else:
                                        message_logs.appendleft("you do not have")
                                        message_logs.appendleft("the stamina")
                        if current_item.has_tag(ItemTag.HEAL):
                            if player_health < 10:
                                if reduce_stamina(current_item.data["stamina_cost"]):
                                    prev_ph = player_health
                                    player_health += current_item.data["heal"]
                                    player_health = min(10, player_health)
                                    player_health = max(0, player_health)
                                    current_item.count -= 1
                                    message_logs.appendleft("you eat the")
                                    if player_health - prev_ph >= 0:
                                        message_logs.appendleft(f"{current_item.name} "
                                                                f"+{player_health - prev_ph}H")
                                    else:
                                        message_logs.appendleft(f"{current_item.name} -{player_health - prev_ph}H")
                                    if current_item.count <= 0:
                                        current_item = NO_ITEM
                                        inventory.remove(NO_ITEM)
                                        displayed_empty_hands_message = True
                                else:
                                    message_logs.appendleft("you do not have")
                                    message_logs.appendleft("the stamina")
                            else:
                                message_logs.appendleft("you have full")
                                message_logs.appendleft("health points")
                        if current_item.has_tag(ItemTag.STAMINA):
                            if player_stamina < 10:
                                prev_ps = player_stamina
                                player_stamina += current_item.data["stamina"]
                                player_stamina = min(10, player_stamina)
                                current_item.count -= 1
                                message_logs.appendleft("you eat the")
                                message_logs.appendleft(f"{current_item.name} "
                                                        f"+{player_stamina - prev_ps}S")
                                if current_item.count <= 0:
                                    current_item = NO_ITEM
                                    inventory.remove(NO_ITEM)
                                    displayed_empty_hands_message = True
                            else:
                                message_logs.appendleft("you have full")
                                message_logs.appendleft("stamina points")
                        if current_item.has_tag(ItemTag.PLACE_TILE):
                            if target_tile is not None and \
                                    target_tile.id in current_item.data["base"]:
                                stam_reduce = 1 if current_item.has_tag(ItemTag.STACKABLE)\
                                    else current_item.data["stamina_cost"]
                                if reduce_stamina(stam_reduce):
                                    just_placed_a_tile = True
                                    tile = Tile(current_item.data["place"])
                                    set_array(target_pos,
                                              current_layer.tile_array, tile)
                                    fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                    if tile.has_tag(TileTag.BLOCK_SIGHT) ^ target_tile.has_tag(TileTag.BLOCK_SIGHT):
                                        do_calc_light_map = True
                                    if not current_item.has_tag(ItemTag.STACKABLE):
                                        message_logs.appendleft("you use the")
                                        message_logs.appendleft(f"{current_item.name}")
                                    else:
                                        message_logs.appendleft("you place the")
                                        message_logs.appendleft(f"{current_item.name}")
                                    current_item.count -= 1
                                    if not current_item.has_tag(ItemTag.STACKABLE):
                                        current_item.count = 1
                                    if current_item.count <= 0:
                                        current_item = NO_ITEM
                                        inventory.remove(NO_ITEM)
                                        displayed_empty_hands_message = True
                                else:
                                    displayed_no_use_message = True
                                    message_logs.appendleft("you do not have")
                                    message_logs.appendleft("the stamina")
                            else:
                                displayed_no_use_message = True
                                if current_item.has_tag(ItemTag.STACKABLE):
                                    message_logs.appendleft("you cannot put")
                                    message_logs.appendleft(f"{current_item.name} here")
                                else:
                                    message_logs.appendleft("you cannot use")
                                    message_logs.appendleft(f"{current_item.name} here")
                                if current_item.has_tag(ItemTag.BREAK_TILE) and target_tile is not None and\
                                    target_tile.id in current_item.data["breakable"]:
                                    displayed_no_use_message = False
                                    message_logs.popleft()
                                    message_logs.popleft()
                        if current_item.has_tag(ItemTag.BREAK_TILE):
                            if not (current_item.has_tag(ItemTag.DAMAGE_MOBS) and target_mob) and \
                                    not just_placed_a_tile and not displayed_no_use_message:
                                if target_tile is not None:
                                    if target_tile.id in current_item.data["breakable"]:
                                        stam_cost = current_item.data["stamina_cost"]
                                        if reduce_stamina(stam_cost):
                                            damage = current_item.data["tile_damage"]
                                            target_tile.health -= damage
                                            if target_tile.health > 0:
                                                message_logs.appendleft("you strike the")
                                                message_logs.appendleft(f"{target_tile.name} "
                                                                        f"{target_tile.health}/"
                                                                        f"{target_tile.max_health}")
                                            else:
                                                tile = Tile(tile_replace[target_tile.id])
                                                loot = resolve_loot(
                                                    tile_break_loot[target_tile.id])
                                                set_array(target_pos,
                                                          current_layer.tile_array, tile)
                                                fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                                if tile.has_tag(TileTag.BLOCK_SIGHT) ^ \
                                                        target_tile.has_tag(TileTag.BLOCK_SIGHT):
                                                    do_calc_light_map = True
                                                for item in loot:
                                                    add_to_inventory(item, inventory)
                                                message_logs.appendleft("you remove the")
                                                message_logs.appendleft(f"{target_tile.name}")
                                            just_broken_a_tile = True
                                        else:
                                            message_logs.appendleft("you do not have")
                                            message_logs.appendleft("the stamina")
                                    elif displayed_empty_hands_message is False and not \
                                            current_item.has_tag(ItemTag.DAMAGE_MOBS):
                                        message_logs.appendleft("you cannot use")
                                        message_logs.appendleft(f"{current_item.name}")
                                else:
                                    message_logs.appendleft("the unfeeling")
                                    message_logs.appendleft("void mocks you")
                        if current_item.has_tag(ItemTag.DAMAGE_MOBS):
                            if not just_broken_a_tile:
                                if target_mob is not None and not target_mob.has_tag(MobTag.CRAFTING):
                                    stam_cost = current_item.data["stamina_cost"]
                                    if reduce_stamina(stam_cost):
                                        damage = current_item.data["mob_damage"]
                                        target_mob.health -= damage
                                        if target_mob.health <= 0:
                                            set_array(target_pos,
                                                      current_layer.mob_array,
                                                      None)
                                            if target_mob.light > 0:
                                                do_calc_light_map = True
                                            loot = resolve_loot(mob_death_loot[target_mob.id])
                                            for item in loot:
                                                add_to_inventory(item, inventory)
                                            message_logs.appendleft("you kill the")
                                            message_logs.appendleft(f"{target_mob.name}")
                                        else:
                                            message_logs.appendleft("you strike the")
                                            message_logs.appendleft(f"{target_mob.name} "
                                                                    f"{target_mob.health}/{target_mob.max_health}")
                                    else:
                                        message_logs.appendleft("you do not have")
                                        message_logs.appendleft("the stamina")
                                elif displayed_empty_hands_message is False:
                                    message_logs.appendleft("you strike at")
                                    message_logs.appendleft("air uselessly")
                        if current_item.has_tag(ItemTag.FISH):
                            if target_tile is not None and target_tile.id in current_item.data["fishable"]:
                                if reduce_stamina(current_item.data["stamina_cost"]):
                                    if random.random() < current_item.data["fish_chance"]:
                                        loot = Item(random.choice(fishing_loot[target_tile.id]).id)
                                        add_to_inventory(loot, inventory)
                                        message_logs.appendleft("you fish and")
                                        message_logs.appendleft(f"catch {loot.name}")
                                    else:
                                        message_logs.appendleft("you fish and")
                                        message_logs.appendleft("catch nothing")
                                else:
                                    message_logs.appendleft("you do not have")
                                    message_logs.appendleft("the stamina")
                            else:
                                message_logs.appendleft("you cannot fish")
                                message_logs.appendleft(f"in {target_tile.name}")
                        just_broken_a_tile = False
                        displayed_empty_hands_message = False
                        displayed_no_use_message = False
                        just_placed_a_tile = False
                    elif game_mode is GameMode.INVENTORY:
                        item = inventory.pop(cursor_index)
                        add_to_inventory(current_item, inventory)
                        current_item = item
                        # back to move mode
                        cursor_index = 0
                        game_mode = GameMode.MOVE
                    else:
                        ingredients = crafting_list[cursor_index][1:]
                        if craftable(ingredients, inventory):
                            # remove ingredients
                            for needed_item in ingredients:
                                remove_from_inventory(needed_item, inventory)
                            # add the result item
                            item = Item(*crafting_list[cursor_index][0])
                            add_to_inventory(item, inventory)
                            # alert the player that it worked
                            message_logs.appendleft("you crafted")
                            message_logs.appendleft(f"{item}")
                elif event.key == pg.K_x:
                    if player_is_dead:
                        continue
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
                                               current_layer.mob_array)
                        target_tile = get_array(target_pos,
                                                current_layer.tile_array)
                        if target_mob and target_mob.has_tag(MobTag.CRAFTING):
                            game_mode = GameMode.CRAFT
                            current_crafter = target_mob
                            crafting_list = current_crafter.recipies
                            message_logs.appendleft("you craft with")
                            message_logs.appendleft(f"the {current_crafter.name}")
                        elif target_mob and target_mob.has_tag(MobTag.BED):
                            if night_time:
                                night_time = False
                                level_is_dark = False
                                day_cycle_timer = world_time
                                message_logs.appendleft("you sleep the")
                                message_logs.appendleft("night away")
                            else:
                                message_logs.appendleft("you cannot rest")
                                message_logs.appendleft("during the day")
                        elif target_tile and target_tile.id in (TileID.OPEN_WOOD_DOOR,
                                                                TileID.CLOSED_WOOD_DOOR):
                            if target_tile.id is TileID.CLOSED_WOOD_DOOR:
                                set_array(target_pos,
                                          current_layer.tile_array,
                                          Tile(TileID.OPEN_WOOD_DOOR))
                                message_logs.appendleft("you open the")
                                message_logs.appendleft(f"{target_tile.name}")
                            else:
                                set_array(target_pos,
                                          current_layer.tile_array,
                                          Tile(TileID.CLOSED_WOOD_DOOR))
                                message_logs.appendleft("you close the")
                                message_logs.appendleft(f"{target_tile.name}")
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            game_mode = GameMode.INVENTORY
                elif event.key == pg.K_z:
                    if player_is_dead:
                        continue
                    if game_mode is GameMode.MOVE:
                        current_tile = get_array(player_pos, current_layer.tile_array)
                        if current_tile.has_tag(TileTag.DOWN_STAIRS):
                            current_layer_index += 1
                            assert current_layer_index < 5
                            set_array(player_pos, current_layer.mob_array, None)
                            current_layer = current_layer_key[current_layer_index]
                            set_array(player_pos, current_layer.mob_array, Mob(MobID.PLAYER))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            do_calc_light_map = True
                            level_is_dark = night_time if current_layer_index < 2 else True
                            number_of_mobs = count_mobs(current_layer.mob_array)
                            message_logs.appendleft("you go down the")
                            message_logs.appendleft("staircase")
                        elif current_tile.has_tag(TileTag.UP_STAIRS):
                            current_layer_index -= 1
                            assert current_layer_index > -1
                            set_array(player_pos, current_layer.mob_array, None)
                            current_layer = current_layer_key[current_layer_index]
                            set_array(player_pos, current_layer.mob_array, Mob(MobID.PLAYER))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            do_calc_light_map = True
                            level_is_dark = night_time if current_layer_index < 2 else True
                            number_of_mobs = count_mobs(current_layer.mob_array)
                            message_logs.appendleft("you go up the")
                            message_logs.appendleft("staircase")
                        else:
                            do_a_game_tick = True
                    else:
                        cursor_index = 0  # reset cursor

        # Update.
        clock.tick()

        # Update animations.
        if pg.time.get_ticks() - cursor_flash_timer >= CURSOR_FLASH_FREQ:
            cursor_flash_timer = pg.time.get_ticks()
            cursor_show = not cursor_show

        if pg.time.get_ticks() - stam_flash_timer >= STAM_FLASH_FREQ:
            stam_flash_timer = pg.time.get_ticks()
            stam_flash = not stam_flash

        # Get the current player light radius
        light_radius = item_light[current_item.id] if current_item.has_tag(ItemTag.LIGHT) else player_light_radius

        # Do the game updates.
        if do_a_game_tick:
            do_a_game_tick = False

            world_time += 1
            if world_time - day_cycle_timer >= DAY_CYCLE_LENGTH:
                day_cycle_timer = world_time
                night_time = not night_time
                level_is_dark = night_time if current_layer_index < 2 else True
                if night_time and current_layer_index < 2:
                    message_logs.appendleft("darkness falls")
                    message_logs.appendleft("over the land")
                else:
                    message_logs.appendleft("the darkness")
                    message_logs.appendleft("is dispelled")
            elif DAY_CYCLE_LENGTH - (world_time - day_cycle_timer) == 20:
                if night_time and current_layer_index < 2:
                    message_logs.appendleft("the sun shines")
                    message_logs.appendleft("ever brighter")
                else:
                    message_logs.appendleft("the sun is")
                    message_logs.appendleft("almost gone")
            elif DAY_CYCLE_LENGTH - (world_time - day_cycle_timer) == 100:
                if night_time and current_layer_index < 2:
                    message_logs.appendleft("the horizon")
                    message_logs.appendleft("shines faintly")
                else:
                    message_logs.appendleft("the sun is")
                    message_logs.appendleft("starting to set")
            print(f"tick {world_time} layer {current_layer_index} - {'night' if night_time else 'day'}")

            if regen_stam and not get_array(player_pos, current_layer.tile_array).has_tag(TileTag.LIQUID):
                player_stamina += 1
                player_stamina = min(player_stamina, 10)
            regen_stam = True
            # Check for darkness; it can still be daytime in caves.
            if level_is_dark and random.random() < MOB_SPAWN_CHANCE and number_of_mobs < game_world.mob_cap:
                # Spawn a mob.
                for i in range(100):
                    # Attempt to place 100 times before giving up
                    sx, sy = random.randrange(world_size[0]), random.randrange(world_size[1])
                    if light_map[sx][sy] or distance_within((sx, sy), player_pos, light_radius + 1):
                        continue  # don't spawn if the tile is lit
                    try_tile = current_layer.tile_array[sx][sy]
                    try_mob = current_layer.mob_array[sx][sy]
                    if try_mob or try_tile.has_tag(TileTag.BLOCK_MOVE) or try_tile.has_tag(TileTag.LIQUID):
                        continue  # don't replace another mob or spawn in a wall
                    if try_tile.id == TileID.WEB:
                        if current_layer_index == 0:
                            mob_id = MobID.CLOUD_SPIDER
                        elif current_layer_index < 4:
                            mob_id = MobID.SPIDER
                        else:
                            mob_id = MobID.HELL_SPIDER
                    else:
                        mob_id = random.choice(mob_spawn_per_layer[current_layer_index])
                    current_layer.mob_array[sx][sy] = Mob(mob_id)
                    number_of_mobs += 1
                    print(f"Spawned {mob_id} at ({sx},{sy}) on {i}")
                    break
                else:
                    print("mob spawning exhausted")
            print(f"total mobs: {number_of_mobs}/{game_world.mob_cap}")

            # Tick the world.
            already_spread: set[tuple[int, int]] = set()
            already_mob_ticked: set[Mob] = set()
            for x in range(world_size.x):
                for y in range(world_size.y):
                    # Tick the tiles first.
                    current_tile = current_layer.tile_array[x][y]
                    # Spread the tiles.
                    if current_tile.has_tag(TileTag.SPREAD) and (x, y) not in already_spread:
                        spread_onto, spread_chance = tile_spread[current_tile.id]
                        for nx in (-1, 0, 1):
                            for ny in (-1, 0, 1):
                                if nx == ny == 0:
                                    continue  # this is the same tile
                                if math.fabs(nx) == math.fabs(ny) == 1:
                                    continue  # this is a diagonal
                                neighbor = get_array((x + nx, y + ny),
                                                     current_layer.tile_array)
                                if neighbor is None:
                                    continue
                                elif neighbor.id == spread_onto and random.random() < spread_chance:
                                    already_spread.add((x + nx, y + ny))
                                    set_array((x + nx, y + ny),
                                              current_layer.tile_array, Tile(current_tile.id))
                                    if (neighbor.has_tag(TileTag.BLOCK_SIGHT) ^
                                            current_tile.has_tag(TileTag.BLOCK_SIGHT)) or \
                                            neighbor.has_tag(TileTag.LIGHT) or current_tile.has_tag(TileTag.LIGHT):
                                        # if we are changing a vision blocker to clear or vice versa
                                        # if they are both clear or vision blockers we don't need to update
                                        fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                        do_calc_light_map = True
                    # Grow the tiles.
                    if current_tile.has_tag(TileTag.GROW):
                        grow_tile, grow_chance = tile_grow[current_tile.id]
                        if random.random() < grow_chance:
                            tile = Tile(grow_tile)
                            set_array((x, y),
                                      current_layer.tile_array, tile)
                            if current_tile.has_tag(TileTag.LIGHT) or tile.has_tag(TileTag.LIGHT) or\
                                    current_tile.has_tag(TileTag.BLOCK_SIGHT) ^ tile.has_tag(TileTag.BLOCK_SIGHT):
                                fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                do_calc_light_map = True
                            if light_map[x][y] and line_of_sight(player_pos, (x, y)):
                                message_logs.appendleft(f"{current_tile.name}")
                                message_logs.appendleft(f"grow> {tile.name}")
                    # Spawn skeletons from desert bones.
                    if current_tile.id is TileID.DESERT_BONES and night_time and random.random() < 0.1:
                        if distance_within(player_pos, (x, y), 5.5):
                            if get_array((x, y), current_layer.mob_array) is None:
                                set_array((x, y), current_layer.tile_array, Tile(TileID.SAND))
                                set_array((x, y), current_layer.mob_array, Mob(MobID.GREEN_SKELETON))
                                if light_map[x][y] and line_of_sight(player_pos, (x, y)):
                                    message_logs.appendleft("the bones rise")
                                    message_logs.appendleft("from the sand")
                    # Tick the mobs.
                    current_mob = current_layer.mob_array[x][y]
                    if current_mob is None or current_mob.id == MobID.PLAYER:
                        continue
                    if current_mob in already_mob_ticked:
                        continue
                    if not level_is_dark and random.random() < MOB_DESPAWN_CHANCE:
                        if not current_mob.has_tag(MobTag.NO_DESPAWN) and not \
                                distance_within((x, y), player_pos, light_radius + 1):
                            current_layer.mob_array[x][y] = None
                            number_of_mobs -= 1
                            print(f"Despawned mob. Mobs: {number_of_mobs}")
                            continue
                    if not distance_within(player_pos, (x, y), MOB_SIM_DISTANCE):
                        continue  # mobs outside this radius won't be ticked
                    if current_mob.has_tag(MobTag.AI_FOLLOW):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        dist = DOG_FOLLOW_RADIUS if current_mob.has_tag(MobTag.SWAPPABLE) else CHASE_DISTANCE
                        if distance_within((x, y), player_pos, dist):
                            # chase player
                            dir_vec = (pg.Vector2(player_pos) - pg.Vector2(x, y)).normalize()
                        else:
                            # wander randomly
                            dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            # mob wants to move horizontally
                            try_pos = Point(x + int(math.copysign(1, dir_vec.x)), y)
                        else:
                            # mob is diagonal or wants to move vertically
                            try_pos = Point(x, y + int(math.copysign(1, dir_vec.y)))
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                (move_tile.id == TileID.LAVA):
                            if move_tile.id == TileID.WATER and not current_mob.has_tag(MobTag.SWAPPABLE):
                                continue
                            set_array((x, y), current_layer.mob_array, None)
                            set_array(try_pos, current_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, current_layer.tile_array,
                                          Tile(tile_replace[move_tile.id]))
                            already_mob_ticked.add(current_mob)
                    elif current_mob.has_tag(MobTag.AI_JUMP):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        if distance_within((x, y), player_pos, JUMP_DISTANCE):
                            # chase player
                            dir_vec = (pg.Vector2(player_pos) - pg.Vector2(x, y)).normalize()
                        else:
                            # wander randomly
                            dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                        try_pos = Point(x + int(math.copysign(1, dir_vec.x)),
                                        y + int(math.copysign(1, dir_vec.y)))
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), current_layer.mob_array, None)
                            set_array(try_pos, current_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, current_layer.tile_array,
                                          Tile(tile_replace[move_tile.id]))
                            already_mob_ticked.add(current_mob)
                    elif current_mob.has_tag(MobTag.AI_SHOOT):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        target_spaces = [
                            (player_pos.x, player_pos.y + SKELETON_SHOOT_RADIUS),
                            (player_pos.x, player_pos.y - SKELETON_SHOOT_RADIUS),
                            (player_pos.x + SKELETON_SHOOT_RADIUS, player_pos.y),
                            (player_pos.x - SKELETON_SHOOT_RADIUS, player_pos.y),
                        ]
                        for target_space in target_spaces:
                            if (x, y) == target_space and line_of_sight((x, y), target_space):
                                player_health -= mob_damage[current_mob.id]
                                player_health = max(0, player_health)
                                message_logs.appendleft(f"the {current_mob.name}s")
                                message_logs.appendleft(f"arrow hits -{mob_damage[current_mob.id]}H")
                                skelly_got_em = True
                                break
                        if skelly_got_em:
                            skelly_got_em = False
                            continue
                        if distance_within((x, y), player_pos, SKELETON_SIGHT_RADIUS):
                            # go to nearest target space
                            target_spaces.sort(key=lambda p: distance_squared(p, (x, y)))
                            for target_space in target_spaces:
                                move_tile = get_array(target_space, current_layer.tile_array)
                                move_mob = get_array(target_space, current_layer.mob_array)
                                if move_mob or move_tile is None or move_tile.has_tag(TileTag.BLOCK_MOVE):
                                    continue
                                else:
                                    dir_vec = (pg.Vector2(target_space) - pg.Vector2(x, y)).normalize()
                                    break
                            else:
                                # no open target space, wander
                                dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                        else:
                            # wander randomly
                            dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            # mob wants to move horizontally
                            try_pos = Point(x + int(math.copysign(1, dir_vec.x)), y)
                        else:
                            # mob is diagonal or wants to move vertically
                            try_pos = Point(x, y + int(math.copysign(1, dir_vec.y)))
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), current_layer.mob_array, None)
                            set_array(try_pos, current_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, current_layer.tile_array,
                                          Tile(tile_replace[move_tile.id]))
                            already_mob_ticked.add(current_mob)
                    elif current_mob.has_tag(MobTag.AI_WANDER):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        # wander randomly
                        dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                        # make dir_vec only cardinal directions
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            dir_vec = Point(int(math.copysign(1, dir_vec.x)), 0)
                        else:
                            dir_vec = Point(0, int(math.copysign(1, dir_vec.y)))
                        # if it is moving in the opposite direction as last move
                        if dir_vec == (-current_mob.last_dir.x, -current_mob.last_dir.y):
                            # go the direction of last time
                            # if a mob is going right, it cannot go left without going up or down first
                            dir_vec = Point(-dir_vec.x, -dir_vec.y)
                        current_mob.last_dir = dir_vec
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            # mob wants to move horizontally
                            try_pos = Point(x + dir_vec.x, y)
                        else:
                            # mob is diagonal or wants to move vertically
                            try_pos = Point(x, y + dir_vec.y)
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob:
                            if not move_tile.has_tag(TileTag.BLOCK_MOVE):
                                set_array((x, y), current_layer.mob_array, None)
                                set_array(try_pos, current_layer.mob_array, current_mob)
                                if current_mob.light > 0:
                                    do_calc_light_map = True
                                if move_tile.has_tag(TileTag.CRUSH):
                                    set_array(try_pos, current_layer.tile_array,
                                              Tile(tile_replace[move_tile.id]))
                                already_mob_ticked.add(current_mob)
                            else:
                                current_mob.last_dir = Point(-dir_vec.x, -dir_vec.y)
                    elif current_mob.has_tag(MobTag.AI_SPIDER):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        player_tile = get_array(player_pos, current_layer.tile_array)
                        if player_tile.id != TileID.WEB:
                            continue  # don't do anything if player isn't on a web
                        if distance_within((x, y), player_pos, SPIDER_CHASE_RADIUS):
                            # chase player
                            dir_vec = (pg.Vector2(player_pos) - pg.Vector2(x, y)).normalize()
                        else:
                            continue  # squat until player on web is close
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            # mob wants to move horizontally
                            try_pos = Point(x + int(math.copysign(1, dir_vec.x)), y)
                        else:
                            # mob is diagonal or wants to move vertically
                            try_pos = Point(x, y + int(math.copysign(1, dir_vec.y)))
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), current_layer.mob_array, None)
                            set_array(try_pos, current_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, current_layer.tile_array,
                                          Tile(tile_replace[move_tile.id]))
                            already_mob_ticked.add(current_mob)
                    elif current_mob.has_tag(MobTag.AI_FLEE):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        if distance_within((x, y), player_pos, SHADE_FLEE_RADIUS):
                            # flee player
                            dir_vec = (pg.Vector2(x, y) - pg.Vector2(player_pos)).normalize()
                            current_mob.state = 'flee'
                        else:
                            # wander randomly
                            dir_vec = pg.Vector2(random.random(), random.random()).normalize()
                            current_mob.state = 'wander'
                        # make dir_vec only cardinal directions
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            dir_vec = Point(int(math.copysign(1, dir_vec.x)), 0)
                        else:
                            dir_vec = Point(0, int(math.copysign(1, dir_vec.y)))
                        # if it is moving in the opposite direction as last move
                        if current_mob.state == 'wander' and \
                                dir_vec == (-current_mob.last_dir.x, -current_mob.last_dir.y):
                            # go the direction of last time
                            # if a mob is going right, it cannot go left without going up or down first
                            dir_vec = Point(-dir_vec.x, -dir_vec.y)
                        current_mob.last_dir = dir_vec
                        if math.fabs(dir_vec.x) > math.fabs(dir_vec.y):
                            # mob wants to move horizontally
                            try_pos = Point(x + dir_vec.x, y)
                        else:
                            # mob is diagonal or wants to move vertically
                            try_pos = Point(x, y + dir_vec.y)
                        move_mob = get_array(try_pos, current_layer.mob_array)
                        move_tile = get_array(try_pos, current_layer.tile_array)
                        if move_tile and not move_mob:
                            if not move_tile.has_tag(TileTag.BLOCK_MOVE):
                                set_array((x, y), current_layer.mob_array, None)
                                set_array(try_pos, current_layer.mob_array, current_mob)
                                if current_mob.light > 0:
                                    do_calc_light_map = True
                                if move_tile.has_tag(TileTag.CRUSH):
                                    set_array(try_pos, current_layer.tile_array,
                                              Tile(tile_replace[move_tile.id]))
                                already_mob_ticked.add(current_mob)
                            else:
                                current_mob.last_dir = Point(-dir_vec.x, -dir_vec.y)

        # Check for player death.
        if not player_is_dead and player_health <= 0:
            player_is_dead = True
            message_logs.appendleft("you have died")
            message_logs.appendleft("press c or esc")

        # Calculate the light map before drawing if needed.
        if do_calc_light_map:
            do_calc_light_map = False
            calc_lightmap()

        # Draw.
        screen.fill((0, 0, 0))
        # Display world.
        dx = 0
        for x in range(-player_vision, player_vision + 1):
            dy = 0
            for y in range(-player_vision, player_vision + 1):
                real_pos = Point(player_pos.x + x, player_pos.y + y)
                if (not do_fov or fov_field[x][y]) and (not level_is_dark or get_array(real_pos, light_map) or
                                                        distance_within(player_pos, real_pos, light_radius)):
                    tile_mem = get_array(real_pos, current_layer.tile_array)
                    if tile_mem:
                        set_array(real_pos, current_layer.mem_array, tile_mem.id)
                    mob = get_array_tile(real_pos, current_layer.mob_array)
                    if mob:
                        screen.blit(mob, (dx * tile_size.x, dy * tile_size.y))
                    else:
                        tile = get_array_tile(real_pos, current_layer.tile_array)
                        if tile:
                            screen.blit(tile, (dx * tile_size.x, dy * tile_size.y))
                elif tile_id := get_array(real_pos, current_layer.mem_array):
                    tile_pos, color = Tile(tile_id).graphic
                    color = tuple(pg.Color(color).lerp((0, 0, 0), 0.75))
                    tile_image = tile_loader.get_tile(tile_pos, color)
                    screen.blit(tile_image, (dx * tile_size.x, dy * tile_size.y))
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
            if stam_flash and player_stamina < 1:
                tile = stam_full_img
            screen.blit(tile, ((40 + i) * tile_size.x, tile_size.y))
        write_text((35, 2), f"time {world_time}-{'night' if night_time else 'day'}", Color.MED_GRAY)

        # Draw current item and inventory.
        if game_mode is not GameMode.CRAFT:
            write_text((35, 3), "current item", Color.WHITE)
            tile = tile_loader.get_tile(*current_item.graphic)
            screen.blit(tile, (36 * tile_size.x, 4 * tile_size.y))
            write_text((38, 4), str(current_item), Color.LIGHT_GRAY)
        else:
            write_text((35, 3), "current recipie", Color.WHITE)
            ingredients = crafting_list[cursor_index]
            for index, ingredient in enumerate(ingredients):
                if index == 0:
                    continue  # this is the result of the recipie
                color = Color.WHITE if craftable((ingredient,), inventory) else Color.LIGHT_GRAY
                item = Item(*ingredient)
                tile = tile_loader.get_tile(*item.graphic)
                screen.blit(tile, (36 * tile_size.x, (3 + index) * tile_size.y))
                write_text((38, 3 + index), str(item), color)

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
            write_text((35, 12), f"{current_crafter.name} {len(crafting_list)}",
                       Color.WHITE)
            for index in range(10):
                real_index = index + crafting_scroll
                if real_index >= len(crafting_list):
                    break
                result = Item(*crafting_list[real_index][0])
                color = Color.WHITE if craftable(crafting_list[real_index][1:],
                                                 inventory) else Color.LIGHT_GRAY
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
    pg.init()
    main_screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("Outlast 7DRL 2024")
    icon_image = tile_loader.get_tile(Graphic.AIR_WIZARD, Color.RED)
    pg.display.set_icon(icon_image)
    things = main_menu(main_screen)
    while True:
        main(main_screen, things)
        things = main_menu(main_screen)
