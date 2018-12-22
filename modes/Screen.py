import pygame
from objects.GamePiece import GamePiece
from widgets.Widget import Widget
from widgets.TextInput import TextInput

class Screen(object):

    def __init__(self, width, height, color):

        self.gamePieceGroup = pygame.sprite.Group()
        self.userInterfaceGroup = pygame.sprite.Group()
        self.background = pygame.Surface((width, height))
        self.background.fill(color)
        self.isPaused = False
        self.isRunning = True
        self.width = width
        self.height = height
        self.color = color
        self.lock = False

    def add(self, *args):

        if not self.lock:

            for arg in args:

                if isinstance(arg, GamePiece):

                    self.gamePieceGroup.add(arg)

    def addUI(self, *args):

        for arg in args:

            if isinstance(arg, Widget):

                self.userInterfaceGroup.add(arg)

    def update(self, application):

        if self.isRunning:

            if not self.isPaused:

                self.gamePieceGroup.update(application)
                self.userInterfaceGroup.update(application)

    def render(self, drawingSurface):

        if self.isRunning:

            drawingSurface.blit(self.background, self.background.get_rect())
            self.gamePieceGroup.draw(drawingSurface)




    def pauseScreen(self):

        self.isPaused = True

    def unPauseScreen(self):

        self.isPaused = False

    def on_event(self, event):

        for gamePiece in self.gamePieceGroup:

            gamePiece.onUserInput(event)

