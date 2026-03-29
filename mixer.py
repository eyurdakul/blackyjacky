import os
from settings import EFFECT_VOLUME, BACKGROUND_VOLUME
from enums import SoundLibrary

class Mixer:
    def __init__(self, mixer):
        self.sounds_dir = "sounds"
        self.__mixer = mixer
        self.__mixer.init()
        self.card = self.__load_sound("card.ogg", EFFECT_VOLUME)
        self.chip = self.__load_sound("chip.ogg", EFFECT_VOLUME)
        self.shuffle = self.__load_sound("shuffle.ogg", EFFECT_VOLUME)
        self.winner = self.__load_sound("winner.mp3", EFFECT_VOLUME)
        self.loser = self.__load_sound("loser.mp3", EFFECT_VOLUME)
        self.click = self.__load_sound("click.mp3", EFFECT_VOLUME)
        self.__load_music("background.mp3")

    def __load_music(self, name):
        self.__mixer.music.load(self.__get_path(name))
        self.__set_volume(BACKGROUND_VOLUME)
        self.__mixer.music.play(-1)

    def play(self, type):
        if type == SoundLibrary.CARD:
            self.card.play()
        elif type == SoundLibrary.CHIP:
            self.chip.play()
        elif type == SoundLibrary.CLICK:
            self.click.play()
        elif type == SoundLibrary.LOSE:
            self.loser.play()
        elif type == SoundLibrary.SHUFFLE:
            self.shuffle.play()
        elif type == SoundLibrary.WIN:
            self.winner.play()

    def __load_sound(self, sound, volume):
        effect = self.__mixer.Sound(self.__get_path(sound))
        effect.set_volume(volume)
        return effect

    def __set_volume(self, volume):
        self.__mixer.music.set_volume(volume)

    def __get_path(self, name):
        return os.path.join(self.sounds_dir, name)
    