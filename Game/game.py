import pygame
import threading

from pygame import Vector2
from pygame_menu import Theme
import time
from utils import load_sprite, get_random_position
from models import Spaceship, Asteroid, Beer
import pygame_menu

BEER_RESPING_TIME = 5


def _init_pygame():
    # pygame init is responsible for loading all necessary modules
    pygame.init()
    # window name
    pygame.display.set_caption("Spaceship game")


def _menu():
    _init_pygame()
    surface = pygame.display.set_mode((1000, 667))
    space_ship_game = SpaceShipGame(surface)
    welcome_text = "Dear student! The greatest threat appeared, there are no more beer \n and the party is about to colapse.\n" \
                   " You need to set out on a mission to rescue your fellow colleagues \n - collect 10 beers and come back on earth\n" \
                   "as soon as you can!"
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    font = pygame_menu.font.FONT_MUNRO
    mytheme.widget_font = font
    mytheme.title_font = font
    mytheme.title_font_size = 50
    menu = pygame_menu.Menu('PIWO MOJE PALIWO', 1000, 667, theme=mytheme)
    menu.add.label(welcome_text)
    menu.add.button('Play', space_ship_game.main_loop, font_size=40, padding=20)
    menu.add.button('Quit', quit, font_size=40, padding=20)
    menu.mainloop(surface)


class SpaceShipGame:
    MIN_DISTANCE = 250

    def __init__(self, surface):
        self.screen = surface
        self.background = load_sprite("space.jpg", False)
        self.clock = pygame.time.Clock()
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        # self.asteroids = [Asteroid(get_random_position(self.screen)) for _ in range(6)]
        self.asteroids = []
        self.beer = []
        self.time = time.time()

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_DISTANCE:
                    break
            self.asteroids.append(Asteroid(position))

    def main_loop(self):
        while True:
            if self.spaceship:
                self.handle_input()
                self._process_game_logic()
                self._draw()
            else:
                self._loss_message()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
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

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    # fajnie by bylo dodac jakis wybuch po zderzeniu
                    self.spaceship = None
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    break
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        current_time = time.time()
        if current_time - self.time > BEER_RESPING_TIME:
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_DISTANCE:
                    break
                self.time = time.time()
            self.beer.append(Beer(position))
        if self.spaceship:
            self.spaceship.use_fuel()
            for beer in self.beer[:]:
                if self.spaceship.collides_with(beer):
                    self.spaceship.add_fuel()
                    self.beer.remove(beer)

        # for bullet in self.bullets[:]:
        #     if not self.screen.get_rect().collidepoint(bullet.position):
        #         self.bullets.remove(bullet)

    def _draw(self):
        # draw one image onto another
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        for beer in self.beer:
            beer.draw(self.screen)
        # updating display
        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def _loss_message(self):
        for asteroid in self.asteroids:
            asteroid.velocity = Vector2(0)
        # self.screen.blit("You lost")
        myfont = pygame.font.SysFont("munro", 30)

        # render text
        label = myfont.render("You lost!", 1, (255, 255, 0))
        self.screen.blit(label, (500, 333))
        pygame.display.update()
        time.sleep(5)
        quit()
