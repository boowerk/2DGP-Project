from pico2d import load_image

import game_framework
from state_machine import StateMachine


class Idle:
    @staticmethod
    def enter(poor, e):
        poor.dir = 0
        poor.frame = 0
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        pass

    @staticmethod
    def draw(poor):
        poor.wait_image.clip_draw(poor.frame * 128, 128, 128, 128, poor.x, poor.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(poor, e):
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        pass

    @staticmethod
    def draw(poor):
        pass

class Walk:
    @staticmethod
    def enter(poor, e):
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        pass

    @staticmethod
    def draw(poor):
        pass

class Poor:
    def __init__(self):
        self.x, self.y = 400, 356
        self.dir = 0
        self.frame = 0
        self.frame_timer = 0
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass