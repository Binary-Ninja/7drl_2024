from pathlib import Path

import pygame as pg


class FakeSound:
    def play(self): pass
    def set_volume(self): pass


class SoundLoader:
    def __init__(self, sound_dir: Path, load_sounds: bool):
        # The keys for the sounds are the filenames without the extension.
        self.sounds: dict[str, pg.mixer.Sound | FakeSound] = {}
        for sound in sound_dir.iterdir():
            self.sounds[sound.stem] = pg.mixer.Sound(str(sound)) if load_sounds else FakeSound()

    def set_volume(self, volume: float):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play(self, sound: str):
        self.sounds[sound].play()

    def play_sounds(self, sounds):
        for sound in sounds:
            self.play(sound)
