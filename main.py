from pico2d import *

from Map import Map, width

class King:
    def __init__(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass


def handle_events():
    global running
    events = get_events()
    
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    pass

def reset_world():
    global running
    global world
    global map
    global king

    running = True
    world = []

    map = [Map(i * width) for i in range(11)]
    world += map

    king = King()
    world.append(king)

    pass

def update_world():
    for o in world:
        o.update()
    pass

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()

# initialization code
reset_world()

while running:
    #game logic
    handle_events()
    update_world()
    render_world()

close_canvas