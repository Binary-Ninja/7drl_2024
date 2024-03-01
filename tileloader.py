from pathlib import Path

import pygame as pg


class TileLoader:
    def __init__(self, img_path: Path, tile_size: tuple[int, int]):
        self.tile_img = pg.image.load(img_path)
        self.tile_size = tile_size
        self.loaded_tiles = {}

    def get_tile(self, tile_pos: tuple[int, int],
                 color: tuple[int, int, int] | None = None) -> pg.Surface:
        key_color = color if color is not None else (255, 255, 255)
        if tile_surf := self.loaded_tiles.get((tile_pos, key_color), None):
            return tile_surf
        tile_surf = pg.Surface(self.tile_size).convert()
        area = (self.tile_size[0] * tile_pos[0],
                self.tile_size[1] * tile_pos[1],
                *self.tile_size)
        tile_surf.blit(self.tile_img, (0, 0), area)
        if color:
            tile_surf.fill(color, special_flags=pg.BLEND_MULT)
        self.loaded_tiles[(tile_pos, key_color)] = tile_surf
        return tile_surf
