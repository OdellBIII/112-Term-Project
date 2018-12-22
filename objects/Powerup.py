
import pygame
from pygame.locals import *
from objects.Piece import Piece


class Powerup(Piece):

    def __init__(self, newX, newY, newWidth, newHeight, newColor, powerUpType):

        super().__init__(newX, newY, newWidth, newHeight, newColor)
        self.isActive = False
        self.power = powerUpType

    def __hash__(self):

        return super().__hash__()

    def update(self, application):

        if not self.isActive:

            super(Powerup, self).update(application)

        else:

            self.remove(application.currentScreenInstance.background.get_at((0, 0)))

    def remove(self, color):

        self.rect = pygame.rect.Rect((0, 0), (0, 0))
        self.image.fill(color)

