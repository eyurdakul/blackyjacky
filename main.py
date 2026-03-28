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

TABLE_GREEN = (16, 102, 58)

WOOD = (139, 69, 19)
WOOD_LIGHT = (160, 82, 45)
WOOD_DARK = (101, 51, 15)

GOLD = (212, 175, 55)
WHITE = (255, 255, 255)

GAP = 40
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 60

class BlackjackGame:
    def __init__(self, width=1024, height=768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.__initiate_positions()
        self.__initiate_buttons()
        self.__initiate_title()
        self.running = True

    def __initiate_title(self):
        self.title_img = pygame.image.load(
            os.path.join("assets", "title.png")
        ).convert_alpha()
        self.title_rect = self.title_img.get_rect(center=(self.center_x, self.center_y - 50))

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
        self.screen.blit(self.title_img, self.title_rect)
        if (self.state == GameState.MENU):
            self.quit_button.draw(self.screen)
            self.start_button.draw(self.screen)
        if (self.state == GameState.PLAYING):
            self.hit_button.draw(self.screen)
            self.back_button.draw(self.screen)
            self.stand_button.draw(self.screen)

    def __handle_action(self, action):
        if action == ButtonType.QUIT:
            self.running = False
        if action == ButtonType.START:
            self.state = GameState.PLAYING
        if action == ButtonType.BACK:
            self.state = GameState.MENU

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

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()