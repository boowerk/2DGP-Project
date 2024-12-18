import random

from pico2d import load_image, get_time

import game_framework
import game_world
from arrow import Arrow
from boss import Boss
from coin import Coin
from game_world import remove_object, add_object
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event, find_tool_event, \
    find_enemy_event, attack_event
from troll import Troll
from wall import Wall

# archer Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Idle:
    @staticmethod
    def enter(archer, e):
        archer.dir = 0    # 정지상태
        archer.frame = 4

        archer.start_time = get_time()
        pass

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        if get_time() - archer.start_time > 3:
            archer.state_machine.add_event(('TIME_OUT', 0))

        if random.random() < 0.01:
            archer.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            archer.wait_image.clip_draw(archer.frame * 128, 128, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            archer.wait_image.clip_composite_draw(archer.frame * 128, 128, 128, 128, 0, 'h', archer.x - adjusted_x, archer.y, 100, 100)
        pass

class Wait:
    @staticmethod
    def enter(archer, e):
        archer.frame = 4
        archer.frame_col = 1
        archer.once = False

        archer.last_dir = archer.dir
        pass

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):

        trolls = game_world.find_objects(Troll)  # Troll 객체 리스트 가져오기
        for troll in trolls:
            distance = abs(archer.x - troll.x)
            if distance <= 600:  # Archer와 Troll의 거리가 200 이하일 때
                archer.state_machine.add_event(('FIND_ENEMY', 0))

        bosses = game_world.find_objects(Boss)  # Troll 객체 리스트 가져오기
        for boss in bosses:
            distance = abs(archer.x - boss.x)
            if distance <= 600:  # Archer와 Troll의 거리가 200 이하일 때
                archer.state_machine.add_event(('FIND_ENEMY', 0))

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.3 and archer.once == False:  # 프레임 간격을 0.1초로 설정 (필요에 따라 조정 가능)
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0.0  # 타이머 리셋

            if archer.frame == 34:
                archer.frame_col = 0
                archer.frame = 4
                archer.once = True

        elif archer.frame_timer >= 0.3 and archer.once == True:
            archer.frame = (archer.frame + 6) % 18
            archer.frame_timer = 0.0  # 타이머 리셋

            if archer.frame == 16:
                archer.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.last_dir == 1:  # 마지막 방향이 오른쪽일 때
            archer.wait_image.clip_draw(archer.frame * 128, archer.frame_col * 128, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.last_dir == -1:  # 마지막 방향이 왼쪽일 때
            archer.wait_image.clip_composite_draw(archer.frame * 128, archer.frame_col * 128, 128, 128, 0, 'h', archer.x - adjusted_x,
                                                archer.y, 100, 100)
        pass

class Walk:
    @staticmethod
    def enter(archer, e):
        archer.dir = random.choice([-1, 1])
        archer.frame = 4
        pass

    @staticmethod
    def exit(archer, e):
        archer.last_dir = archer.dir
        pass

    @staticmethod
    def do(archer):

        walls = game_world.find_objects(Wall)  # Wall 객체 리스트 가져오기
        for wall in walls:
            if wall.is_attacked():  # Wall이 공격받은 상태인지 확인
                archer.state_machine.add_event(('FIND_ENEMY', 0))

        archer.x += archer.dir * RUN_SPEED_PPS * game_framework.frame_time

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.1:
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0

        trolls = game_world.find_objects(Troll)  # Troll 객체 리스트 가져오기
        for troll in trolls:
            distance = abs(archer.x - troll.x)
            if distance <= 600:  # Archer와 Troll의 거리가 200 이하일 때
                archer.state_machine.add_event(('FIND_ENEMY', 0))

        bosses = game_world.find_objects(Boss)  # Troll 객체 리스트 가져오기
        for boss in bosses:
            distance = abs(archer.x - boss.x)
            if distance <= 600:  # Archer와 Troll의 거리가 200 이하일 때
                archer.state_machine.add_event(('FIND_ENEMY', 0))

        if archer.x < 600:  # 화면 왼쪽 경계
            archer.x = 600
            archer.dir = 1
        elif archer.x > 2100:  # 화면 오른쪽 경계
            archer.x = 2100
            archer.dir = -1

        if random.random() < 0.001:
            archer.state_machine.add_event(('RANDOM', 0))
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.dir == 1:
            archer.walk_image.clip_draw(archer.frame * 128, 0, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.dir == -1:
            archer.walk_image.clip_composite_draw(archer.frame * 128, 0, 128, 128, 0, 'h',archer.x - adjusted_x, archer.y, 100, 100)
        pass

class Run:
    @staticmethod
    def enter(archer, e):
        archer.frame = 4
        pass

    @staticmethod
    def exit(archer, e):
        archer.last_dir = archer.dir
        pass

    @staticmethod
    def do(archer):

        trolls = game_world.find_objects(Troll)  # Troll 객체 리스트 가져오기
        for troll in trolls:
            distance = abs(archer.x - troll.x)

            # Troll 방향으로 이동
            direction = 1 if troll.x > archer.x else -1
            archer.dir = direction

            if distance <= 200:  # Archer와 Troll의 거리가 100 이하일 때
                archer.state_machine.add_event(('ATTACK', 0))

        bosses = game_world.find_objects(Boss)
        for boss in bosses:
            distance = abs(archer.x - boss.x)

            direction = 1 if boss.x > archer.x else -1
            archer.dir = direction

            if distance <= 200:
                archer.state_machine.add_event(('ATTACK', 0))

        walls = game_world.find_objects(Wall)  # Wall 객체 리스트 가져오기
        for wall in walls:
            if wall.is_attacked():  # Wall이 공격받은 상태인지 확인
                direction = 1 if wall.x > archer.x else -1
                archer.dir = direction  # 벽 방향으로 이동
                distance = abs(archer.x - wall.x)

        archer.x += archer.dir * RUN_SPEED_PPS * game_framework.frame_time

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.1:
            archer.frame = (archer.frame + 6) % 36
            archer.frame_timer = 0
        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.dir == 1:
            archer.run_image.clip_draw(archer.frame * 128, 0, 128, 128, archer.x - adjusted_x, archer.y, 100, 100)
        elif archer.dir == -1:
            archer.run_image.clip_composite_draw(archer.frame * 128, 0, 128, 128, 0, 'h', archer.x - adjusted_x, archer.y, 100,
                                                100)
        pass

class Shoot:
    @staticmethod
    def enter(archer, e):
        archer.frame = 0
        pass

    @staticmethod
    def exit(archer, e):
        archer.last_dir = archer.dir
        pass

    @staticmethod
    def do(archer):

        archer.shoot_arrow()

        # troll과 arrow 충돌 그룹 추가
        trolls = game_world.find_objects(Troll)
        bosses = game_world.find_objects(Boss)
        arrows = game_world.find_objects(Arrow)
        for troll in trolls:
            for arrow in arrows:
                game_world.add_collision_pair('troll:arrow', troll, arrow)

        for boss in bosses:
            for arrow in arrows:
                game_world.add_collision_pair('boss:arrow', boss, arrow)

        archer.frame_timer += game_framework.frame_time
        if archer.frame_timer >= 0.1:
            archer.frame = (archer.frame + 1) % 7
            archer.frame_timer = 0

            if archer.frame == 6:
                archer.state_machine.add_event(("TIME_OUT", 0))

        pass

    @staticmethod
    def draw(archer):
        adjusted_x = archer.king.get_camera_x()
        if archer.dir == 1:
            archer.shoot_image.clip_draw(archer.frame * 300, 0, 300, 100, archer.x - adjusted_x, archer.y - 10, 240, 80)
        elif archer.dir == -1:
            archer.shoot_image.clip_composite_draw(archer.frame * 300, 0, 300, 100, 0, 'h', archer.x - adjusted_x, archer.y - 10, 240, 80)
        pass

class Archer:
    def __init__(self, x, y, king):
        self.x, self.y = x, y
        self.dir = 1
        self.last_dir = 1
        self.frame = 0
        self.frame_timer = 0
        self.last_arrow_time = 0.0
        self.arrow_interval = 1.0
        self.king = king
        self.run_image = load_image('npc_run_sprite.png')
        self.wait_image = load_image('npc_wait_sprite.png')
        self.walk_image = load_image('npc_walk_sprite.png')
        self.shoot_image = load_image('archer_shoot.png')
        self.arrow = load_image('arrow.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Wait, random_event: Walk},
                Wait: {time_out: Idle, find_enemy_event: Run},
                Walk: {random_event: Wait, find_enemy_event: Run},
                Run : {attack_event: Shoot},
                Shoot: {time_out: Idle}
            }
        )

    def shoot_arrow(self):
        current_time = get_time()
        if current_time - self.last_arrow_time >= self.arrow_interval:
            arrow = Arrow(self.x, self.y - 20, self.dir, self.king)
            game_world.add_object(arrow)  # 화살 추가
            self.last_arrow_time = current_time  # 마지막 생성 시간 업데이트

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass