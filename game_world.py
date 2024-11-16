world = [ [] for _ in range(4)]
collision_pairs = {}

def add_collision_pair():
    pass

def remove_collision_object(o):
    pass

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    pass

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    pass

def handle_collision():
    pass