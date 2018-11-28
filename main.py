import pygame
import random
from pygame.locals import *
from objects.Piece import Piece
from objects.Player import Player
from objects.GamePiece import GamePiece
from objects.Powerup import Powerup
from modes.Screen import Screen
from widgets.Button import *


class App:
    def __init__(self, newWidth, newHeight):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = newWidth, newHeight
        self.clock = pygame.time.Clock()
        self.scrollDy = 0
        self.scrollY = 0
        self.highestPoint = self.height

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((255, 0, 0))
        self._running = True
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.screens = ["Start", "Play", "ScoreBoard", "Credits", "Instructions"]
        self.currentScreen = 0

        # Start Screen initialization
        self.startScreen = Screen(self.width, self.height, (255, 255, 255))
        self.startScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Jerry's Great Climb", 40))
        startButton = Button(self.width // 2, self.height // 2, 100, 50, "Play!", 40)
        instructionButton = Button(self.width // 2, self.height // 2 + 50, 100, 50, "Instructions!", 40)
        creditsButton = Button(self.width // 2, self.height // 2 + 100, 100, 50, "Credits!", 40)

        startButton.setCallBack(self.setPlayScreen)
        instructionButton.setCallBack(self.setInstructionScreen)
        creditsButton.setCallBack(self.setCreditsScreen)
        self.startScreen.add(startButton, instructionButton, creditsButton)

        # Instruction Screen initialization
        self.instructionScreen = Screen(self.width, self.height, (255, 255, 255))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Instructions", 40))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 50, 100, 50, "W.............................Jump", 40))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 100, 100, 50, "A.............................Left", 40))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 150, 100, 50, "D.............................Right", 40))
        backButton = Button(50, 50, 100, 50, "<-", 40)
        backButton.setCallBack(self.setStartScreen)
        self.instructionScreen.add(backButton)

        # Credits Screen Initialization
        self.creditScreen = Screen(self.width, self.height, (255, 255, 255))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Credits!", 40))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4 + 50, 100, 50, "Sole Developer.............................Odell Blackmon III", 20))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4 + 100, 100, 50, "UI Designer.............................Odell Blackmon III", 20))
        creditBackButton = Button(50, 50, 100, 50, "<-", 40)
        creditBackButton.setCallBack(self.setStartScreen)
        self.creditScreen.add(creditBackButton)

        # Game Screen initialization
        self.gameScreen = Screen(self.width, self.height, (0, 255, 255))
        self.newPieceGenerationEvent = pygame.USEREVENT + 1

        # Player initialization methods
        self.gameScreen.add(Player(self.width // 2, 0, 20, 50, (255, 255, 255)))


    def on_event(self, event):


        if self.currentScreen == 0:

            self.startScreen.on_event(event)

        elif self.currentScreen == 1:

            self.gameScreen.on_event(event)

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            self.creditScreen.on_event(event)
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.on_event(event)
            pass

        if event.type == pygame.QUIT:
            self._running = False

        # Produces a new falling piece every second
        elif event.type == self.newPieceGenerationEvent:

            color = random.choice([(255, 255, 255), (0, 0, 255)])
            self.gameScreen.add(Piece(random.choice(list(range(0, 80*8, 80))), \
                                         -100 - self.scrollY, 80, 80, color))

            # self.gameScreen.add(Powerup(self.width //2, -100, 20, 20, (0, 0, 0)))
            pass

    def on_loop(self):

        self.clock.tick(60)

        if self.currentScreen == 0:

            self.startScreen.update(self)
            pass
        elif self.currentScreen == 1:

            self.gameScreen.update(self)

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            self.creditScreen.update(self)
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.update(self)
            pass


    def on_render(self):

        if self.currentScreen == 0:

            self.startScreen.render(self._display_surf)
            pygame.display.flip()

        elif self.currentScreen == 1:

            self.gameScreen.render(self._display_surf)
            pygame.display.flip()

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            self.creditScreen.render(self._display_surf)
            pygame.display.flip()
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.render(self._display_surf)
            pygame.display.flip()
            pass

    def changeScreen(self, newScreen):

        if 0 <= newScreen < len(self.screens):

            self.currentScreen = newScreen

    def setPlayScreen(self):

        self.changeScreen(1)
        pygame.time.set_timer(self.newPieceGenerationEvent, 1000)

    def setInstructionScreen(self):

        self.changeScreen(4)

    def setCreditsScreen(self):

        self.changeScreen(3)

    def setStartScreen(self):

        self.changeScreen(0)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App(400, 600)
    theApp.on_execute()