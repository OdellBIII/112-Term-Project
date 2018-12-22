import pygame
from pygame.locals import *
from modes.Screen import Screen
from widgets.Button import Button
from widgets.TextDisplay import TextDisplay
class GameScreen(Screen):

    def __init__(self, width, height, color):

        super().__init__(width, height, color)
        # Clock
        self.timer = 0

    def render(self, drawingSurface):


        if not self.isPaused:

            super().render(drawingSurface)
            score = pygame.font.Font(None, 20).render(str(self.timer / 100), True, (0, 0, 0))
            drawingSurface.blit(score, (self.width - 50, 25))


    def on_event(self, event):


        if self.isPaused:

            pass

        else:

            super().on_event(event)


    def update(self, application):


        if self.isPaused:

            pygame.time.set_timer(application.newPieceGenerationEvent, 0)
            pygame.time.set_timer(application.newPowerUpGenerationEvent, 0)
            pygame.time.set_timer(application.scrollEvent, 0)
            self.gamePieceGroup = pygame.sprite.Group()
            self.isPaused = False
            application.setEndScreen()

        else:

            super().update(application)
            self.timer += 1
            piecesToRemove = []
            for piece in self.gamePieceGroup.sprites():

                if piece.rect.y > application.height:

                    self.gamePieceGroup.remove(piece)





