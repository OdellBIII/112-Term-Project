import pygame
import random
from pygame.locals import *
from objects.Piece import Piece
from objects.Player import Player
from objects.GamePiece import GamePiece
from modes.Screen import Screen



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
        self._display_surf.fill((255, 255, 255))
        self._running = True
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 255, 255))
        self.screens = ["Start", "Play", "ScoreBoard", "Credits", "Instructions"]
        self.currentScreen = 0

        # Game Screen initialization
        self.gameScreen = Screen(self.width, self.height, (0, 255, 255))
        self.newPieceGenerationEvent = pygame.USEREVENT + 1
        pygame.time.set_timer(self.newPieceGenerationEvent, 1000)

        # Player initialization methods
        self.gameScreen.add(Player(self.width // 2, 0, 20, 50, (255, 255, 255)))

    def on_event(self, event):


        if self.currentScreen == 0:

            pass
        elif self.currentScreen == 1:

            self.gameScreen.on_event(event)

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            pass
        elif self.currentScreen == 4:

            pass

        if event.type == pygame.QUIT:
            self._running = False

        # Produces a new falling piece every second
        elif event.type == self.newPieceGenerationEvent:

            color = random.choice([(255, 255, 255), (0, 0, 255)])
            self.gameScreen.add(Piece(random.choice(list(range(0, 80*8, 80))), \
                                         -100 - self.scrollY, 80, 80, color))

        if event.type == KEYDOWN and event.key == K_p:

            self.currentScreen = 1

    def on_loop(self):

        self.clock.tick(60)

        if self.currentScreen == 0:

            pass
        elif self.currentScreen == 1:

            self.gameScreen.update(self)

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            pass
        elif self.currentScreen == 4:

            pass


    def on_render(self):

        if self.currentScreen == 0:

            pass
        elif self.currentScreen == 1:

            self._display_surf.blit(self.background, self.background.get_rect())
            self.gameScreen.render(self._display_surf)

        elif self.currentScreen == 2:

            pass
        elif self.currentScreen == 3:

            pass
        elif self.currentScreen == 4:

            pass

        pygame.display.flip()

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