
import pygame
from pygame.locals import *
from objects.GamePiece import GamePiece
# Some Wants:
# Make x, y points based on center of widget

defaultForegroundColor = (190, 190, 190)
defaultBackgroundColor = (88, 88, 88)
defaultFontColor = (0, 0, 0)

class Widget(GamePiece):

    def __init__(self, x, y, width=100, height=50):

        super().__init__(x - width // 2, y - height // 2, width, height)

        self.foregroundColor = defaultForegroundColor
        self.backgroundColor = defaultBackgroundColor
        self.fontColor = defaultFontColor
        self.visibility = True
        self.image.fill(self.foregroundColor)

    def setForegroundColor(self, foregroundColor):

        self.foregroundColor = foregroundColor

        return self

    def setBackgroundColor(self, backgroundColor):

        self.backgroundColor = backgroundColor

        return self

    def setFontColor(self, fontColor):

        self.fontColor = fontColor

        return self

    def pointInBounds(self, point):

        return self.rect.x <= point[0] <= self.rect.x + self.rect.width and \
            self.rect.y <= point[1] <= self.rect.y + self.rect.height

    def setVisibility(self, visibility):

        self.visibility = visibility

    def onUserInput(self, event):

        pass








