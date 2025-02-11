import sys
import pygame

from core.input import Input


class Base(object):
    """Minuta"""
    def __init__(self, screenSize=(512, 512)):
        pygame.init()
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        self.screen = pygame.display.set_mode(screenSize, displayFlags)
        pygame.display.set_caption("CGr@UAlg")
        self.running = True
        self.clock = pygame.time.Clock()
        self.input = Input()

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        self.initialize()
        while self.running:
            self.input.update()
            if self.input.quit or pygame.key.get_pressed()[pygame.K_ESCAPE]: #ESC
                self.running = False
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
