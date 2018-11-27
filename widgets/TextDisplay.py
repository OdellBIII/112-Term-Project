
import pygame
from pygame.locals import *
from widgets.Widget import Widget

class TextDisplay(Widget):

    def __init__(self, x, y, width, height, text, size, color=(0, 0, 0)):

        self.textSurface = pygame.font.Font(None, size).render(text, True, color)
        super().__init__(x, y, self.textSurface.get_rect().width, self.textSurface.get_rect().height)
        self.image = self.textSurface