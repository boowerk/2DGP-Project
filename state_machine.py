from tabnanny import check

from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_q, SDLK_F1


def start_evnet(e):
    return e[0] == 'START'

def find_tool_event(e):
    return e[0] == 'FIND_TOOL'

def find_coin_event(e):
    return e[0] == 'FIND_COIN'

def find_wall_event(e):
    return e[0] == 'FIND_WALL'

def find_enemy_event(e):
    return e[0] == 'FIND_ENEMY'

def attack_event(e):
    return e[0] == 'ATTACK'

def die_event(e):
    return e[0] == 'DIE'

def miss_event(e):
    return e[0] == 'MISS'

def random_event(e):
    return e[0] == 'RANDOM'

def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_F1


class StateMachine:

    def __init__(self, obj):
        self.obj = obj
        self.event_q = []

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.obj, ('START', 0))
        # print(f'Enter into {state}')
        pass

    def update(self):
        self.cur_state.do(self.obj)

        if self.event_q:
            e = self.event_q.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    # print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)

                    self.cur_state = next_state
                    # print(f'Enter into {next_state}')

                    self.cur_state.enter(self.obj, e)
                    return
            # print(f'        WARING: {e} not handled at state {self.cur_state}')


    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        # print(f'    DEBUG: add event {e}')
        self.event_q.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions