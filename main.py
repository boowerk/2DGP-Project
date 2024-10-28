from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('tiles.png')

    def draw(self):
        self.image.draw(400, 30)

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