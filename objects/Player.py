import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece
from modes.GameScreen import GameScreen
from objects.Piece import Piece
from objects.Powerup import Powerup


class Player(GamePiece):

    def __init__(self, newX, newY, newWidth, newHeight, newColor, player):

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
        self.horizontalPiece = None
        self.isOnWall = False
        self.newGround = newHeight - 40
        self.squished = False
        self.jumpCount = 0
        self.player = player
        self.isDoubleJumpActive = False
        self.isHighJumpActive = False

        self.isClimbing = False
        self.powerUpTimer = pygame.USEREVENT + 4

    def move(self, deltaTime):

        deltaX = (self.velocityX * deltaTime * 0.001)
        deltaY = (self.velocityY * deltaTime * 0.001)

        self.rect.move_ip(deltaX, deltaY)


    def update(self, application):

        if self.isInAir and self.isClimbing == False:

            self.velocityY += self.gravity

        self.velocityX += self.horizontalSpeed

        if self.horizontalPiece != None:

            if self.horizontalPiece.collidepoint(self.rect.x + self.rect.width + 1, self.rect.y + self.rect.height) or \
            self.horizontalPiece.collidepoint(self.rect.x - 2, self.rect.y + self.rect.height):

                pass

            else:

                self.isOnWall = False

        # Add horizontal speed checker to max out speed

        self.collidedWithPowerUp(application)
        self.checkBounds(application)
        self.collidedWithPieces(application)
        self.move(application.clock.get_time())

        if self.squished:

            application.currentScreenInstance.isPaused = True

        self.rect.move_ip(0, application.scrollDy)
        self.newGround = application.ground


    def onUserInput(self, event):

        if self.player == "first":
            if event.type == KEYDOWN:

                if event.key == pygame.K_w and not self.isInAir or self.isClimbing:

                    self.isInAir = True
                    self.isClimbing = False
                    self.velocityY += self.jumpVelocity

                if event.key == pygame.K_w and self.isDoubleJumpActive \
                    and self.jumpCount < 2:

                    self.isInAir = True
                    self.isOnWall = False
                    self.velocityY = 0
                    self.velocityY += -700
                    self.jumpCount += 1

                    if self.jumpCount >= 2:

                        self.jumpCount = 0
                        self.isDoubleJumpActive = False

                if event.key == pygame.K_w and self.isHighJumpActive:

                    self.isInAir = True
                    self.isClimbing = False
                    self.velocityY += self.jumpVelocity * 1.1
                    self.isHighJumpActive = False

                if event.key == pygame.K_d and self.isClimbing == False:

                    self.horizontalSpeed = 20

                if event.key == pygame.K_a and self.isClimbing == False:

                    self.horizontalSpeed = -20


            elif event.type == KEYUP:

                if event.key == pygame.K_d or event.key == pygame.K_a:

                    self.horizontalSpeed = 0
                    # self.isTouched = False
                    self.horizontalPiece = None

                    if not self.isInAir:

                        self.velocityX = 0


                if event.key == pygame.K_f and self.isClimbing:

                    self.isClimbing = False
                    self.isInAir = True

        elif self.player == "second":

            if event.type == KEYDOWN:

                if event.key == pygame.K_UP and not self.isInAir or self.isClimbing:
                    self.isInAir = True
                    self.isClimbing = False
                    self.velocityY += self.jumpVelocity

                if event.key == pygame.K_UP and self.isDoubleJumpActive \
                        and self.jumpCount < 2:

                    self.isInAir = True
                    self.isOnWall = False
                    self.velocityY = 0
                    self.velocityY += -700
                    self.jumpCount += 1

                    if self.jumpCount >= 2:
                        self.jumpCount = 0
                        self.isDoubleJumpActive = False

                if event.key == pygame.K_UP and self.isHighJumpActive:
                    self.isInAir = True
                    self.isClimbing = False
                    self.velocityY += self.jumpVelocity * 1.1
                    self.isHighJumpActive = False

                if event.key == pygame.K_RIGHT and self.isClimbing == False:
                    self.horizontalSpeed = 20

                if event.key == pygame.K_LEFT and self.isClimbing == False:
                    self.horizontalSpeed = -20


            elif event.type == KEYUP:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:

                    self.horizontalSpeed = 0
                    self.horizontalPiece = None

                    if not self.isInAir:
                        self.velocityX = 0

                if event.key == pygame.K_m and self.isClimbing:
                    self.isClimbing = False
                    self.isInAir = True

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

        if self.player == "first":
            listOfPieces = [piece for piece in application.currentScreenInstance.gamePieceGroup.sprites() \
                           if isinstance(piece, Piece) and not isinstance(piece, Powerup)]

            listOfRects = [piece.rect for piece in listOfPieces]

            fallingPieces = [piece for piece in listOfPieces if piece.rect.y < self.rect.y]

            index = self.rect.collidelist(listOfRects)

            for piece in fallingPieces:

                if piece.rect.collidepoint(self.rect.x + (self.rect.width // 2), self.rect.y - 1) and \
                        piece.rect != self.rect and not self.isInAir and not piece.isTouched:

                    self.squished = True
                    # self.isTouched = True
                    return


            if index != -1 and listOfRects[index] != self.rect:


                if self.rect.y + self.rect.height >= listOfRects[index].y + listOfRects[index].height * 0.15:

                    if self.rect.x < listOfRects[index].x + listOfRects[index].width and self.rect.x > listOfRects[index].x + listOfRects[index].width // 2:

                        self.rect.x = listOfRects[index].x + listOfRects[index].width + 1
                        self.velocityX = 0
                        self.horizontalPiece = listOfRects[index]

                        if pygame.key.get_pressed()[pygame.K_f]:
                            self.isClimbing = True
                            self.velocityY = 0
                            self.velocityX = 0
                            self.isInAir = False

                    if self.rect.x + self.rect.width > listOfRects[index].x and self.rect.x < listOfRects[index].x + listOfRects[index].width // 2:

                        self.rect.x = listOfRects[index].x - self.rect.width
                        self.velocityX = 0
                        self.horizontalPiece = listOfRects[index]

                        if pygame.key.get_pressed()[pygame.K_f]:
                            self.isClimbing = True
                            self.velocityY = 0
                            self.velocityX = 0
                            self.isInAir = False

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

                    if self.rect.x > self.bottomPiece.x + self.bottomPiece.width or \
                        self.rect.x + self.rect.width < self.bottomPiece.x:

                        self.isInAir = True
                        self.isOnWall = False
                        self.isClimbing = False
                        self.bottomPiece = None

        elif self.player == "second":

            listOfPieces = [piece for piece in application.currentScreenInstance.gamePieceGroup.sprites() \
                            if isinstance(piece, Piece) and not isinstance(piece, Powerup)]

            listOfRects = [piece.rect for piece in listOfPieces]

            fallingPieces = [piece for piece in listOfPieces if piece.rect.y < self.rect.y]

            index = self.rect.collidelist(listOfRects)

            for piece in fallingPieces:

                if piece.rect.collidepoint(self.rect.x + (self.rect.width // 2), self.rect.y - 1) and \
                        piece.rect != self.rect and not self.isInAir and not piece.isTouched:
                    self.squished = True
                    # self.isTouched = True
                    return

            if index != -1 and listOfRects[index] != self.rect:

                if self.rect.y + self.rect.height >= listOfRects[index].y + listOfRects[index].height * 0.15:

                    if self.rect.x < listOfRects[index].x + listOfRects[index].width and self.rect.x > listOfRects[
                        index].x + listOfRects[index].width // 2:

                        self.rect.x = listOfRects[index].x + listOfRects[index].width + 1
                        self.velocityX = 0
                        self.horizontalPiece = listOfRects[index]

                        if pygame.key.get_pressed()[pygame.K_m]:
                            self.isClimbing = True
                            self.velocityY = 0
                            self.velocityX = 0
                            self.isInAir = False

                    if self.rect.x + self.rect.width > listOfRects[index].x and self.rect.x < listOfRects[index].x + \
                            listOfRects[index].width // 2:

                        self.rect.x = listOfRects[index].x - self.rect.width
                        self.velocityX = 0
                        self.horizontalPiece = listOfRects[index]

                        if pygame.key.get_pressed()[pygame.K_m]:
                            self.isClimbing = True
                            self.velocityY = 0
                            self.velocityX = 0
                            self.isInAir = False

                if listOfRects[index].x <= self.rect.x <= listOfRects[index].x + listOfRects[index].width or \
                        listOfRects[index].x <= self.rect.x + self.rect.width <= listOfRects[index].x + listOfRects[
                    index].width and \
                        self.rect.y + self.rect.height < listOfRects[index].y and self.isInAir and self.newGround != \
                        listOfRects[index].y:
                    self.isInAir = False
                    self.rect.y = listOfRects[index].y - self.rect.height - 1
                    self.velocityY = 0
                    self.velocityX = 0
                    self.newGround = listOfRects[index].y
                    self.bottomPiece = listOfRects[index]
            else:

                if self.bottomPiece != None:

                    if self.rect.x > self.bottomPiece.x + self.bottomPiece.width or \
                            self.rect.x + self.rect.width < self.bottomPiece.x:
                        self.isInAir = True
                        self.isOnWall = False
                        self.isClimbing = False
                        self.bottomPiece = None

    def collidedWithPowerUp(self, application):

        listOfPowerUps = [powerup for powerup in application.currentScreenInstance.gamePieceGroup \
                          if isinstance(powerup, Powerup)]

        index = self.rect.collidelist(listOfPowerUps)
        if index != -1:

            if listOfPowerUps[index].power == "Double Jump":

                listOfPowerUps[index].isActive = True
                self.isDoubleJumpActive = True

            elif listOfPowerUps[index].power == "High Jump":

                listOfPowerUps[index].isActive = True
                self.isHighJumpActive = True


            pygame.time.set_timer(self.powerUpTimer, 10000)




