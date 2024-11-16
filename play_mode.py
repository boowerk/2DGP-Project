from pico2d import *
import game_framework
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_KEYUP

from king import King
from map import Map, width


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                king.handle_event(event)

    pass

def init():
    global king

    world = []

    king = King()
    world.append(king)

    map = [Map(i * width, king) for i in range(11)]
    world += map

    pass