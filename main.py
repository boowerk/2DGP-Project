from pico2d import *

from Map import Map, width

class King:
    def __init__(self):
        self.x, self.y = 400, 100
        self.frame = 8
        self.image = load_image('king.png')
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 64, 0, 64, 64, self.x, self.y)
        pass

    def update(self):
        self.frame = (self.frame + 1) % 8
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
    delay(0.05)

close_canvas