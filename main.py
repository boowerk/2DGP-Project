from pico2d import *

width, height = 254, 64

class Map:
    def __init__(self):
        self.grass_tile = load_image('tiles.png')

    def draw(self):
        self.grass_tile.clip_draw(232, 0, 127, 32, 0, 150, width, height)

    def upadate(self):
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

    running = True
    world = []

    map = Map()
    world.append(map)

    pass

def update_world():
    for o in world:
        o.upadate()
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