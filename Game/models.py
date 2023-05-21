from pygame.math import Vector2
from utils import load_sprite, wrap_position
from pygame.transform import rotozoom

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        # Calculating blit position
        # It is needed because blit() method requires a top-left corner position
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.2
    BRAKE = 0.1
    RESISTANCE = 0.05

    def __init__(self, position):
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("ufo1_small.png"), Vector2(0))

    def accelerate(self):
        if 10 > self.velocity.x > -10 and 10 > self.velocity.y > -10:
            self.velocity += self.direction * self.ACCELERATION
        else:
            self.velocity = self.direction

    def brake(self):
        self.velocity -= self.velocity * self.BRAKE

    def stop(self):
        self.velocity = Vector2(0)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def slow(self):
        if not 0.5 > self.velocity.y > -0.5 or not 0.5 > self.velocity.x > -0.5:
            self.velocity -= self.velocity * self.RESISTANCE
        else:
            self.velocity = Vector2(0)


class Asteroid(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("meteor1_smaller.png"), (0, 0))
