import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece
from modes.GameScreen import GameScreen
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
        self.jumpVelocity = -700
        self.horizontalSpeed = 0
        self.bottomPiece = None
        self.newGround = newHeight - 40
        self.squished = False
        self.jumpCount = 0
        self.isDoubleJumpActive = False

    def move(self, deltaTime):

        deltaX = (self.velocityX * deltaTime * 0.001)
        deltaY = (self.velocityY * deltaTime * 0.001)

        self.rect.move_ip(deltaX, deltaY)


    def update(self, application):


        if self.isInAir:

            self.velocityY += self.gravity

        self.velocityX += self.horizontalSpeed

        # Add horizontal speed checker to max out speed

        self.collidedWithPowerUp(application)
        self.checkBounds(application)
        self.collidedWithPieces(application)
        self.move(application.clock.get_time())
        if self.squished:

            application.gameScreen.isPaused = True

        self.rect.move_ip(0, application.scrollDy)
        self.newGround = application.ground


    def onUserInput(self, event):

        if event.type == KEYDOWN:

            if event.key == pygame.K_w and not self.isInAir:

                self.isInAir = True
                self.velocityY += self.jumpVelocity

            if event.key == pygame.K_w and self.isDoubleJumpActive \
                    and self.jumpCount < 2:

                self.isInAir = True
                self.velocityY = 0
                self.velocityY += -700
                self.jumpCount += 1

                if self.jumpCount >= 2:

                    self.jumpCount = 0
                    self.isDoubleJumpActive = False

            if event.key == pygame.K_d:

                self.horizontalSpeed = 20

            if event.key == pygame.K_a:

                self.horizontalSpeed = -20

        elif event.type == KEYUP:

            if event.key == pygame.K_d or event.key == pygame.K_a:

                self.horizontalSpeed = 0

                if not self.isInAir:

                    self.velocityX = 0



    def checkBounds(self, application):

        if self.rect.y + self.rect.height > self.newGround:

            if self.isInAir:
                self.velocityX = 0

            self.isInAir = False
            self.rect.y = application.ground - self.rect.height - 1
            self.velocityY = 0
            self.newGround = application.ground


        if self.rect.x < 0:

            self.rect.x = 0
            self.horizontalSpeed = 0

        elif self.rect.x + self.rect.width > application.width:

            self.rect.x = application.width - self.rect.width
            self.horizontalSpeed = 0

        if self.rect.y >= application.height:

            self.squished = True



    def collidedWithPieces(self, application):

        listOfPieces = [piece for piece in application.gameScreen.gamePieceGroup.sprites() \
                       if isinstance(piece, Piece) and not isinstance(piece, Powerup)]
        listOfRects = [piece.rect for piece in listOfPieces]

        fallingPieces = [piece for piece in listOfPieces if piece.rect.y < self.rect.y]

        index = self.rect.collidelist(listOfRects)

        for piece in fallingPieces:

            if piece.rect.collidepoint(self.rect.x + (self.rect.width // 2), self.rect.y - 1) and \
                    piece.rect != self.rect and not self.isInAir and not piece.isTouched:

                self.squished = True
                return


        if index != -1 and listOfRects[index] != self.rect:


            if self.rect.y + self.rect.height >= listOfRects[index].y + listOfRects[index].height * 0.15:

                if self.rect.x + self.rect.width >= listOfRects[index].x and self.rect.x < listOfRects[index].x + listOfRects[index].width // 2:

                    self.rect.x = listOfRects[index].x - self.rect.width - 1
                    self.velocityX = 0

                if self.rect.x <= listOfRects[index].x + listOfRects[index].width and self.rect.x > listOfRects[index].x + listOfRects[index].width // 2:

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

        else:

            if self.bottomPiece != None:

                if self.newGround < application.ground and \
                        self.rect.x > self.bottomPiece.x + self.bottomPiece.width or \
                        self.rect.x + self.rect.width < self.bottomPiece.x:

                    self.isInAir = True
                    self.bottomPiece = None

    def collidedWithPowerUp(self, application):

        listOfPowerUps = [powerup for powerup in application.gameScreen.gamePieceGroup \
                          if isinstance(powerup, Powerup)]

        index = self.rect.collidelist(listOfPowerUps)
        if index != -1:

            listOfPowerUps[index].isActive = True
            self.isDoubleJumpActive = True




