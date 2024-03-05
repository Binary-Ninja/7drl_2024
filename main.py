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
from items import Item, item_to_mob
from mobs import Mob, mob_damage
from tiles import Tile, tile_replace, tile_damage, TileID, tile_grow, tile_spread, tile_light
from loots import tile_break_loot, resolve_loot


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
CHASE_DISTANCE = 10
JUMP_DISTANCE = 8
SKELETON_SHOOT_RADIUS = 5
SKELETON_SIGHT_RADIUS = 12

player_vision = 17
player_light_radius = 3.5
player_health = 10
player_stamina = 10
regen_stam = True
light_map: list[list[bool]] = []
path_to_player: dict[tuple, tuple] = {}


def main():
    pg.init()

    screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("Outlast 7DRL 2024")
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
    icon_image = tile_loader.get_tile(Graphic.AIR_WIZARD, Color.RED)

    pg.display.set_icon(icon_image)

    cursor_flash_timer = pg.time.get_ticks()
    CURSOR_FLASH_FREQ = 500
    cursor_show = True

    stam_flash_timer = pg.time.get_ticks()
    STAM_FLASH_FREQ = 200
    stam_flash = True

    cursor_index = 0  # what inventory item it is on

    world_time = 0
    do_a_game_tick = False

    day_cycle_timer = world_time
    DAY_CYCLE_LENGTH = 400
    night_time = False
    level_is_dark = False
    number_of_mobs = 0  # TODO: dont forget to update this to load on layer load when i add world layers
    MOB_SPAWN_CHANCE = 0.1
    MOB_DESPAWN_CHANCE = 0.05

    world_seed = random.getrandbits(64)
    world_seed = 1234
    print(world_seed)
    world_size = Point(100, 100)
    print(world_size)
    game_world = World(world_size, world_seed)
    game_world.generate_overworld_layer()

    global player_vision
    global path_to_player
    global light_map
    do_fov = True
    global player_health
    global player_stamina
    global regen_stam
    player_dir = Point(0, -1)
    player_pos = Point(game_world.size[0] // 2, game_world.size[1] // 2)
    set_array(player_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))

    current_item: Item | NO_ITEM = NO_ITEM
    inventory: list[Item] = [Item(ItemID.WORKBENCH),
                             # Item(ItemID.DIRT, 30), Item(ItemID.SAND, 9),
                             # Item(ItemID.WOOD, 1000), Item(ItemID.STONE, 100),
                             # Item(ItemID.COCONUT, 100), Item(ItemID.COAL, 99),
                             # Item(ItemID.WINDOW, 100), Item(ItemID.STONE_WALL, 99),
                             # Item(ItemID.WOOD_DOOR, 100), Item(ItemID.WHEAT_SEEDS, 99),
                             # Item(ItemID.SPAWN_EGG_GREEN_ZOMBIE, 100), Item(ItemID.GEM, 99),
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

    just_broken_a_tile = False
    displayed_empty_hands_message = False
    just_placed_a_tile = False
    displayed_no_use_message = False
    skelly_got_em = False

    def calc_paths():
        return
        global path_to_player
        frontier: deque[Point] = deque()
        frontier.append(player_pos)
        path_to_player = {player_pos: player_pos}

        while len(frontier):
            current = frontier.pop()
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if x == y == 0:
                        continue  # same tile
                    if math.fabs(x) == math.fabs(y) == 1:
                        continue  # this is a diagonal
                    next_point = (current[0] + x, current[1] + y)
                    if not distance_within(player_pos, next_point, MOB_SIM_DISTANCE + 1):
                        continue  # don't spread bfs beyond the simulation distance
                    path_tile = get_array(next_point, game_world.overworld_layer.tile_array)
                    if path_tile is None:
                        continue  # out of bounds
                    if (TileTag.BLOCK_MOVE, TileTag.LIQUID) in path_tile.tags:
                        # this has the effect of removing these tiles from the path data entirely
                        # this means if a mob is standing on a blocking tile or a liquid, it cannot path
                        continue  # there is a liquid or blocker in the way
                    if next_point not in path_to_player:
                        frontier.append(next_point)
                        path_to_player[next_point] = tuple(current)

    calc_paths()

    def line_of_sight_path(start: PointType, end: PointType) -> list[Point]:
        path: list[Point] = []
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
            tile = get_array((int(p.x), int(p.y)), game_world.overworld_layer.tile_array)
            if tile is None or tile.has_tag(TileTag.BLOCK_SIGHT):
                return []
            else:
                path.append(Point(int(p.x), int(p.y)))
        return path

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
            tile = get_array((int(p.x), int(p.y)), game_world.overworld_layer.tile_array)
            if tile is None or tile.has_tag(TileTag.BLOCK_SIGHT):
                return False
        return True

    def calc_fov(start: Point, radius: int, master=None) -> list[list[bool]]:
        fov_field = make_2d_array((radius * 2 + 1, radius * 2 + 1), False)
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                real_pos = Point(start.x + x, start.y + y)
                if distance_within(start, real_pos, radius + 0.5):
                    if master is not None:
                        if line_of_sight(start, real_pos):
                            master[real_pos.x][real_pos.y] = True
                    else:
                        fov_field[x][y] = line_of_sight(start, real_pos)
        return fov_field

    fov_field = calc_fov(player_pos, MAX_VIEW_DIST)

    def calc_lightmap():
        global light_map
        light_map = make_2d_array(world_size, False)
        for x in range(world_size.x):
            for y in range(world_size.y):
                light_mob = game_world.overworld_layer.mob_array[x][y]
                if light_mob and light_mob.light > 0:
                    calc_fov(Point(x, y), light_mob.light, light_map)
                light_tile = game_world.overworld_layer.tile_array[x][y]
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

    def spawn_mob(pos: PointType, mob_id: MobID):
        set_array(pos, game_world.overworld_layer.mob_array, Mob(mob_id))

    # add some test mobs
    # spawn_mob((48, 48), MobID.WORKBENCH)
    # spawn_mob((49, 49), MobID.WOOD_LANTERN)
    # spawn_mob((60, 50), MobID.GREEN_SKELETON)
    # spawn_mob((50, 52), MobID.GREEN_ZOMBIE)
    # spawn_mob((50, 60), MobID.GREEN_SKELETON)
    # spawn_mob((50, 62), MobID.GREEN_ZOMBIE)

    calc_lightmap()

    def write_text(pos: PointType, text: str, color: tuple[int, int, int]):
        for index, char in enumerate(text):
            char_tile = tile_loader.get_tile(str_2_tile[char], color)
            screen.blit(char_tile, ((pos[0] + index) * tile_size[0],
                                    pos[1] * tile_size.y))

    def get_array_tile(pos: PointType, array: list[list], dark: bool = False) -> pg.Surface | None:
        value = get_array(pos, array)
        if value:
            tile, color = value.graphic
            if dark:
                color = tuple(pg.Color(color).lerp((0, 0, 0), 0.75))
            return tile_loader.get_tile(tile, color)

    def move_player(direction: tuple[int, int]) -> Point:
        global player_health, light_map, player_stamina, regen_stam
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
                        message_logs.appendleft("you push the")
                        message_logs.appendleft(f"{move_mob.name}")
                        set_array(try_pos, game_world.overworld_layer.mob_array, None)
                        if try_tile.has_tag(TileTag.LIQUID):
                            message_logs.appendleft("it sinks into")
                            message_logs.appendleft(f"the {try_tile.name}")
                        else:
                            set_array(try_space,
                                      game_world.overworld_layer.mob_array, move_mob)
                            if try_tile.has_tag(TileTag.CRUSH):
                                set_array(try_space, game_world.overworld_layer.tile_array,
                                          Tile(tile_replace[try_tile.id]))
                                message_logs.appendleft("it crushes the")
                                message_logs.appendleft(f"{try_tile.name}")
                        if move_mob.light > 0:
                            calc_lightmap()
                        calc_paths()
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
        if move_tile is None:
            message_logs.appendleft("you stare into")
            message_logs.appendleft("the abyss")
            return player_pos
        damage = tile_damage[move_tile.id]
        if move_tile.has_tag(TileTag.BLOCK_MOVE):
            message_logs.appendleft("you bump into")
            message_logs.appendleft(f"the {move_tile.name}")
            if move_tile.has_tag(TileTag.DAMAGE):
                message_logs.appendleft("it hurts you")
                message_logs.appendleft(f"for -{damage}H")
                player_health -= damage
                player_health = max(0, player_health)
            return player_pos
        if move_tile.has_tag(TileTag.DAMAGE):
            message_logs.appendleft(f"the {move_tile.name}")
            message_logs.appendleft(f"hurts you -{damage}H")
            player_health -= damage
            player_health = max(0, player_health)
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
            set_array(try_pos, game_world.overworld_layer.tile_array, Tile(tile_replace[move_tile.id]))
            for item in resolve_loot(tile_break_loot[move_tile.id]):
                add_to_inventory(item, inventory)
                message_logs.appendleft("you crush the")
                message_logs.appendleft(f"{move_tile.name}")
        set_array(player_pos, game_world.overworld_layer.mob_array, None)
        set_array(try_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))
        calc_paths()
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
                elif event.key == pg.K_SPACE:
                    level_is_dark = not level_is_dark
                elif event.key == pg.K_f:
                    do_fov = not do_fov
                elif event.key == pg.K_w:
                    player_health = 10
                    player_stamina = 10
                elif event.key == pg.K_UP:
                    cursor_show = True
                    if game_mode is GameMode.MOVE:
                        if player_dir == (0, -1):
                            do_a_game_tick = True
                            player_pos = move_player((0, -1))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            calc_paths()
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
                            do_a_game_tick = True
                            player_pos = move_player((0, 1))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            calc_paths()
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
                            do_a_game_tick = True
                            player_pos = move_player((-1, 0))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            calc_paths()
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
                            do_a_game_tick = True
                            player_pos = move_player((1, 0))
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            calc_paths()
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
                        do_a_game_tick = True
                        target_pos = Point(player_pos.x + player_dir.x,
                                           player_pos.y + player_dir.y)
                        target_mob = get_array(target_pos,
                                               game_world.overworld_layer.mob_array)
                        target_tile = get_array(target_pos,
                                                game_world.overworld_layer.tile_array)
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
                                              game_world.overworld_layer.mob_array, mob)
                                    current_item.count -= 1
                                    if current_item.count <= 0:
                                        current_item = NO_ITEM
                                        inventory.remove(NO_ITEM)
                                        displayed_empty_hands_message = True
                                    message_logs.appendleft("you place the")
                                    message_logs.appendleft(f"{mob.name}")
                                    calc_paths()
                                    if mob.light > 0:
                                        calc_lightmap()
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
                                                  game_world.overworld_layer.mob_array,
                                                  None)
                                        message_logs.appendleft("you pick up the")
                                        message_logs.appendleft(f"{item.name}")
                                        calc_paths()
                                        if target_mob.light > 0:
                                            calc_lightmap()
                                    else:
                                        message_logs.appendleft("you do not have")
                                        message_logs.appendleft("the stamina")
                        if current_item.has_tag(ItemTag.HEAL):
                            if player_health < 10:
                                if reduce_stamina(current_item.data["stamina_cost"]):
                                    prev_ph = player_health
                                    player_health += current_item.data["heal"]
                                    player_health = min(10, player_health)
                                    current_item.count -= 1
                                    message_logs.appendleft("you eat the")
                                    message_logs.appendleft(f"{current_item.name} "
                                                            f"+{player_health - prev_ph}H")
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
                                              game_world.overworld_layer.tile_array, tile)
                                    fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                    calc_paths()
                                    if tile.has_tag(TileTag.LIGHT):
                                        calc_lightmap()
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
                                                                        f"-{damage}H")
                                            else:
                                                tile = Tile(tile_replace[target_tile.id])
                                                loot = resolve_loot(
                                                    tile_break_loot[target_tile.id])
                                                set_array(target_pos,
                                                          game_world.overworld_layer.tile_array, tile)
                                                fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                                calc_paths()
                                                if tile.has_tag(TileTag.LIGHT):
                                                    calc_lightmap()
                                                for item in loot:
                                                    add_to_inventory(item, inventory)
                                                message_logs.appendleft("you remove the")
                                                message_logs.appendleft(f"{target_tile.name}")
                                            just_broken_a_tile = True
                                        else:
                                            message_logs.appendleft("you do not have")
                                            message_logs.appendleft("the stamina")
                                    elif displayed_empty_hands_message is False:
                                        message_logs.appendleft("you cannot use")
                                        message_logs.appendleft(f"{current_item.name}")
                                else:
                                    message_logs.appendleft("the unfeeling")
                                    message_logs.appendleft("void mocks you")
                        if current_item.has_tag(ItemTag.DAMAGE_MOBS):
                            if not just_broken_a_tile:
                                if target_mob is not None:
                                    stam_cost = current_item.data["stamina_cost"]
                                    if reduce_stamina(stam_cost):
                                        damage = current_item.data["mob_damage"]
                                        target_mob.health -= damage
                                        message_logs.appendleft("you strike the")
                                        message_logs.appendleft(f"{target_mob.name}"
                                                                f"-{damage}H")
                                        if target_mob.health <= 0:
                                            set_array(target_pos,
                                                      game_world.overworld_layer.mob_array,
                                                      None)
                                            if target_mob.light > 0:
                                                calc_lightmap()
                                            calc_paths()
                                            message_logs.appendleft("you kill the")
                                            message_logs.appendleft(f"{target_mob.name}")
                                    else:
                                        message_logs.appendleft("you do not have")
                                        message_logs.appendleft("the stamina")
                                elif displayed_empty_hands_message is False:
                                    message_logs.appendleft("you strike at")
                                    message_logs.appendleft("air uselessly")
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
                        target_tile = get_array(target_pos,
                                                game_world.overworld_layer.tile_array)
                        if target_mob and target_mob.has_tag(MobTag.CRAFTING):
                            game_mode = GameMode.CRAFT
                            current_crafter = target_mob
                            crafting_list = current_crafter.recipies
                            message_logs.appendleft("you craft with")
                            message_logs.appendleft(f"the {current_crafter.name}")
                        elif target_tile and target_tile.id in (TileID.OPEN_WOOD_DOOR,
                                                                TileID.CLOSED_WOOD_DOOR):
                            if target_tile.id is TileID.CLOSED_WOOD_DOOR:
                                set_array(target_pos,
                                          game_world.overworld_layer.tile_array,
                                          Tile(TileID.OPEN_WOOD_DOOR))
                                message_logs.appendleft("you open the")
                                message_logs.appendleft(f"{target_tile.name}")
                            else:
                                set_array(target_pos,
                                          game_world.overworld_layer.tile_array,
                                          Tile(TileID.CLOSED_WOOD_DOOR))
                                message_logs.appendleft("you close the")
                                message_logs.appendleft(f"{target_tile.name}")
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                        else:
                            game_mode = GameMode.INVENTORY
                elif event.key == pg.K_z:
                    if game_mode is GameMode.MOVE:
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

        # Do the game updates.
        if do_a_game_tick:
            do_a_game_tick = False

            world_time += 1
            if world_time - day_cycle_timer >= DAY_CYCLE_LENGTH:
                day_cycle_timer = world_time
                night_time = not night_time
                level_is_dark = night_time
                if night_time:
                    message_logs.appendleft("darkness falls")
                    message_logs.appendleft("over the land")
                else:
                    message_logs.appendleft("the darkness")
                    message_logs.appendleft("is dispelled")
            elif DAY_CYCLE_LENGTH - (world_time - day_cycle_timer) == 20:
                if night_time:
                    message_logs.appendleft("the sun shines")
                    message_logs.appendleft("ever brighter")
                else:
                    message_logs.appendleft("the sun is")
                    message_logs.appendleft("almost gone")
            elif DAY_CYCLE_LENGTH - (world_time - day_cycle_timer) == 100:
                if night_time:
                    message_logs.appendleft("the horizon")
                    message_logs.appendleft("shines faintly")
                else:
                    message_logs.appendleft("the sun is")
                    message_logs.appendleft("starting to set")
            print(f"tick {world_time} - {'night' if night_time else 'day'}")

            if regen_stam:
                player_stamina += 1
                player_stamina = min(player_stamina, 10)
            regen_stam = True
            # Check for darkness; it can still be daytime in caves.
            if level_is_dark and random.random() < MOB_SPAWN_CHANCE and number_of_mobs < game_world.mob_cap:
                # Spawn a mob.
                for i in range(100):
                    # Attempt to place 100 times before giving up
                    sx, sy = random.randrange(world_size[0]), random.randrange(world_size[1])
                    if light_map[sx][sy] or distance_within((sx, sy), player_pos, player_light_radius + 1):
                        continue  # don't spawn if the tile is lit or too close to player
                    try_tile = game_world.overworld_layer.tile_array[sx][sy]
                    try_mob = game_world.overworld_layer.mob_array[sx][sy]
                    if try_mob or try_tile.has_tag(TileTag.BLOCK_MOVE) or try_tile.has_tag(TileTag.LIQUID):
                        continue  # don't replace another mob or spawn in a wall
                    mob_id = random.choice((MobID.GREEN_ZOMBIE, MobID.GREEN_SLIME, MobID.GREEN_SKELETON))
                    game_world.overworld_layer.mob_array[sx][sy] = Mob(mob_id)
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
                    current_tile = game_world.overworld_layer.tile_array[x][y]
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
                                                     game_world.overworld_layer.tile_array)
                                if neighbor is None:
                                    continue
                                elif neighbor.id == spread_onto and random.random() < spread_chance:
                                    already_spread.add((x + nx, y + ny))
                                    set_array((x + nx, y + ny),
                                              game_world.overworld_layer.tile_array, Tile(current_tile.id))
                                    if neighbor.has_tag(TileTag.BLOCK_SIGHT) ^ \
                                            current_tile.has_tag(TileTag.BLOCK_SIGHT):
                                        # if we are changing a vision blocker to clear or vice versa
                                        # if they are both clear or vision blockers we don't need to update
                                        fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                                    if neighbor.has_tag(TileTag.LIGHT) or current_tile.has_tag(TileTag.LIGHT):
                                        calc_lightmap()
                    # Grow the tiles.
                    if current_tile.has_tag(TileTag.GROW):
                        grow_tile, grow_chance = tile_grow[current_tile.id]
                        if random.random() < grow_chance:
                            tile = Tile(grow_tile)
                            set_array((x, y),
                                      game_world.overworld_layer.tile_array, tile)
                            fov_field = calc_fov(player_pos, MAX_VIEW_DIST)
                            if current_tile.has_tag(TileTag.LIGHT) or tile.has_tag(TileTag.LIGHT):
                                calc_lightmap()
                            if line_of_sight(player_pos, (x, y)):
                                message_logs.appendleft(f"{current_tile.name}")
                                message_logs.appendleft(f"grow> {tile.name}")
                    # Spawn skeletons from desert bones.
                    if current_tile.id is TileID.DESERT_BONES and night_time and random.random() < 0.1:
                        if distance_within(player_pos, (x, y), 5.5):
                            if get_array((x, y), game_world.overworld_layer.mob_array) is None:
                                set_array((x, y), game_world.overworld_layer.tile_array, Tile(TileID.SAND))
                                set_array((x, y), game_world.overworld_layer.mob_array, Mob(MobID.GREEN_SKELETON))
                                if light_map[x][y] and line_of_sight(player_pos, (x, y)):
                                    message_logs.appendleft("the bones rise")
                                    message_logs.appendleft("from the sand")
                    # Tick the mobs.
                    current_mob = game_world.overworld_layer.mob_array[x][y]
                    if current_mob is None or current_mob.id is MobID.PLAYER:
                        continue
                    if current_mob in already_mob_ticked:
                        continue
                    if not level_is_dark and random.random() < MOB_DESPAWN_CHANCE:
                        game_world.overworld_layer.mob_array[x][y] = None
                        number_of_mobs -= 1
                        print(f"Despawned mob. Mobs: {number_of_mobs}")
                        continue
                    if not distance_within(player_pos, (x, y), MOB_SIM_DISTANCE):
                        continue  # mobs outside this radius won't be ticked
                    if current_mob.has_tag(MobTag.AI_FOLLOW):
                        current_mob.ai_tick += 1
                        if current_mob.ai_tick % current_mob.ai_timer != 0:
                            continue  # only tick every ai_timer ticks
                        if distance_within((x, y), player_pos, CHASE_DISTANCE):
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
                        move_mob = get_array(try_pos, game_world.overworld_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, game_world.overworld_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), game_world.overworld_layer.mob_array, None)
                            set_array(try_pos, game_world.overworld_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, game_world.overworld_layer.tile_array,
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
                        move_mob = get_array(try_pos, game_world.overworld_layer.mob_array)
                        if move_mob and move_mob.id == MobID.PLAYER and current_mob.has_tag(MobTag.DAMAGE):
                            player_health -= mob_damage[current_mob.id]
                            player_health = max(0, player_health)
                            message_logs.appendleft(f"the {current_mob.name}")
                            message_logs.appendleft(f"hits you -{mob_damage[current_mob.id]}H")
                        move_tile = get_array(try_pos, game_world.overworld_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), game_world.overworld_layer.mob_array, None)
                            set_array(try_pos, game_world.overworld_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, game_world.overworld_layer.tile_array,
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
                            if (x, y) == target_space:
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
                                move_tile = get_array(target_space, game_world.overworld_layer.tile_array)
                                move_mob = get_array(target_space, game_world.overworld_layer.mob_array)
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
                        move_mob = get_array(try_pos, game_world.overworld_layer.mob_array)
                        move_tile = get_array(try_pos, game_world.overworld_layer.tile_array)
                        if move_tile and not move_mob and not move_tile.has_tag(TileTag.BLOCK_MOVE) and not\
                                move_tile.has_tag(TileTag.LIQUID):
                            set_array((x, y), game_world.overworld_layer.mob_array, None)
                            set_array(try_pos, game_world.overworld_layer.mob_array, current_mob)
                            if move_tile.has_tag(TileTag.CRUSH):
                                set_array(try_pos, game_world.overworld_layer.tile_array,
                                          Tile(tile_replace[move_tile.id]))
                            already_mob_ticked.add(current_mob)

        # Draw.
        screen.fill((0, 0, 0))

        # Display world.
        dx = 0
        for x in range(-player_vision, player_vision + 1):
            dy = 0
            for y in range(-player_vision, player_vision + 1):
                real_pos = Point(player_pos.x + x, player_pos.y + y)
                if (not do_fov or fov_field[x][y]) and (not level_is_dark or get_array(real_pos, light_map) or
                                                        distance_within(player_pos, real_pos, player_light_radius)):
                    set_array(real_pos, game_world.overworld_layer.mem_array, True)
                    mob = get_array_tile(real_pos, game_world.overworld_layer.mob_array)
                    if mob:
                        screen.blit(mob, (dx * tile_size.x, dy * tile_size.y))
                    else:
                        tile = get_array_tile(real_pos, game_world.overworld_layer.tile_array)
                        if tile:
                            screen.blit(tile, (dx * tile_size.x, dy * tile_size.y))
                elif get_array(real_pos, game_world.overworld_layer.mem_array):
                    mob = get_array_tile(real_pos, game_world.overworld_layer.mob_array, True)
                    if mob:
                        screen.blit(mob, (dx * tile_size.x, dy * tile_size.y))
                    else:
                        tile = get_array_tile(real_pos, game_world.overworld_layer.tile_array, True)
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
    main()
