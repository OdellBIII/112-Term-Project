import pygame
import random
from pygame.locals import *
from objects.Piece import Piece
from objects.Player import Player
from objects.GamePiece import GamePiece



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
        self._display_surf.fill((0, 255, 255))
        self._running = True
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 255, 255))

        # Falling piece initialization methods
        self.groupOfPieces = pygame.sprite.Group()
        self.newPieceGenerationEvent = pygame.USEREVENT + 1
        pygame.time.set_timer(self.newPieceGenerationEvent, 1000)

        # Player initialization methods
        self.player = Player(self.width // 2, 0, 50, 50, (255, 255, 255))

    def on_event(self, event):

        if event.type == pygame.QUIT:
            self._running = False

        # Produces a new falling piece every second
        elif event.type == self.newPieceGenerationEvent:

            color = random.choice([(255, 255, 255), (0, 0, 255)])
            self.groupOfPieces.add(Piece(random.randint(0, self.width - 50), \
                                         -100 - self.scrollY, 50, 50, color))
            pass
        self.player.onKeyPressed(event)
        pass

    def on_loop(self):

        self.clock.tick(60)

        Piece.registryOfGamePieces.update(self)

        self.player.update(self)
        #self.highestPoint = min([piece.rect.y if piece.isTouched else self.height for piece in self.groupOfPieces.sprites()])

        if self.highestPoint <= self.height // 2:

            self.scrollDy = 3

        self.scrollY += self.scrollDy

    def on_render(self):

        self._display_surf.blit(self.background, self.background.get_rect())

        self.groupOfPieces.draw(self._display_surf)
        self._display_surf.blit(self.player.surface, self.player.rect)
        # pygame.draw.line(self._display_surf, (255, 0, 0), (0, self.height // 2), \
        #                  (self.width, self.height // 2), 2)
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