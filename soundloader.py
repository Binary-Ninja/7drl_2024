from pathlib import Path
from typing import Sequence

import pygame as pg


class FakeSound:
    def play(self): pass


class SoundLoader:
    def __init__(self, sound_dir: Path, load_sounds: bool):
        # The keys for the sounds are the filenames without the extension.
        self.sounds: dict[str, pg.mixer.Sound | FakeSound] = {}
        for sound in sound_dir.iterdir():
            self.sounds[sound.stem] = pg.mixer.Sound(str(sound)) if load_sounds else FakeSound()

    def play(self, sound: str):
        self.sounds[sound].play()

    def play_sounds(self, sounds: Sequence[str]):
        for sound in sounds:
            self.play(sound)
