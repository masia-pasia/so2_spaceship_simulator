import time

from pygame.math import Vector2
from utils import load_sprite, get_random_velocity, load_sound
from pygame.transform import rotozoom
import threading

# const vectors for some calculations
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)


class GameObject:
    def __init__(self, position, sprite):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2

    def draw(self, surface):
        # Calculating blit position
        # It is needed because blit() method requires a top-left corner position
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    # checking if object has collided with something
    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.3
    BRAKE = 0.25
    RESISTANCE = 0.05
    MAX_SPEED = 10
    BULLET_SPEED = 6
    FUEL_CAPACITY = 10

    def __init__(self, position, create_bullet_callback):
        self.direction = Vector2(UP)
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser.mp3")
        self.velocity = Vector2(0)
        self.fuel = self.FUEL_CAPACITY
        self.key_lock = threading.Lock()
        super().__init__(position, load_sprite("ufo1_small.png"))

    def move(self, surface):
        if self.fuel != 0:
            w, h = surface.get_size()
            # checking if spaceship will be still in the screen after the move
            if 0 < self.position.x + self.velocity.x < w and 0 < self.position.y + self.velocity.y < h:
                self.position = self.position + self.velocity
            else:
                self.velocity = Vector2(0)

    def accelerate(self):
        # avoid speeding to not get the fine
        if 10 > (self.velocity + self.direction * self.ACCELERATION).length():
            self.velocity += self.direction * self.ACCELERATION

    def brake(self):
        if 10 > (self.velocity - self.direction * self.ACCELERATION).length():
            self.velocity -= self.direction * self.BRAKE

    # stop in place
    def stop(self):
        self.velocity = Vector2(0)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    # method that draws images on objects
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        # it is needed because object is always inside the square and if we rotate our object the square will get bigger
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def slow(self):
        if self.MAX_SPEED >= self.velocity.length() > 0.01:
            self.velocity -= self.velocity * self.RESISTANCE
        else:
            self.velocity = Vector2(0)

    # shoot laser
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    # method for using fuel with a critical section
    def use_fuel(self, spaceship):
        while spaceship:
            spaceship.key_lock.acquire()
            if self.fuel - 0.02 * self.FUEL_CAPACITY > 0:
                self.fuel -= 0.02 * self.FUEL_CAPACITY
            else:
                self.fuel = 0
            spaceship.key_lock.release()
            time.sleep(1)

    # method for adding fuel with critical section
    def add_fuel(self, spaceship, condition, key_lock):
        while spaceship:
            with condition:
                # wait for notification about colliding with fuel
                condition.wait()
                spaceship.key_lock.acquire()
                if self.fuel + 0.2 * self.FUEL_CAPACITY > self.FUEL_CAPACITY:
                    self.fuel = self.FUEL_CAPACITY
                else:
                    self.fuel += 0.2 * self.FUEL_CAPACITY
                spaceship.key_lock.release()


class Asteroid(GameObject):
    def __init__(self, position):
        self.velocity = get_random_velocity(1, 3)
        super().__init__(position, load_sprite("asteroid_smaller.png"))

    # method responsible for moving asteroids. If the asteroid hit the edge of the screen it will bounce back
    def move(self, surface):
        w, h = surface.get_size()
        if self.position.x > w or self.position.x < 0:
            self.velocity.x = -self.velocity.x
        if self.position.y > h or self.position.y < 0:
            self.velocity.y = -self.velocity.y
        self.position += self.velocity


class Bullet(GameObject):
    def __init__(self, position, velocity):
        self.velocity = velocity
        super().__init__(position, load_sprite("bullet_smaller.png"))

    def draw(self, surface):
        angle = self.velocity.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        # it is needed because object is always inside the square and if we rotate our object the square will get bigger
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move(self, surface):
        self.position += self.velocity


class Fuel(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("gas.png"))


class Beer(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("piwo_ale_takie_male.png"))
