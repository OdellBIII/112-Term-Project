import pygame
from pygame.locals import *

# Referenced this url for how to use Sprites and Groups: https://www.pygame.org/docs/ref/sprite.html
# Referenced this url for how to use Rects in Pygame: https://www.pygame.org/docs/ref/rect.html
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

        return super().__hash__()

    def getHashables(self):

        return self.x, self.y, self.isTouched, self.width, self.height, self.image

    def collidedWithPieces(self):

        pass

    def onUserInput(self, event):

        pass

