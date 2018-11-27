
import pygame
from pygame.locals import *
from widgets.TextDisplay import TextDisplay


# Some wants:
# Add in automatic padding
# Add in hover color change
# Add in click color change

class Button(TextDisplay):

    def __init__(self, x, y, width, height, text, size, color=(0, 0, 0)):

        super().__init__(x, y, width, height, text, size, color)
        self.textSurface = pygame.font.Font(None, size).render(text, True, color, self.foregroundColor)
        self.image = self.textSurface
        self.callback = None
        self.callbackArgs = None

    def setCallBack(self, callBack):

        self.callback = callBack
        return self

    def onUserInput(self, event):

        if event.type == MOUSEBUTTONUP and self.pointInBounds(pygame.mouse.get_pos()) and callable(self.callback):

            self.callback()