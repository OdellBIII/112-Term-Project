import pygame
from pygame.locals import *
from widgets.TextDisplay import TextDisplay

class TextInput(TextDisplay):

    def __init__(self, x, y, width, height, text, size, color):

        super().__init__(x, y, width, height, text, size, color)
        self.isFocused = False



    def onUserInput(self, event):

        if event.type == pygame.MOUSEBUTTONUP:

            self.getFocus(pygame.mouse.get_pos())

        if event.type == KEYDOWN and self.isFocused:

            pygame.time.wait(500)
            if event.key == pygame.K_BACKSPACE:

                self.setText(self.text[:-1])
                pass
            else:

                keyPressed = pygame.key.get_pressed()

                if keyPressed[pygame.K_a]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "a")
                    return
                elif keyPressed[pygame.K_b]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "b")

                elif keyPressed[pygame.K_c]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "c")

                elif keyPressed[pygame.K_d]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "d")

                elif keyPressed[pygame.K_e]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "e")

                elif keyPressed[pygame.K_f]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "f")

                elif keyPressed[pygame.K_g]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "g")

                elif keyPressed[pygame.K_h]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "h")

                elif keyPressed[pygame.K_i]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "i")

                elif keyPressed[pygame.K_j]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "j")

                elif keyPressed[pygame.K_k]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "k")

                elif keyPressed[pygame.K_l]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "l")

                elif keyPressed[pygame.K_m]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "m")

                elif keyPressed[pygame.K_n]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "n")

                elif keyPressed[pygame.K_o]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "o")

                elif keyPressed[pygame.K_p]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "p")

                elif keyPressed[pygame.K_q]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "q")

                elif keyPressed[pygame.K_r]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "r")
                elif keyPressed[pygame.K_s]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "s")
                elif keyPressed[pygame.K_t]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "t")
                elif keyPressed[pygame.K_u]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "u")
                elif keyPressed[pygame.K_v]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "v")
                elif keyPressed[pygame.K_w]:

                    # self.setText(self.text[:-1])
                    self.setText(self.text + "w")

                elif keyPressed[pygame.K_x]:

                    #self.setText(self.text[:-1])
                    self.setText(self.text + "x")

                elif keyPressed[pygame.K_y]:

                    #self.setText(self.text[:-1])
                    self.setText(self.text + "y")

                elif keyPressed[pygame.K_z]:

                    #self.setText(self.text[:-1])
                    self.setText(self.text + "z")

                elif keyPressed[pygame.K_SPACE]:

                    self.setText(self.text[:-1])
                    self.setText(self.text + " ")


    def getFocus(self, point):

        self.isFocused = self.pointInBounds(point)

