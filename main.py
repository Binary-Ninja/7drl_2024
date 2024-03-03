#!/usr/bin/env python3
import sys
from pathlib import Path
import random
from collections import deque
from enum import Enum, auto
from typing import Sequence

import pygame as pg

from tileloader import TileLoader
from world import World, set_array, get_array
from data import (Point, str_2_tile, PointType, Graphic, Color, ItemID, ItemTag,
                  TileTag, MobID, MobTag)
from items import Item, item_to_mob
from mobs import Mob
from tiles import Tile, tile_replace, tile_damage


class GameMode(Enum):
    MOVE = auto()
    INVENTORY = auto()
    CRAFT = auto()


NO_ITEM = Item(ItemID.EMPTY_HANDS)

player_health = 10


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
    global player_health
    player_stamina = 10
    player_dir = Point(0, -1)
    player_pos = Point(game_world.size[0] // 2, game_world.size[1] // 2)
    set_array(player_pos, game_world.overworld_layer.mob_array, Mob(MobID.PLAYER))

    current_item: Item | NO_ITEM = NO_ITEM
    inventory: list[Item] = [Item(ItemID.WORKBENCH),
                             Item(ItemID.DIRT, 30), Item(ItemID.SAND, 9),
                             Item(ItemID.WOOD, 1000), Item(ItemID.STONE, 100),
                             Item(ItemID.APPLE, 100),
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
        global player_health
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
                message_logs.appendleft(f"for -{damage}hp")
                player_health -= damage
                player_health = max(0, player_health)
            return player_pos
        if move_tile.has_tag(TileTag.DAMAGE):
            message_logs.appendleft(f"the {move_tile.name}")
            message_logs.appendleft(f"hurts you -{damage}hp")
            player_health -= damage
            player_health = max(0, player_health)
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
                                    not target_tile.has_tag(TileTag.BLOCK_MOVE):
                                set_array(target_pos,
                                          game_world.overworld_layer.mob_array, mob)
                                current_item = NO_ITEM
                                inventory.remove(NO_ITEM)
                                message_logs.appendleft("you place the")
                                message_logs.appendleft(f"{mob.name}")
                                displayed_empty_hands_message = True
                            else:
                                message_logs.appendleft("you cannot put")
                                message_logs.appendleft(f"{mob.name} here")
                        if current_item.has_tag(ItemTag.PICKUP):
                            if target_mob is not None:
                                item = item_to_mob[target_mob.id]
                                if item is not None:
                                    item = Item(item)
                                    add_to_inventory(current_item, inventory)
                                    current_item = item
                                    set_array(target_pos,
                                              game_world.overworld_layer.mob_array,
                                              None)
                                    message_logs.appendleft("you pick up the")
                                    message_logs.appendleft(f"{item.name}")
                        if current_item.has_tag(ItemTag.HEAL):
                            if player_health < 10:
                                prev_ph = player_health
                                player_health += current_item.data["heal"]
                                player_health = min(10, player_health)
                                current_item.count -= 1
                                message_logs.appendleft("you eat the")
                                message_logs.appendleft(f"{current_item.name} "
                                                        f"+{player_health - prev_ph}hp")
                                if current_item.count <= 0:
                                    current_item = NO_ITEM
                                    inventory.remove(NO_ITEM)
                                    displayed_empty_hands_message = True
                            else:
                                message_logs.appendleft("you have full")
                                message_logs.appendleft("health points")
                        if current_item.has_tag(ItemTag.PLACE_TILE):
                            if target_tile is not None and \
                                    target_tile.id in current_item.data["base"]:
                                set_array(target_pos,
                                          game_world.overworld_layer.tile_array,
                                          Tile(current_item.data["place"]))
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
                                message_logs.appendleft("you cannot put")
                                message_logs.appendleft(f"{current_item.name} here")
                        if current_item.has_tag(ItemTag.BREAK_TILE):
                            if not (current_item.has_tag(ItemTag.DAMAGE_MOBS) and target_mob):
                                if target_tile is not None:
                                    if target_tile.id in current_item.data["breakable"]:
                                        damage = current_item.data["tile_damage"]
                                        target_tile.health -= damage
                                        if target_tile.health > 0:
                                            message_logs.appendleft("you strike the")
                                            message_logs.appendleft(f"{target_tile.name} "
                                                                    f"-{damage}hp")
                                        else:
                                            tile, item = tile_replace[target_tile.id]
                                            set_array(target_pos,
                                                      game_world.overworld_layer.tile_array,
                                                      Tile(tile))
                                            add_to_inventory(Item(item), inventory)
                                            message_logs.appendleft("you remove the")
                                            message_logs.appendleft(f"{target_tile.name}")
                                        just_broken_a_tile = True
                                    elif displayed_empty_hands_message is False:
                                        message_logs.appendleft("you cannot use")
                                        message_logs.appendleft(f"{current_item.name}")
                                else:
                                    message_logs.appendleft("the unfeeling")
                                    message_logs.appendleft("void mocks you")
                        if current_item.has_tag(ItemTag.DAMAGE_MOBS):
                            if not just_broken_a_tile:
                                if target_mob is not None:
                                    damage = current_item.data["mob_damage"]
                                    target_mob.health -= damage
                                    message_logs.appendleft("you strike the")
                                    message_logs.appendleft(f"{target_mob.name} -{damage}hp")
                                    if target_mob.health <= 0:
                                        set_array(target_pos,
                                                  game_world.overworld_layer.mob_array,
                                                  None)
                                        message_logs.appendleft("you kill the")
                                        message_logs.appendleft(f"{target_mob.name}")
                                elif displayed_empty_hands_message is False:
                                    message_logs.appendleft("you strike at")
                                    message_logs.appendleft("air uselessly")
                        just_broken_a_tile = False
                        displayed_empty_hands_message = False
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
                        if target_mob and target_mob.has_tag(MobTag.CRAFTING):
                            game_mode = GameMode.CRAFT
                            current_crafter = target_mob
                            crafting_list = current_crafter.recipies
                            message_logs.appendleft("you craft with")
                            message_logs.appendleft(f"the {current_crafter.name}")
                        else:
                            game_mode = GameMode.INVENTORY
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
