import pygame
import os
from settings import CARD_WIDTH, CARD_HEIGHT

class CardRenderer:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 20, bold=True)

        self.suit_images = {
            "HEARTS": pygame.image.load(os.path.join("assets/suits", "hearts.png")).convert_alpha(),
            "DIAMONDS": pygame.image.load(os.path.join("assets/suits", "diamonds.png")).convert_alpha(),
            "CLUBS": pygame.image.load(os.path.join("assets/suits", "clubs.png")).convert_alpha(),
            "SPADES": pygame.image.load(os.path.join("assets/suits", "spades.png")).convert_alpha(),
        }

        for k in self.suit_images:
            self.suit_images[k] = pygame.transform.scale(self.suit_images[k], (15, 15))

    def draw_card(self, screen, card, x, y):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=8)

        suit_key = card.suit.name
        suit_img = self.suit_images[suit_key]

        color = (200, 0, 0) if suit_key in ["HEARTS", "DIAMONDS"] else (0, 0, 0)

        rank_text = self.font.render(card.rank, True, color)

        screen.blit(rank_text, (x + 5, y + 5))
        screen.blit(suit_img, (x + 5, y + 25))

        screen.blit(rank_text, (x + CARD_WIDTH - 20, y + 5))
        screen.blit(suit_img, (x + CARD_WIDTH - 20, y + 25))

        screen.blit(rank_text, (x + 5, y + CARD_HEIGHT - 40))
        screen.blit(suit_img, (x + 5, y + CARD_HEIGHT - 20))

        screen.blit(rank_text, (x + CARD_WIDTH - 20, y + CARD_HEIGHT - 40))
        screen.blit(suit_img, (x + CARD_WIDTH - 20, y + CARD_HEIGHT - 20))