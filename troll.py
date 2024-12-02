import random

from pico2d import load_image, get_time

import game_framework
import game_world
import shop_hammer
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event

# troll Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 12.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(troll, e):
        troll.dir = 0    # 정지상태
        troll.frame = 0

        troll.start_time = get_time()
        pass

    @staticmethod
    def exit(troll, e):
        pass

    @staticmethod
    def do(troll):
        if get_time() - troll.start_time > 3:
            troll.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            troll.wait_image.clip_draw(troll.frame * 128, 128, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            troll.wait_image.clip_composite_draw(troll.frame * 128, 128, 128, 128, 0, 'h', troll.x - adjusted_x, troll.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(troll, e):
        troll.dir = random.choice([-1, 1])
        troll.frame = 3
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):

        troll.x += troll.dir * RUN_SPEED_PPS * game_framework.frame_time

        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 6) % 36
            troll.frame_timer = 0

        if troll.x < 900:  # 화면 왼쪽 경계
            troll.x = 900
            troll.dir = 1
        elif troll.x > 2100:  # 화면 오른쪽 경계
            troll.x = 2100
            troll.dir = -1

        if random.random() < 0.001:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.walk_image.clip_draw(troll.frame * 128, 0, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.walk_image.clip_composite_draw(troll.frame * 128, 0, 128, 128, 0, 'h',troll.x - adjusted_x, troll.y, 100, 100)
        pass

class attack:
    @staticmethod
    def enter(troll, e):
        troll.frame = 3
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):
        troll.x += troll.dir * RUN_SPEED_PPS * game_framework.frame_time

        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 6) % 36
            troll.frame_timer = 0

        if troll.x < 900:  # 화면 왼쪽 경계
            troll.x = 900
            troll.dir = 1
        elif troll.x > 2100:  # 화면 오른쪽 경계
            troll.x = 2100
            troll.dir = -1

        if random.random() < 0.001:
            troll.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.attack_image.clip_draw(troll.frame * 128, 0, 128, 128, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.attack_image.clip_composite_draw(troll.frame * 128, 0, 128, 128, 0, 'h', troll.x - adjusted_x, troll.y, 100,
                                                100)
        pass

class die:
    @staticmethod
    def enter(troll, e):
        pass

    @staticmethod
    def exit(troll, e):
        pass

    @staticmethod
    def do(troll):
        pass

    @staticmethod
    def draw(troll):
        pass

class Troll:
    def __init__(self, x, y, king):
        self.x, self.y = x, y
        self.dir = 0
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.king = king
        self.attack_image = load_image('troll_charge.png')
        self.walk_image = load_image('troll_walk.png')
        self.die_image = load_image('troll_die.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {random_event: Walk},
                Walk: {find_coin_event: attack},
                attack : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass
