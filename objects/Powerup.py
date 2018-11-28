
import pygame
from pygame.locals import *
from objects.Piece import Piece


class Powerup(Piece):

    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        super().__init__(newX, newY, newWidth, newHeight, newColor)


