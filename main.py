from pico2d import *

def handle_events():
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