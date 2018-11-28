import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece
from objects.Piece import Piece
from objects.Powerup import Powerup


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
        self.bottomPiece = None
        self.newGround = 600

    def move(self, deltaTime, horizontalBound, verticalBound):

        deltaX = (self.velocityX * deltaTime * 0.001)
        deltaY = self.velocityY * deltaTime * 0.001

        self.rect.move_ip(deltaX, deltaY)


    def update(self, application):


        if self.isInAir:

            self.velocityY += self.gravity

        self.velocityX += self.horizontalSpeed

        # Add horizontal speed checker to max out speed

        self.checkBounds(application.width, application.height)
        self.collidedWithPieces(application.width, application.height)
        self.move(application.clock.get_time(), application.width, application.height)

    def onUserInput(self, event):

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
            self.rect.y = height - self.rect.height - 1
            self.velocityY = 0
            self.newGround = height


        if self.rect.x < 0:

            self.rect.x = 0
            self.horizontalSpeed = 0

        elif self.rect.x + self.rect.width > width:

            self.rect.x = width - self.rect.width
            self.horizontalSpeed = 0



    def collidedWithPieces(self, width, height):

        listOfRects = [piece.rect for piece in Piece.registryOfGamePieces.sprites()]

        index = self.rect.collidelist(listOfRects)

        if index != -1:

            if self.rect.y + self.rect.height >= listOfRects[index].y + listOfRects[index].height * 0.2:

                if self.rect.x + self.rect.width >= listOfRects[index].x and self.rect.x < listOfRects[index].x + listOfRects[index].width // 2:

                    self.rect.x = listOfRects[index].x - self.rect.width - 2
                    self.velocityX = 0

                elif self.rect.x <= listOfRects[index].x + listOfRects[index].width and self.rect.x > listOfRects[index].x + listOfRects[index].width // 2:

                    self.rect.x = listOfRects[index].x + listOfRects[index].width + 1
                    self.velocityX = 0


            if listOfRects[index].x <= self.rect.x <= listOfRects[index].x + listOfRects[index].width or \
                        listOfRects[index].x <= self.rect.x + self.rect.width <= listOfRects[index].x + listOfRects[index].width and \
                    self.rect.y + self.rect.height < listOfRects[index].y and self.isInAir and self.newGround != listOfRects[index].y:

                self.isInAir = False
                self.rect.y = listOfRects[index].y - self.rect.height - 1
                self.velocityY = 0
                self.velocityX = 0
                self.newGround = listOfRects[index].y
                self.bottomPiece = listOfRects[index]

        # if index != -1 and isinstance(Piece.registryOfGamePieces.sprites()[index], Powerup):
        #
        #     listOfRects[index].remove(Piece.registryOfGamePieces)

        else:

            if self.bottomPiece != None:

                if self.newGround < height and self.bottomPiece != None and \
                        self.rect.x > self.bottomPiece.x + self.bottomPiece.width or \
                        self.rect.x + self.rect.width < self.bottomPiece.x:

                    self.isInAir = True
                    self.bottomPiece = None





