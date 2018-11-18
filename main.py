import pygame
import random
from pygame.locals import *


class Piece(pygame.sprite.Sprite):

    def __init__(self, newX, newY, newWidth, newHeight, newColor):

        pygame.sprite.Sprite.__init__(self)

        self.x = newX
        self.y = newY
        self.width = newWidth
        self.height = newHeight
        self.color = newColor
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(newColor)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.isTouched = False
        self.image = self.surface

    def __eq__(self, other):

        if isinstance(other, Piece) and self.rect == other.rect:

            return True
        else:

            return False

    def __hash__(self):

        return hash(self.getHashables())

    def __repr__(self):

        return "No name billy bob"

    def getHashables(self):

        return self.x, self.y, self.isTouched, self.width, self.height

    def update(self, application):

        if not self.isTouched:

            self.rect.move_ip(0, 20)
        else:

            self.rect.move_ip(0, application.scrollDy)

        self.respondToBoundsCollision(application)
        self.collidedWithPiece(application)

    def collidedWithPiece(self, application):

        listOfRects = [piece.rect for piece in application.groupOfPieces.sprites()]
        index = self.rect.collidelist(listOfRects)
        if index != -1 and application.groupOfPieces.sprites()[index] != self:

            self.isTouched = True
            self.rect.y = listOfRects[index].y - 50

    def respondToBoundsCollision(self, application):

        if self.rect.y + self.height >= application.height - application.scrollY:

            self.isTouched = True

        if self.rect.y >= application.height - application.scrollY:

            self.kill()
            pass

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.timer = 0
        self.listOfPieces = []
        self.groupOfPieces = pygame.sprite.Group()
        self.scrollDy = 0
        self.scrollY = 0
        self.highestPoint = self.height

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill((0, 255, 255))
        self._running = True
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 255, 255))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.timer += 1
        if self.timer % 100 == 0:

            self.groupOfPieces.update(self)

        if self.timer % 1000 == 0:

            color = random.choice([(255, 255, 255), (0, 0, 255)])
            self.groupOfPieces.add(Piece(random.randint(0, self.width - 50), -100 - self.scrollY, 50, 50, color))

        if self.timer % 1000 == 0:

            self.highestPoint = min([piece.rect.y if piece.isTouched else self.height for piece in self.groupOfPieces.sprites()])

            if self.highestPoint <= self.height // 2:

                self.scrollDy = 3

            self.scrollY += self.scrollDy

    def on_render(self):

        self._display_surf.blit(self.background, self.background.get_rect())

        self.groupOfPieces.draw(self._display_surf)

        pygame.draw.line(self._display_surf, (255, 0, 0), (0, self.height // 2), \
                         (self.width, self.height // 2), 2)
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
    theApp = App()
    theApp.on_execute()