import pygame
import sys, os
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

TABLE_GREEN = (16, 102, 58)

WOOD = (139, 69, 19)
WOOD_LIGHT = (160, 82, 45)
WOOD_DARK = (101, 51, 15)

GOLD = (212, 175, 55)
WHITE = (255, 255, 255)

GAP = 40
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60

BACKGROUND_VOLUME = 0.2
EFFECT_VOLUME = 0.5

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class BlackjackGame:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.sound = Mixer()
        self.__initiate_positions()
        self.__initiate_buttons()
        self.__initiate_title()
        self.__initialise_background()
        self.running = True

    def __initiate_title(self):
        self.title_img = pygame.image.load(
            os.path.join("assets", "title.png")
        ).convert_alpha()
        self.title_rect = self.title_img.get_rect(center=(self.center_x, self.center_y - 50))

    def __initialise_background(self):
        self.background_img = pygame.image.load(
            os.path.join("assets", "background.png")
        ).convert()
        self.background_rect = self.background_img.get_rect(center=(self.center_x, self.center_y - 50))

    def __initiate_positions(self):
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.pos_y = self.height - BUTTON_HEIGHT - GAP

        self.pos1_x = self.center_x - BUTTON_WIDTH - (GAP // 2)
        self.pos2_x = self.center_x + (GAP // 2)
        self.pos4_x = self.center_x - (BUTTON_WIDTH // 2)
        self.pos3_x = self.pos4_x - BUTTON_WIDTH - GAP
        self.pos5_x = self.pos4_x + BUTTON_WIDTH + GAP
    
    def __initiate_buttons(self):
        self.start_button = Button(ButtonType.START, self.pos1_x, self.pos_y)
        self.hit_button = Button(ButtonType.HIT, self.pos3_x, self.pos_y)
        self.stand_button = Button(ButtonType.STAND, self.pos5_x, self.pos_y)
        self.back_button = Button(ButtonType.BACK, self.pos4_x, self.pos_y)
        self.quit_button = Button(ButtonType.QUIT, self.pos2_x, self.pos_y)

    def __create_scene(self):
        self.screen.fill(TABLE_GREEN)
        self.screen.blit(self.background_img, self.background_rect)
        if (self.state == GameState.MENU):
            self.screen.blit(self.title_img, self.title_rect)
            self.quit_button.draw(self.screen)
            self.start_button.draw(self.screen)
        if (self.state == GameState.PLAYING):
            self.hit_button.draw(self.screen)
            self.back_button.draw(self.screen)
            self.stand_button.draw(self.screen)

    def __handle_action(self, action):
        if action == ButtonType.QUIT:
            self.sound.play(SoundLibrary.CLICK)
            self.running = False
        if action == ButtonType.START:
            self.sound.play(SoundLibrary.CLICK)
            self.state = GameState.PLAYING
        if action == ButtonType.BACK:
            self.sound.play(SoundLibrary.CLICK)
            self.state = GameState.MENU
        if action == ButtonType.HIT:
            self.sound.play(SoundLibrary.CHIP)
        if action == ButtonType.STAND:
            self.sound.play(SoundLibrary.CHIP)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == GameState.MENU:
                self.__handle_action(self.start_button.handle_event(event))
                self.__handle_action(self.quit_button.handle_event(event))
                
            elif self.state == GameState.PLAYING:
                self.__handle_action(self.hit_button.handle_event(event))
                self.__handle_action(self.stand_button.handle_event(event))
                self.__handle_action(self.back_button.handle_event(event))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.__create_scene()
            self.__handle_events()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

class Button:
    def __init__(self, type, x, y):
        self.type = type
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.font = pygame.font.Font("assets/casino_font.otf", 32)
        self.color = WOOD_DARK
        self.hover_color = WOOD_LIGHT
        self.text_color = WHITE

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(screen, color, self.rect, border_radius=15)

        text = self.font.render(self.type.name, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.type
        return None
    
class Mixer:
    def __init__(self):
        self.sounds_dir = "sounds"
        self.__mixer = pygame.mixer
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
    

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()