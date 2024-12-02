import random

from pico2d import load_image, get_time

import game_framework
import game_world
import shop_hammer
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event, find_wall_event
from wall import Wall

# troll Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 12.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Walk:
    @staticmethod
    def enter(troll, e):
        # troll.dir = random.choice([-1, 1])
        troll.dir = 1
        troll.frame = 0
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):

        # Wall과의 거리 확인
        walls = game_world.find_objects(Wall)  # Wall 객체 리스트 가져오기
        for wall in walls:
            distance = abs(troll.x - wall.x)
            if distance < 50:  # 벽과 100 이하의 거리일 경우 이벤트 발생
                troll.state_machine.add_event(('FIND_WALL', 0))

        troll.x += troll.dir * RUN_SPEED_PPS * game_framework.frame_time

        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 1) % 6
            troll.frame_timer = 0

        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.walk_image.clip_draw(troll.frame * 32, 0, 32, 32, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.walk_image.clip_composite_draw(troll.frame * 32, 0, 32, 32, 0, 'h',troll.x - adjusted_x, troll.y, 100, 100)
        pass

class Attack:
    @staticmethod
    def enter(troll, e):
        troll.frame = 0
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):
        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 1) % 4
            troll.frame_timer = 0

        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.attack_image.clip_draw(troll.frame * 32, 0, 32, 32, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.attack_image.clip_composite_draw(troll.frame * 32, 0, 32, 32, 0, 'h', troll.x - adjusted_x, troll.y, 100,
                                                100)
        pass

class Die:
    @staticmethod
    def enter(troll, e):
        troll.frame = 0
        pass

    @staticmethod
    def exit(troll, e):
        troll.last_dir = troll.dir
        pass

    @staticmethod
    def do(troll):
        troll.frame_timer += game_framework.frame_time
        if troll.frame_timer >= 0.1:
            troll.frame = (troll.frame + 1) % 8
            troll.frame_timer = 0
        pass

    @staticmethod
    def draw(troll):
        adjusted_x = troll.king.get_camera_x()
        if troll.dir == 1:
            troll.die_image.clip_draw(troll.frame * 32, 32, 32, 32, troll.x - adjusted_x, troll.y, 100, 100)
        elif troll.dir == -1:
            troll.die_image.clip_composite_draw(troll.frame * 32, 0, 32, 32, 0, 'h', troll.x - adjusted_x, troll.y,
                                                   100, 100)
        pass

class Troll:
    def __init__(self, x, y, king):
        self.x, self.y = x, y
        self.dir = 1
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.king = king
        self.attack_image = load_image('troll_charge.png')
        self.walk_image = load_image('troll_walk.png')
        self.die_image = load_image('troll_die.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Walk)
        self.state_machine.set_transitions(
            {
                Walk: {find_wall_event: Attack},
                Attack : {},
                Die : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass
