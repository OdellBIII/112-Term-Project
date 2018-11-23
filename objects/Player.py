import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece
from objects.Piece import Piece


class Player(GamePiece):

    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        super().__init__(newX, newY, newWidth, newHeight)

        self.velocityX = 0
        self.velocityY = 0
        self.color = newColor
        self.surface.fill(self.color)
        self.gravity = 20
        self.isInAir = True
        self.jumpVelocity = -500
        self.horizontalSpeed = 0

    def move(self, deltaTime, horizontalBound, verticalBound):

        deltaX = (self.velocityX * deltaTime * 0.001)
        deltaY = self.velocityY * deltaTime * 0.001

        self.rect.move_ip(deltaX, deltaY)


    def update(self, application):

        if self.isInAir:

            self.velocityY += self.gravity

        self.velocityX += self.horizontalSpeed

        self.move(application.clock.get_time(), application.width, application.height)

        self.checkBounds(application.width, application.height)
        self.collidedWithPieces()

    def onKeyPressed(self, event):

        if event.type == KEYDOWN:

            if event.key == pygame.K_w:

                self.isInAir = True
                self.velocityY += self.jumpVelocity

            if event.key == pygame.K_d:

                self.horizontalSpeed = 20

            if event.key == pygame.K_a:

                self.horizontalSpeed = -20

        elif event.type == KEYUP:

            if event.key == pygame.K_d or event.key == pygame.K_a:

                self.horizontalSpeed = 0

                if not self.isInAir:

                    self.velocityX = 0



    def checkBounds(self, width, height):

        listOfRects = [piece.rect for piece in Piece.registryOfGamePieces.sprites() if piece.rect.y == self.rect.y + self.rect.height]

        if self.rect.y + self.rect.height > height:

            if self.isInAir:
               self.velocityX = 0
            self.isInAir = False
            self.rect.y = height - self.rect.height
            self.velocityY = 0

        if self.rect.x < 0:

            self.rect.x = 0

        elif self.rect.x + self.rect.width > width:

            self.rect.x = width - self.rect.width

        for piece in listOfRects:

            if self.rect.x < piece.x or self.rect.x > piece.x + piece.width:

                self.isInAir = True


    def collidedWithPieces(self):

        listOfRects = [piece.rect for piece in Piece.registryOfGamePieces.sprites()]

        index = self.rect.collidelist(listOfRects)
        if index != -1 and Piece.registryOfGamePieces.sprites()[index].rect != self.rect and self.isInAir and Piece.registryOfGamePieces.sprites()[index].isTouched:

            self.isTouched = True
            self.isInAir = False
            self.velocityY = 0
            self.rect.y = listOfRects[index].y - self.rect.height
