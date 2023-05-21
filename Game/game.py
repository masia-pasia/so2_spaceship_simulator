import pygame
from utils import load_sprite, get_random_position
from models import Spaceship, Asteroid


def _init_pygame():
    pygame.init()
    pygame.display.set_caption("Spaceship game")


class SpaceShipGame:
    def __init__(self):
        _init_pygame()
        self.screen = pygame.display.set_mode((1000, 667))
        self.background = load_sprite("space.jpg", False)
        self.clock = pygame.time.Clock()
        self.spaceship = Spaceship((400, 300))
        self.asteroids = [Asteroid(get_random_position(self.screen)) for _ in range(6)]

    def main_loop(self):
        while True:
            self.handle_input()
            self._process_game_logic()
            self._draw()
            print(self.spaceship.velocity)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        is_key_pressed = pygame.key.get_pressed()

        if is_key_pressed[pygame.K_RIGHT]:
            self.spaceship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.spaceship.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.spaceship.accelerate()
        elif is_key_pressed[pygame.K_DOWN]:
            self.spaceship.brake()
        else:
            self.spaceship.slow()
        if is_key_pressed[pygame.K_LCTRL]:
            self.spaceship.stop()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        return [*self.asteroids, self.spaceship]
