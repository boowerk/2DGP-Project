from pico2d import *

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
    pass

def render_world():
    pass

running = True

open_canvas()

# initialization code
reset_world()

while running:
    #game logic
    handle_events()
    update_canvas()
    render_world()

close_canvas