import random

from pico2d import load_image, get_time, draw_rectangle, load_wav

import game_framework
import game_world
import shop_hammer
from coin import Coin
from game_world import remove_object
from king import King
from state_machine import StateMachine, time_out, random_event, find_coin_event, miss_event, find_wall_event, die_event
from wall import Wall

# troll Run Speed
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 8.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Walk:
    @staticmethod
    def enter(boss, e):
        # boss.dir = random.choice([-1, 1])
        boss.dir = 1
        boss.frame = 0
        pass

    @staticmethod
    def exit(boss, e):
        boss.last_dir = boss.dir
        pass

    @staticmethod
    def do(boss):
        kings = game_world.find_objects(King)
        bosses = game_world.find_objects(Boss)
        for king in kings:
            for boss in bosses:
                game_world.add_collision_pair('King:boss', king, boss)

        # Wall과의 거리 확인
        walls = game_world.find_objects(Wall)  # Wall 객체 리스트 가져오기
        for wall in walls:
            distance = abs(boss.x - wall.x)
            if distance < 100 and wall.hp > 0:  # 벽과 100 이하의 거리일 경우 이벤트 발생
                boss.state_machine.add_event(('FIND_WALL', 0))

        boss.x += boss.dir * RUN_SPEED_PPS * game_framework.frame_time

        boss.frame_timer += game_framework.frame_time
        if boss.frame_timer >= 0.1:
            boss.frame = (boss.frame + 1) % 6
            boss.frame_timer = 0

        if boss.hp <= 0:
            boss.state_machine.add_event(('DIE', 0))

        pass

    @staticmethod
    def draw(boss):
        adjusted_x = boss.king.get_camera_x()
        if boss.dir == 1:
            boss.walk_image.clip_draw(boss.frame * 96, 0, 96, 96, boss.x - adjusted_x, boss.y, 192, 192)
        elif boss.dir == -1:
            boss.walk_image.clip_composite_draw(boss.frame * 96, 0, 96, 96, 0, 'h',boss.x - adjusted_x, boss.y, 192, 192)
        pass

class Attack:
    @staticmethod
    def enter(boss, e):
        boss.frame = 0
        pass

    @staticmethod
    def exit(boss, e):
        boss.last_dir = boss.dir
        pass

    @staticmethod
    def do(boss):
        kings = game_world.find_objects(King)
        bosses = game_world.find_objects(Boss)
        for king in kings:
            for boss in bosses:
                game_world.add_collision_pair('King:boss', king, boss)

        boss.frame_timer += game_framework.frame_time
        boss.attack_timer += game_framework.frame_time  # 공격 타이머 갱신
        boss.hand_timer += game_framework.frame_time


        # 일정 시간마다 공격 실행 (예: 1초)
        if boss.attack_timer >= 5.0:
            walls = game_world.find_objects(Wall)  # Wall 객체 리스트 가져오기
            for wall in walls:
                if abs(boss.x - wall.x) < 150:  # 가까운 Wall에만 공격
                    wall.take_damage(1)  # HP 1씩 감소
                    print(f"Wall HP: {wall.hp}")
                    if wall.hp <= 0:
                        boss.state_machine.add_event(('MISS', 0))
                    break
            boss.attack_timer = 0  # 공격 타이머 초기화

        if boss.frame_timer >= 0.1:
            boss.frame = (boss.frame + 1) % 7
            boss.frame_timer = 0

        if boss.hp <= 0:
            boss.state_machine.add_event(('DIE', 0))

        pass

    @staticmethod
    def draw(boss):
        adjusted_x = boss.king.get_camera_x()
        if boss.use_left_hand:
            # 왼손 공격 이미지 출력
            if boss.dir == 1:
                boss.attack_left_image.clip_draw(boss.frame * 96, 0, 96, 96, boss.x - adjusted_x, boss.y, 192, 192)
            elif boss.dir == -1:
                boss.attack_left_image.clip_composite_draw(boss.frame * 96, 0, 96, 96, 0, 'h', boss.x - adjusted_x,
                                                           boss.y, 192, 192)
        else:
            # 오른손 공격 이미지 출력
            if boss.dir == 1:
                boss.attack_right_image.clip_draw(boss.frame * 96, 0, 96, 96, boss.x - adjusted_x, boss.y, 192, 192)
            elif boss.dir == -1:
                boss.attack_right_image.clip_composite_draw(boss.frame * 96, 0, 96, 96, 0, 'h', boss.x - adjusted_x,
                                                            boss.y, 192, 192)

class Die:
    @staticmethod
    def enter(boss, e):
        boss.frame = 0
        pass

    @staticmethod
    def exit(boss, e):
        boss.last_dir = boss.dir
        pass

    @staticmethod
    def do(boss):
        boss.frame_timer += game_framework.frame_time
        if boss.frame_timer >= 0.1:
            boss.frame = (boss.frame + 1) % 8
            boss.frame_timer = 0
            if boss.frame == 7:
                boss.col -= 1
                boss.frame = 0
                if boss.col == 0:
                    boss.drop_coin()
                    game_world.remove_collision_object(boss)
                    game_world.remove_object(boss)  # 객체 삭제
        pass

    @staticmethod
    def draw(boss):
        adjusted_x = boss.king.get_camera_x()
        if boss.dir == 1:
            boss.die_image.clip_draw(boss.frame * 96, boss.col * 96, 96, 96, boss.x - adjusted_x, boss.y, 192, 192)
        elif boss.dir == -1:
            boss.die_image.clip_composite_draw(boss.frame * 96, boss.col * 96, 96, 96, 0, 'h', boss.x - adjusted_x, boss.y,
                                                   192, 192)
        pass

class Boss:
    hit_sound = None
    kill_sound = None

    def __init__(self, x, king):
        if not Boss.hit_sound:
            Boss.hit_sound = load_wav('arrow_hit_bunny.wav')
            Boss.hit_sound.set_volume(32)

        if not Boss.kill_sound:
            Boss.kill_sound = load_wav('arrow_kill_troll.wav')
            Boss.kill_sound.set_volume(32)

        self.x, self.y = x, 355
        self.dir = 1
        self.last_dir = 1
        self.frame = 0
        self.col = 3
        self.frame_timer = 0
        self.attack_timer = 0
        self.hand_timer = 0
        self.king = king
        self.use_left_hand = True  # True면 왼손, False면 오른손
        self.damaged = False
        self.damaged_timer = 0
        self.hp = 5
        self.attack_left_image = load_image('boss_bash_left.png')
        self.attack_right_image = load_image('boss_bash_right.png')
        self.walk_image = load_image('boss_walk.png')
        self.die_image = load_image('boss_death.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Walk)
        self.state_machine.set_transitions(
            {
                Walk: {find_wall_event: Attack, die_event: Die},
                Attack : {miss_event: Walk, die_event: Die},
                Die : {}
            }
        )

    def draw(self):
        self.state_machine.draw()
        pass

    def drop_coin(self):
        coin = Coin(self.x, self.y - 80, self.king)
        game_world.add_object(coin, 1)

    def update(self):
        self.state_machine.update()

        if self.damaged and self.hp > 0:
            self.damaged_timer += game_framework.frame_time
            if self.damaged_timer > 0.5:  # 0.5초 후에 다시 충돌 가능
                self.damaged = False
                self.damaged_timer = 0

        # 공격 간격마다 손 교체
        if self.hand_timer >= 1.0:  # 1초마다 손을 바꿔 공격
            self.use_left_hand = not self.use_left_hand  # 손 교체
            self.hand_timer = 0  # 타이머 리셋

        if self.hp <= 0:
            self.state_machine.add_event(('DIE', 0))

        pass

    def get_bb(self):
        # 충돌 박스 좌표 반환
        return self.x - self.king.camera_x - 40, self.y - 80, self.x - self.king.camera_x + 40, self.y + 20

    def handle_collision(self, group, other):
        if group == 'boss:arrow' and not self.damaged:  # 다른 Troll과는 독립적으로 처리
            self.damaged = True  # 충돌 상태로 설정
            if self.hp > 0:  # HP 감소
                self.hit_sound.play()
                self.hp -= 1
            if self.hp <= 0:
                self.state_machine.add_event(('DIE', 0))
        elif group == 'King:boss':
            pass
