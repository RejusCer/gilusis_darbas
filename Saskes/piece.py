from .constants import SQUARE_SIZE, GREY, RED
import pygame
import random


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.pictureIndex = None

    def make_king(self):
        self.king = True

    def draw(self, win, boughtProducts):  # nupiesia saske
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        if not self.king:
            if len(boughtProducts) != 0 and self.color == RED:
                if self.pictureIndex is None:
                    self.pictureIndex = random.randint(0, len(boughtProducts) - 1)

                CROWN = pygame.transform.scale(pygame.image.load(
                   'assets/' + boughtProducts[self.pictureIndex]), (45, 45))
                win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_width() // 2))


        else: # jei karalius
            CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (45, 45))
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_width() // 2))

    def move(self, row, col): #pakeicia saskes koordinates
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):  # apskaiciuoja saskes centra
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
