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

TABLE_GREEN = (16, 102, 58)

WOOD = (139, 69, 19)
WOOD_LIGHT = (160, 82, 45)
WOOD_DARK = (101, 51, 15)

GOLD = (212, 175, 55)
WHITE = (255, 255, 255)

class BlackjackGame:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.__initiate_buttons()
        self.__initiate_title()
        self.running = True

    def __initiate_title(self):
        self.title_img = pygame.image.load(
            os.path.join("assets", "title.png")
        ).convert_alpha()
        self.title_rect = self.title_img.get_rect(center=(self.width // 2, 80))

    def __initiate_buttons(self):
        self.start_button = Button(ButtonType.START, 300, 150)
        self.hit_button = Button(ButtonType.HIT, 300, 250)
        self.stand_button = Button(ButtonType.STAND, 300, 350)
        self.quit_button = Button(ButtonType.QUIT, 300, 450)

    def __create_scene(self):
        self.screen.fill(TABLE_GREEN)
        if (self.state == GameState.MENU):
            self.screen.blit(self.title_img, self.title_rect)
            self.quit_button.draw(self.screen)

    def __handle_action(self, action):
        if action == ButtonType.QUIT:
            self.running = False

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.__handle_action(self.quit_button.handle_event(event))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.__create_scene()
            self.__handle_events()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

class Button:
    def __init__(self, type, x, y, width=180, height=60):
        self.type = type
        self.rect = pygame.Rect(x, y, width, height)
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

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()