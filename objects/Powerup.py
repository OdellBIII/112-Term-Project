
import pygame
from pygame.locals import *
from objects.Piece import Piece


class Powerup(Piece):

    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        super().__init__(newX, newY, newWidth, newHeight, newColor)
        self.isActive = False

    def __hash__(self):

        return super().__hash__()

    def update(self, application):

        if not self.isActive:

            super(Powerup, self).update(application)

        else:

            super().remove(application.gameScreen.background.get_at((0, 0)))

    def power(self):

        return "Double Jump"