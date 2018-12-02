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

            self.rect.move_ip(0, 5)

        self.respondToBoundsCollision(application)
        self.collidedWithPieces(application)
        self.rect.move_ip(0, application.scrollDy)



    def respondToBoundsCollision(self, application):

        if self.rect.y - 100 >= application.height:

            super().remove(application.gameScreen.background.get_at((0, 0)))

            pass

        if self.rect.y + self.height >= application.ground:

            self.isTouched = True
            self.rect.y = application.ground - self.height

    def collidedWithPieces(self, application):

        listOfRects = [piece.rect for piece in application.gameScreen.gamePieceGroup.sprites() \
                       if isinstance(piece, Piece) and not isinstance(piece, Powerup)]

        index = self.rect.collidelist(listOfRects)
        if index != -1 and application.gameScreen.gamePieceGroup.sprites()[index] != self and \
                isinstance(application.gameScreen.gamePieceGroup.sprites()[index], Piece) and self.rect.y < listOfRects[index].y:

            self.isTouched = True
            self.rect.y = listOfRects[index].y - self.rect.height
