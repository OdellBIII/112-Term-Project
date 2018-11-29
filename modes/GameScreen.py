import pygame
from pygame.locals import *
from modes.Screen import Screen
from widgets.Button import Button

class GameScreen(Screen):

    def __init__(self, width, height, color):

        super().__init__(width, height, color)
        pausePanelDimensions = int(min(width * (3 / 4), height * (3 / 4)))
        self.pausePanel = Screen(pausePanelDimensions, pausePanelDimensions, (0, 0, 0))
        resumeButton = Button(pausePanelDimensions // 2, pausePanelDimensions // 2, 100, 50, "Close Window", 40)
        resumeButton.setCallBack(GameScreen.printSomething)
        self.pausePanel.add(resumeButton)
        self.pausePanel.background.get_rect(center=(width // 2, height //2))



    def render(self, drawingSurface):

        super().render(drawingSurface)

        if self.isPaused:

            drawingSurface.blit(self.pausePanel.background, \
                self.pausePanel.background.get_rect(center=(drawingSurface.get_rect().width // 2, \
                drawingSurface.get_rect().height // 2)))

            self.pausePanel.render(self.pausePanel.background)



    def on_event(self, event):

        super().on_event(event)

        if self.isPaused:

            self.pausePanel.on_event(event)


    def update(self, application):

        super().update(application)

        if self.isPaused:

            self.pausePanel.update(application)



    def printSomething(self):

        print("Foo Poo!")



