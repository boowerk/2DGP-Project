import random

from pico2d import load_image, get_time

import game_framework
import game_world
import shop_hammer
from citizen import Citizen
from coin import Coin
from game_world import remove_object
from shop_hammer import Shop_hammer
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event

# Poor Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(poor, e):
        poor.dir = 0    # 정지상태
        poor.frame = 0

        poor.start_time = get_time()
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        if get_time() - poor.start_time > 3:
            poor.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            poor.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(poor):
        adjusted_x = poor.king.get_camera_x()
        if poor.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            poor.wait_image.clip_draw(poor.frame * 128, 128, 128, 128, poor.x - adjusted_x, poor.y, 100, 100)
        elif poor.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            poor.wait_image.clip_composite_draw(poor.frame * 128, 128, 128, 128, 0, 'h', poor.x - adjusted_x, poor.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(poor, e):
        poor.frame = 0
        poor.frame_col = 1
        poor.once = False

        poor.last_dir = poor.dir
        pass

    @staticmethod
    def exit(poor, e):
        pass

    @staticmethod
    def do(poor):
        poor.frame_timer += game_framework.frame_time
        if poor.frame_timer >= 0.3 and poor.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            poor.frame = (poor.frame + 6) % 36
            poor.frame_timer = 0.0  # 타이머 리셋

            if poor.frame == 30:
                poor.frame_col = 0
                poor.frame = 0
                poor.once = True

        elif poor.frame_timer >= 0.3 and poor.once == True:
            poor.frame = (poor.frame + 6) % 18
            poor.frame_timer = 0.0  # 타이머 리셋

            if poor.frame == 12:
                poor.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(poor):
        adjusted_x = poor.king.get_camera_x()
        if poor.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            poor.wait_image.clip_draw(poor.frame * 128, poor.frame_col * 128, 128, 128, poor.x - adjusted_x, poor.y, 100, 100)
        elif poor.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            poor.wait_image.clip_composite_draw(poor.frame * 128, poor.frame_col * 128, 128, 128, 0, 'h', poor.x - adjusted_x,
                                                poor.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(poor, e):
        poor.dir = random.choice([-1, 1])
        poor.frame = 0
        pass

    @staticmethod
    def exit(poor, e):
        poor.last_dir = poor.dir
        pass

    @staticmethod
    def do(poor):
        # 근처 동전 찾기
        coins = [coin for coin in game_world.find_objects(Coin) if coin.y < 400]
        if coins:
            poor.state_machine.add_event(('FIND_COIN', 0))

        poor.x += poor.dir * RUN_SPEED_PPS * game_framework.frame_time

        poor.frame_timer += game_framework.frame_time
        if poor.frame_timer >= 0.1:
            poor.frame = (poor.frame + 6) % 36
            poor.frame_timer = 0

        if poor.x < 900:  # 화면 왼쪽 경계
            poor.x = 900
            poor.dir = 1
        elif poor.x > 2100:  # 화면 오른쪽 경계
            poor.x = 2100
            poor.dir = -1

        if random.random() < 0.001:
            poor.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(poor):
        adjusted_x = poor.king.get_camera_x()
        if poor.dir == 1:
            poor.walk_image.clip_draw(poor.frame * 128, 0, 128, 128, poor.x - adjusted_x, poor.y, 100, 100)
        elif poor.dir == -1:
            poor.walk_image.clip_composite_draw(poor.frame * 128, 0, 128, 128, 0, 'h',poor.x - adjusted_x, poor.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(poor, e):
        poor.frame = 0
        pass

    @staticmethod
    def exit(poor, e):
        poor.last_dir = poor.dir
        pass

    @staticmethod
    def do(poor):
        # 근처 동전 찾기
        coins = [coin for coin in game_world.find_objects(Coin) if coin.y < 400]
        if coins:
            nearest_coin = min(coins, key=lambda c: abs(c.x - poor.x))
            poor.dir = 1 if nearest_coin.x > poor.x else -1

            if abs(nearest_coin.x - poor.x) < 5:  # 동전에 가까워지면 멈춤
                remove_object(nearest_coin)
                remove_object(poor)
                citizen = Citizen(poor.x, poor.y, poor.king, poor.shop_hammer, poor.shop_bow)
                game_world.add_object(citizen, 0)
                return
        else:
            poor.state_machine.add_event(('MISS', 0))

        poor.x += poor.dir * RUN_SPEED_PPS * game_framework.frame_time

        poor.frame_timer += game_framework.frame_time
        if poor.frame_timer >= 0.1:
            poor.frame = (poor.frame + 6) % 36
            poor.frame_timer = 0

        if poor.x < 900:  # 화면 왼쪽 경계
            poor.x = 900
            poor.dir = 1
        elif poor.x > 2100:  # 화면 오른쪽 경계
            poor.x = 2100
            poor.dir = -1

        if random.random() < 0.001:
            poor.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(poor):
        adjusted_x = poor.king.get_camera_x()
        if poor.dir == 1:
            poor.run_image.clip_draw(poor.frame * 128, 0, 128, 128, poor.x - adjusted_x, poor.y, 100, 100)
        elif poor.dir == -1:
            poor.run_image.clip_composite_draw(poor.frame * 128, 0, 128, 128, 0, 'h', poor.x - adjusted_x, poor.y, 100,
                                                100)
        pass

class Poor:
    def __init__(self, king, shop_hammer, shop_bow):
        self.x, self.y = 1600, 315
        self.dir = 0
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.king = king
        self.gen_timer = 0
        self.shop_hammer = shop_hammer
        self.shop_bow = shop_bow
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait, random_event: Walk},
                Wait: {time_out: Idle},
                Walk: {random_event: Wait, find_coin_event: Run},
                Run : {miss_event: Idle}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.gen_timer += game_framework.frame_time
        if self.gen_timer >= 30.0:
            poor = [Poor(self.king, self.shop_hammer, self.shop_bow) for i in range(2)]
            game_world.add_objects(poor, 1)
            self.gen_timer = 0
        self.state_machine.update()
        pass