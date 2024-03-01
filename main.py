#!/usr/bin/env python3
import sys
from pathlib import Path

import pygame as pg

from tileloader import TileLoader


def main():
    pg.init()

    screen = pg.display.set_mode((800, 560))  # 50x35 tiles
    pg.display.set_caption("7DRL 2024")
    clock = pg.time.Clock()
    font = pg.font.Font(None, 20)

    tile_size = (16, 16)
    tile_loader = TileLoader(Path() / "kenney_tileset.png", tile_size)

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

        # Display FPS.
        fps_surf = font.render(str(clock.get_fps()), True, (255, 255, 255))
        screen.blit(fps_surf, (0, screen.get_height() - fps_surf.get_height()))
        # Flip display.
        pg.display.flip()


if __name__ == "__main__":
    main()
