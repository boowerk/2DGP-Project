import random

from pico2d import load_image, get_time

import game_framework
import game_world
from archer import Archer
from coin import Coin
from game_world import remove_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event, find_tool_event
from worker import Worker

# Citizen Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(citizen, e):
        citizen.dir = 0    # 정지상태
        citizen.frame = 1

        citizen.start_time = get_time()
        pass

    @staticmethod
    def exit(citizen, e):
        pass

    @staticmethod
    def do(citizen):
        if citizen.shop_hammer.tool_count > 0:
            citizen.target_x = citizen.shop_hammer.x
            citizen.state_machine.add_event(('FIND_TOOL', 0))
            citizen.tool = 'Hammer'
        elif citizen.shop_bow.tool_count > 0:
            citizen.target_x = citizen.shop_bow.x
            citizen.state_machine.add_event(('FIND_TOOL', 0))
            citizen.tool = 'Bow'


        if get_time() - citizen.start_time > 3:
            citizen.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            citizen.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(citizen):
        adjusted_x = citizen.king.get_camera_x()
        if citizen.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            citizen.wait_image.clip_draw(citizen.frame * 128, 128, 128, 128, citizen.x - adjusted_x, citizen.y, 100, 100)
        elif citizen.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            citizen.wait_image.clip_composite_draw(citizen.frame * 128, 128, 128, 128, 0, 'h', citizen.x - adjusted_x, citizen.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(citizen, e):
        citizen.frame = 1
        citizen.frame_col = 1
        citizen.once = False

        citizen.last_dir = citizen.dir
        pass

    @staticmethod
    def exit(citizen, e):
        pass

    @staticmethod
    def do(citizen):
        citizen.frame_timer += game_framework.frame_time
        if citizen.frame_timer >= 0.3 and citizen.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            citizen.frame = (citizen.frame + 6) % 36
            citizen.frame_timer = 0.0  # 타이머 리셋

            if citizen.frame == 31:
                citizen.frame_col = 0
                citizen.frame = 1
                citizen.once = True

        elif citizen.frame_timer >= 0.3 and citizen.once == True:
            citizen.frame = (citizen.frame + 6) % 18
            citizen.frame_timer = 0.0  # 타이머 리셋

            if citizen.frame == 13:
                citizen.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(citizen):
        adjusted_x = citizen.king.get_camera_x()
        if citizen.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            citizen.wait_image.clip_draw(citizen.frame * 128, citizen.frame_col * 128, 128, 128, citizen.x - adjusted_x, citizen.y, 100, 100)
        elif citizen.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            citizen.wait_image.clip_composite_draw(citizen.frame * 128, citizen.frame_col * 128, 128, 128, 0, 'h', citizen.x - adjusted_x,
                                                citizen.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(citizen, e):
        citizen.dir = random.choice([-1, 1])
        citizen.frame = 1
        pass

    @staticmethod
    def exit(citizen, e):
        citizen.last_dir = citizen.dir
        pass

    @staticmethod
    def do(citizen):

        if citizen.shop_hammer.tool_count > 0:
            citizen.target_x = citizen.shop_hammer.x
            citizen.state_machine.add_event(('FIND_TOOL', 0))
            citizen.tool = 'Hammer'
        elif citizen.shop_bow.tool_count > 0:
            citizen.target_x = citizen.shop_bow.x
            citizen.state_machine.add_event(('FIND_TOOL', 0))
            citizen.tool = 'Bow'

        citizen.x += citizen.dir * RUN_SPEED_PPS * game_framework.frame_time

        citizen.frame_timer += game_framework.frame_time
        if citizen.frame_timer >= 0.1:
            citizen.frame = (citizen.frame + 6) % 36
            citizen.frame_timer = 0

        if citizen.x < 900:  # 화면 왼쪽 경계
            citizen.x = 900
            citizen.dir = 1
        elif citizen.x > 2100:  # 화면 오른쪽 경계
            citizen.x = 2100
            citizen.dir = -1

        if random.random() < 0.001:
            citizen.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(citizen):
        adjusted_x = citizen.king.get_camera_x()
        if citizen.dir == 1:
            citizen.walk_image.clip_draw(citizen.frame * 128, 0, 128, 128, citizen.x - adjusted_x, citizen.y, 100, 100)
        elif citizen.dir == -1:
            citizen.walk_image.clip_composite_draw(citizen.frame * 128, 0, 128, 128, 0, 'h',citizen.x - adjusted_x, citizen.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(citizen, e):
        citizen.frame = 1
        pass

    @staticmethod
    def exit(citizen, e):
        citizen.last_dir = citizen.dir
        pass

    @staticmethod
    def do(citizen):

        citizen.frame_timer += game_framework.frame_time
        if citizen.frame_timer >= 0.1:
            citizen.frame = (citizen.frame + 6) % 36
            citizen.frame_timer = 0

        target_x = citizen.target_x  # 목표 위치

        # 목표 위치로 이동
        if citizen.x < target_x:
            citizen.x += RUN_SPEED_PPS * game_framework.frame_time
            citizen.dir = 1  # 오른쪽으로 이동
        elif citizen.x > target_x:
            citizen.x -= RUN_SPEED_PPS * game_framework.frame_time
            citizen.dir = -1  # 왼쪽으로 이동

        # 목표 위치에 도달했을 때 정확히 고정
        if abs(citizen.x - target_x) < 1.0:  # 1 픽셀 이하로 가까워지면
            citizen.x = target_x

            if citizen.tool == 'Hammer':
                worker = Worker(citizen.x, citizen.y, citizen.king)
                citizen.shop_hammer.tool_count -= 1
                game_world.remove_object(citizen)
                game_world.add_object(worker)
            elif citizen.tool == 'Bow':
                archer = Archer(citizen.x, citizen.y, citizen.king)
                citizen.shop_bow.tool_count -= 1
                game_world.remove_object(citizen)
                game_world.add_object(archer)


        if random.random() < 0.001:
            citizen.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(citizen):
        adjusted_x = citizen.king.get_camera_x()
        if citizen.dir == 1:
            citizen.run_image.clip_draw(citizen.frame * 128, 0, 128, 128, citizen.x - adjusted_x, citizen.y, 100, 100)
        elif citizen.dir == -1:
            citizen.run_image.clip_composite_draw(citizen.frame * 128, 0, 128, 128, 0, 'h', citizen.x - adjusted_x, citizen.y, 100,
                                                100)
        pass

class Citizen:
    def __init__(self, x, y, king, shop_hammer, shop_bow):
        self.x, self.y = x, y
        self.dir = 0
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.target_x = 0
        self.shop_hammer = shop_hammer
        self.shop_bow = shop_bow
        self.king = king
        self.tool = None
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait, random_event: Walk},
                Wait: {time_out: Idle},
                Walk: {random_event: Wait, find_tool_event: Run},
                Run : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass