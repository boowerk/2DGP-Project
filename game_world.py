world = [ [] for _ in range(4)]
collision_pairs = {}

def is_collision_pair_registered(group, a, b):
    if group not in collision_pairs:
        return False  # 그룹 자체가 없으면 등록되지 않음
    return a in collision_pairs[group][0] and b in collision_pairs[group][1]

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]  # 초기화

    # 중복 등록 방지
    if a and not is_collision_pair_registered(group, a, b):
        collision_pairs[group][0].append(a)
    if b and not is_collision_pair_registered(group, a, b):
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
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

def find_objects(obj_type):
    result = []
    for layer in world:
        result += [obj for obj in layer if isinstance(obj, obj_type)]
    return result

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
