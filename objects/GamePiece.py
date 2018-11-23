import pygame
from pygame.locals import *

class GamePiece(pygame.sprite.Sprite):


    def __init__(self, newX, newY, newWidth, newHeight):

        pygame.sprite.Sprite.__init__(self)

        self.x = newX
        self.y = newY
        self.width = newWidth
        self.height = newHeight

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = self.surface
        self.isTouched = False

    def __eq__(self, other):

        if isinstance(other, GamePiece) and self.rect == other.rect:

            return True
        else:

            return False

    def __hash__(self):

        return hash(self.getHashables())

    def __repr__(self):

        return "No name billy bob"

    def getHashables(self):

        return self.x, self.y, self.isTouched, self.width, self.height

    def collidedWithPiece(self):

        pass

