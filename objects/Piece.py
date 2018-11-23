import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece

class Piece(GamePiece):


    registryOfGamePieces = pygame.sprite.Group()

    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        super().__init__(newX, newY, newWidth, newHeight)

        self.color = newColor
        self.surface.fill(newColor)

        Piece.registryOfGamePieces.add(self)

    def __eq__(self, other):

        if isinstance(other, Piece) and self.rect == other.rect:

            return True
        else:

            return False

    def __hash__(self):

        return hash(self.getHashables())

    def __repr__(self):

        return "No name billy bob"

    def getHashables(self):

        return self.x, self.y, self.isTouched, self.width, self.height

    def update(self, application):

        if not self.isTouched:

            self.rect.move_ip(0, 20)
        else:

            self.rect.move_ip(0, 0)

        self.respondToBoundsCollision(application)
        self.collidedWithPieces()



    def respondToBoundsCollision(self, application):

        if self.rect.y + self.height >= application.height - application.scrollY:

            self.isTouched = True

        if self.rect.y >= application.height - application.scrollY:

            self.kill()
            pass

    def collidedWithPieces(self):

        listOfRects = [piece.rect for piece in Piece.registryOfGamePieces.sprites()]

        index = self.rect.collidelist(listOfRects)
        if index != -1 and Piece.registryOfGamePieces.sprites()[index] != self and isinstance(self, Piece):

            self.isTouched = True
            self.rect.y = listOfRects[index].y - self.rect.height
