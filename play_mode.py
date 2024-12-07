from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDL_KEYUP

import game_framework
import game_world
from archer import Archer
from arrow import Arrow
from background import Background
from citizen import Citizen
from coin import Coin
from coin_pocket import Coin_pocket
from game_world import add_collision_pair, find_objects
from king import King
from kingdom import Kingdom
from map import Map, width
from poor import Poor
from portal import Portal
from shop_bow import Shop_bow
from shop_hammer import Shop_hammer
from troll import Troll
from wall import Wall
from water import Water
from worker import Worker


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
    game_world.add_objects(map, 1)

    background = Background(king)
    game_world.add_object(background, 0)

    kingdom = Kingdom(king)
    game_world.add_object(kingdom, 0)

    shop_hammer = Shop_hammer(king, kingdom)
    game_world.add_object(shop_hammer)

    shop_bow = Shop_bow(king, kingdom)
    game_world.add_object(shop_bow)

    poor = [Poor(king, shop_hammer) for i in range(2)]
    game_world.add_objects(poor, 1)

    archer = Archer(1100, 315, king)
    game_world.add_object(archer)

    portal = Portal(king)
    game_world.add_object(portal)

    wall = Wall(king)
    game_world.add_object(wall, 2)

    water = Water(king)
    game_world.add_object(water, 1)

    coin_pocket = Coin_pocket(king)
    game_world.add_object(coin_pocket, 3)

    # 충돌 대상 등록
    add_collision_pair('king:kingdom', king, kingdom)
    add_collision_pair('king:shop_hammer', king, shop_hammer)
    add_collision_pair('king:bow', king, shop_bow)

    add_collision_pair('king:wall', king, wall)


def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass