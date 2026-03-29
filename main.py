import pygame
import sys, os
from enums import *
from settings import *
from mixer import Mixer
from button import Button

class BlackjackGame:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.sound = Mixer(pygame.mixer)
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

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()