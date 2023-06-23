import random
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
import os


# loading images like ufo, fuel or beer
def load_sprite(name, with_alpha=True):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    path = parent_directory.__add__("\\assets\\sprites\\").__add__(name)
    loaded_sprite = load(path)
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


# loading sound (laser sound for example)
def load_sound(name):
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    path = parent_directory.__add__("\\assets\\sounds\\").__add__(name)
    return Sound(path)


# generating random position for placing objects

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )


# generating random velocity for objects

def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
