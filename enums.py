from enum import Enum

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    DEALER_TURN = 3
    GAME_OVER = 4

class ButtonType(Enum):
    QUIT = 1
    START = 2
    HIT = 3
    STAND = 4
    BACK = 5

class SoundLibrary(Enum):
    CARD = 1
    CHIP = 2
    WIN = 3
    LOSE = 4
    CLICK = 5
    SHUFFLE = 6

class Suits(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4