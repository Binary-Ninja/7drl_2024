from pathlib import Path

import pygame as pg

sound_names = [
    "explosion.wav",
    "failure.wav",
    "heal.wav",
    "hurt.wav",
    "hurt_enemy.wav",
    "indicator.wav",
    "success.wav",
    "use_item.wav",
    "victory.wav",
]


class FakeSound:
    def play(self): pass
    def set_volume(self): pass


class SoundLoader:
    def __init__(self, sound_dir: str, load_sounds: bool):
        # The keys for the sounds are the filenames without the extension.
        self.sounds: dict[str, pg.mixer.Sound | FakeSound] = {}
        if load_sounds:
            for sound_name in sound_names:
                sound = Path() / sound_dir / sound_name
                self.sounds[sound.stem] = pg.mixer.Sound(str(sound)) if load_sounds else FakeSound()

    def set_volume(self, volume: float):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play(self, sound: str):
        self.sounds.get(sound, FakeSound()).play()

    def play_sounds(self, sounds):
        for sound in sounds:
            self.play(sound)
