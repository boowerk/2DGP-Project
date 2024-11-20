from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_KEYUP

import game_framework
import game_world
from citizen import Citizen
from coin import Coin
from game_world import add_collision_pair
from king import King
from kingdom import Kingdom
from map import Map, width
from poor import Poor


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                king.handle_event(event)

def init():
    global king

    king = King()
    game_world.add_object(king, 1)

    map = [Map(i * width, king) for i in range(11)]
    game_world.add_objects(map, 0)

    poor = [Poor(king) for i in range(2)]
    game_world.add_objects(poor, 1)

    kingdom = Kingdom(king)
    game_world.add_object(kingdom, 0)

    # 충돌 대상 등록
    add_collision_pair('king:kingdom', king, kingdom)


def finish():
    game_world.clear()

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass