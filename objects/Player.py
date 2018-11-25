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
        self.gravity = 40
        self.isInAir = True
        self.jumpVelocity = -600
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

        self.collidedWithPieces()
        self.checkBounds(application.width, application.height)

    def onKeyPressed(self, event):

        if event.type == KEYDOWN:

            if event.key == pygame.K_w and not self.isInAir:

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


    def collidedWithPieces(self):

        listOfRects = [piece.rect for piece in Piece.registryOfGamePieces.sprites()]

        index = self.rect.collidelist(listOfRects)

        if index != -1 and listOfRects[index] != self.rect and \
                listOfRects[index].y + listOfRects[index].height * 0.2 < self.rect.y + self.rect.height:

            if self.rect.x > listOfRects[index].x + listOfRects[index].width * 0.8 and \
                    self.rect.x < listOfRects[index].x + listOfRects[index].width:

                self.rect.x = Piece.registryOfGamePieces.sprites()[index].x + Piece.registryOfGamePieces.sprites()[index].width
                self.velocityX = 0
                self.horizontalSpeed = 0

            elif self.rect.x + self.rect.width > Piece.registryOfGamePieces.sprites()[index].x:

                self.rect.x = Piece.registryOfGamePieces.sprites()[index].x - self.rect.width
                self.velocityX = 0
                self.horizontalSpeed = 0

        if index != -1 and self.rect.y + self.rect.height < listOfRects[index].y + listOfRects[index].height * 0.3 and \
            self.isInAir:

            print("Boop it Happened!")
            self.isInAir = False
            self.rect.y = listOfRects[index].y - self.rect.height
            self.velocityY = 0
            self.velocityX = 0
            self.horizontalSpeed = 0

