import pygame
from utils import load_sprite


def _init_pygame():
    pygame.init()
    pygame.display.set_caption("Spaceship game")


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


class SpaceShipGame:
    def __init__(self):
        _init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space.jpg", False)

    def main_loop(self):
        while True:
            handle_input()
            self._process_game_logic()
            self._draw()

    def _process_game_logic(self):
        pass

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
