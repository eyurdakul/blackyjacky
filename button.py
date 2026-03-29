import pygame
from settings import BUTTON_HEIGHT, BUTTON_WIDTH, WOOD_DARK, WOOD_LIGHT, WHITE

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