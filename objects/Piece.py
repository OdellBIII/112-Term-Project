import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece


class Piece(GamePiece):


    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        super().__init__(newX, newY, newWidth, newHeight)

        self.color = newColor
        self.surface.fill(newColor)


    def __eq__(self, other):

        if isinstance(other, Piece) and self.rect == other.rect:

            return True

        else:

            return False


    def __hash__(self):

        return super().__hash__()


    def update(self, application):

        if not self.isTouched:

            self.rect.move_ip(0, 10)

        self.respondToBoundsCollision(application)
        self.collidedWithPieces(application)
        self.rect.move_ip(0, application.scrollDy)



    def respondToBoundsCollision(self, application):

        if self.rect.y - 1000 >= application.height:

            pass

        if self.rect.y + self.height >= application.ground:

            self.isTouched = True
            self.rect.y = application.ground - self.rect.height - 1

    def collidedWithPieces(self, application):

        listOfRects = [piece.rect for piece in application.currentScreenInstance.gamePieceGroup.sprites() \
                       if isinstance(piece, Piece) and piece.__class__.__name__ == "Piece"]

        index = self.rect.collidelist(listOfRects)
        if index != -1 and \
                self.rect.y < listOfRects[index].y:

            self.isTouched = True
            self.rect.y = listOfRects[index].y - self.rect.height - 1
