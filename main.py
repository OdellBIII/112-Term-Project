# I used this template for the App class:
# http://pygametutorials.wikidot.com/tutorials-basic


import pygame
import random
from pygame.locals import *
from objects.Piece import Piece
from objects.Player import Player
from objects.GamePiece import GamePiece
from objects.Powerup import Powerup
from modes.Screen import Screen
from modes.GameScreen import GameScreen
from widgets.Button import *
from widgets.TextInput import TextInput



class App:
    def __init__(self, newWidth, newHeight):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = newWidth, newHeight
        self.clock = pygame.time.Clock()

        # Scrolling configuration
        self.scrollDy = 0
        self.scrollY = 0
        self.ground = self.height * (9 / 10)
        self.scrollEvent = pygame.USEREVENT + 2


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((255, 0, 0))
        self._running = True
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.screens = ["Start", "Player Selection", "Play", "End", "ScoreBoard", "Credits", "Instructions", "Practice"]
        self.currentScreen = 0
        self.currentScreenInstance = None

        # Start Screen initialization
        self.startScreen = Screen(self.width, self.height, (255, 255, 255))
        self.startScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Jerry's Great Climb", 40))
        startButton = Button(self.width // 2, self.height // 2, 100, 50, "Play!", 40)
        practiceButton = Button(self.width // 2, self.height // 2 + 50, 100, 50, "Practice", 40)
        instructionButton = Button(self.width // 2, self.height // 2 + 100, 100, 50, "Instructions!", 40)
        creditsButton = Button(self.width // 2, self.height // 2 + 150, 200, 50, "Credits!", 40)

        startButton.setCallBack(self.setPlayerSelectionScreen)
        instructionButton.setCallBack(self.setInstructionScreen)
        practiceButton.setCallBack(self.setPracticeScreen)
        creditsButton.setCallBack(self.setCreditsScreen)
        self.startScreen.add(startButton, instructionButton, creditsButton, practiceButton)
        self.currentScreenInstance = self.startScreen

        # Instruction Screen initialization
        self.instructionScreen = Screen(self.width, self.height, (255, 255, 255))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 - 100, 100, 50, "Instructions", 40))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 - 75, 100, 50, "W/UP.............................Jump", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 -50, 100, 50, "A/Left.............................Left", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 - 25, 100, 50, "D/Right.............................Right", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "F/M............Climb", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 25, 100, 50, "Objective", 30))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 50, 100, 50, "Spend the most time on screen while dodging falling blocks.", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 75, 100, 50, "Climb onto fallen pieces by pressing in the direction of the block", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 100, 100, 50, "holding down F/M if you are first or second player respectively.", 20))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 125, 100, 50, "Enter the practice screen to practice climbing and using powerups.", 18))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 150, 100, 50, "Powerups", 30))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 175, 100, 50,"Each power up is one use only. The orange power up is High Jump,", 18))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 200, 100, 50, "and the green power up is double jump.", 18))
        self.instructionScreen.add(TextDisplay(self.width // 2, self.height // 4 + 250, 100, 50, "Press 1 or 2 to access the power ups in the practice screen.", 18))
        backButton = Button(50, 50, 100, 50, "<-", 40)
        backButton.setCallBack(self.setStartScreen)
        self.instructionScreen.add(backButton)

        # Practice Screen Initializaiton

        self.practiceScreen = GameScreen(self.width, self.height, (0, 255, 255))

        # Credits Screen Initialization
        self.creditScreen = Screen(self.width, self.height, (255, 255, 255))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Credits!", 40))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4 + 50, 100, 50, "Sole Developer.............................Odell Blackmon III", 20))
        self.creditScreen.add(TextDisplay(self.width // 2, self.height // 4 + 100, 100, 50, "UI Designer.............................Odell Blackmon III", 20))
        creditBackButton = Button(50, 50, 100, 50, "<-", 40)
        creditBackButton.setCallBack(self.setStartScreen)
        self.creditScreen.add(creditBackButton)

        # Player Screen initialization

        self.playerScreen = Screen(self.width, self.height, (255, 255, 255))
        onePlayerButton = Button(self.width // 2 - 50, self.height // 2, 100, 50, "1P", 40)
        twoPlayerButton = Button(self.width // 2 + 50, self.height // 2, 100, 50, "2P", 40)

        onePlayerButton.setCallBack(self.setPlayScreen)
        twoPlayerButton.setCallBack(self.setPlay2Screen)

        self.playerScreen.add(onePlayerButton, twoPlayerButton)

        # Game Screen initialization
        self.gameScreen = GameScreen(self.width, self.height, (0, 255, 255))
        self.newPieceGenerationEvent = pygame.USEREVENT + 1
        self.newPowerUpGenerationEvent = pygame.USEREVENT + 3
        # Player initialization methods


        # End Game Screen initialization

        self.endScreen = Screen(self.width, self.height, (255, 255, 255))


    def on_event(self, event):


        if self.currentScreen == 0:

            self.startScreen.on_event(event)

        elif self.currentScreen == 1:

            self.gameScreen.on_event(event)

        elif self.currentScreen == 2:

            self.endScreen.on_event(event)
            pass
        elif self.currentScreen == 3:

            self.creditScreen.on_event(event)
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.on_event(event)
            pass

        elif self.currentScreen == 5:

            self.playerScreen.on_event(event)

        elif self.currentScreen == 6:

            self.practiceScreen.on_event(event)

            if event.type == KEYDOWN:

                if event.key == pygame.K_1:

                    self.practiceScreen.add(Powerup(self.width - 50, -100 - self.scrollY, 20, 20, (0, 255, 0), "Double Jump"))

                elif event.key == pygame.K_2:

                    self.practiceScreen.add(Powerup(self.width - 50, -100 - self.scrollY, 20, 20, (255, 255, 0), "High Jump"))


        if event.type == pygame.QUIT:
            self._running = False

        # Produces a new falling piece every second
        if event.type == self.newPieceGenerationEvent:

            color = random.choice([(255, 255, 255), (0, 0, 255)])

            self.gameScreen.add(Piece(random.choice(list(range(0, 80*5, 80))) + 10, \
                                          - 100 - self.scrollY, 40, 100, color))

        if event.type == self.newPowerUpGenerationEvent:

            power = random.choice([((255, 255, 0), "High Jump"), ((0, 255, 0), "Double Jump")])

            self.gameScreen.add(Powerup(random.choice(list(range(0, 80 * 5, 80))) - 10, \
                                        -300 - self.scrollY, 20, 20, power[0], power[1]))


        if event.type == self.scrollEvent:

            self.scrollDy = 1
            pygame.time.set_timer(self.scrollEvent, 0)
            pass


    def on_loop(self):

        self.clock.tick(60)

        if self.currentScreen == 0:

            self.startScreen.update(self)
            pass
        elif self.currentScreen == 1:

            self.gameScreen.update(self)

        elif self.currentScreen == 2:

            self.endScreen.update(self)
            pass
        elif self.currentScreen == 3:

            self.creditScreen.update(self)
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.update(self)
            pass

        elif self.currentScreen == 5:

            self.playerScreen.update(self)

        elif self.currentScreen == 6:

            self.practiceScreen.update(self)

        self.ground += self.scrollDy
        self.scrollY += self.scrollDy

    def on_render(self):

        if self.currentScreen == 0:

            self.startScreen.render(self._display_surf)
            pygame.display.flip()

        elif self.currentScreen == 1:

            self.gameScreen.render(self._display_surf)
            pygame.display.flip()

        elif self.currentScreen == 2:

            self.endScreen.render(self._display_surf)
            pygame.display.flip()
            pass
        elif self.currentScreen == 3:

            self.creditScreen.render(self._display_surf)
            pygame.display.flip()
            pass
        elif self.currentScreen == 4:

            self.instructionScreen.render(self._display_surf)
            pygame.display.flip()
            pass

        elif self.currentScreen == 5:

            self.playerScreen.render(self._display_surf)
            pygame.display.flip()

        elif self.currentScreen == 6:

            self.practiceScreen.render(self._display_surf)
            pygame.display.flip()

    def changeScreen(self, newScreen):

        if 0 <= newScreen < len(self.screens):

            self.currentScreen = newScreen

    def setPlayScreen(self):

        self.currentScreenInstance = self.gameScreen
        self.gameScreen.isPaused = False
        self.gameScreen.timer = 0
        self.scrollY = 0
        self.ground = self.height
        self.scrollDy = 0
        self.gameScreen.timer = 0
        color = random.choice([(255, 255, 255), (0, 0, 255)])

        self.gameScreen.add(Piece(random.choice(list(range(0, 80 * 5, 80))) + 10, \
                                  - 100 - self.scrollY, 40, 100, color))
        #self.gameScreen.add(Player(self.width // 2, 0, 20, 50, (255, 255, 255), "first"))
        pygame.time.set_timer(self.newPieceGenerationEvent, 300)
        pygame.time.set_timer(self.newPowerUpGenerationEvent, 5000)
        pygame.time.set_timer(self.scrollEvent, 5000)
        self.changeScreen(1)

    def setPlay2Screen(self):

        self.currentScreenInstance = self.gameScreen
        self.gameScreen.gamePieceGroup = pygame.sprite.Group()
        self.gameScreen.timer = 0
        self.gameScreen.add(Player(3, 0, 20, 50, (255, 255, 255), "first"))
        self.gameScreen.add(Player(self.width - 20, 0, 20, 50, (255, 0, 0), "second"))
        pygame.time.set_timer(self.newPieceGenerationEvent, 300)
        pygame.time.set_timer(self.newPowerUpGenerationEvent, 5000)
        pygame.time.set_timer(self.scrollEvent, 5000)
        pygame.time.set_timer(self.newPieceGenerationEvent, 300)
        self.changeScreen(1)

    def setInstructionScreen(self):

        self.currentScreenInstance = self.instructionScreen
        self.changeScreen(4)

    def setCreditsScreen(self):

        self.currentScreenInstance = self.creditScreen
        self.changeScreen(3)

    def setStartScreen(self):

        self.currentScreenInstance = self.startScreen
        self.changeScreen(0)

    def setPracticeScreen(self):

        self.currentScreenInstance = self.practiceScreen

        self.practiceScreen.gamePieceGroup = pygame.sprite.Group()
        color = random.choice([(255, 255, 255), (0, 0, 255)])

        self.practiceScreen.add(Player(self.width // 2 - 100, 0, 20, 50, (255, 255, 255), "first"))

        self.practiceScreen.add(Piece(self.width / 2, \
                                  -100 - self.scrollY, 40, 100, color))

        self.practiceScreen.add(Piece(self.width / 2, \
                                  -300 - self.scrollY, 40, 100, color))

        practiceScreenBackButton = Button(50, 50, 50, 50, "<-", 40)
        practiceScreenBackButton.setCallBack(self.setStartScreen)
        self.practiceScreen.add(practiceScreenBackButton)
        self.practiceScreen.timer = 0
        self.practiceScreen.isPaused = False
        self.changeScreen(6)


    def setEndScreen(self):

        self.endScreen.gamePieceGroup = pygame.sprite.Group()
        score = self.gameScreen.timer
        self.currentScreenInstance = self.endScreen
        self.endScreen.add(TextDisplay(self.width // 2, self.height // 4 + 100, \
            100, 50, "You lasted: " + str(score / 100) + "s", 40))
        self.endScreen.add(TextDisplay(self.width // 2, self.height // 4, 100, 50, "Game Over!!", 40))
        submitScoreButton = Button(self.width // 2, self.height // 4 + 50, 100, 50, "Return to Main Screen!!", 40)
        submitScoreButton.setCallBack(self.setStartScreen)
        self.endScreen.add(submitScoreButton)
        self.changeScreen(2)

    def setPlayerSelectionScreen(self):

        self.currentScreenInstance = self.playerScreen
        playerScreenBackButton = Button(50, 50, 50, 50, "<-", 40)
        playerScreenBackButton.setCallBack(self.setStartScreen)
        self.playerScreen.add(playerScreenBackButton)
        self.changeScreen(5)

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