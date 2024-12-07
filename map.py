from pico2d import load_image

class Map:
    grass_tile = None

    def __init__(self, king):
        if Map.grass_tile == None:
            Map.grass_tile = load_image('tiles.png')  
        self.image_width = 381  # 타일 한 개의 너비
        self.image_height = 96  # 타일 한 개의 높이
        self.king = king
        self.y = 225  # 바닥의 Y 좌표 (고정)

    def draw(self):
        # 카메라 위치에 따라 offset 계산
        offset = self.king.camera_x % self.image_width

        # 5 개의 타일을 이어서 그리기
        self.grass_tile.clip_draw(232, 0, 127, 32, self.image_width - offset, self.y, self.image_width, self.image_height)
        self.grass_tile.clip_draw(232, 0, 127, 32, self.image_width - offset + 381, self.y, self.image_width, self.image_height)
        self.grass_tile.clip_draw(232, 0, 127, 32, self.image_width - offset + 762, self.y, self.image_width, self.image_height)
        self.grass_tile.clip_draw(232, 0, 127, 32, -offset, self.y, self.image_width, self.image_height)
        self.grass_tile.clip_draw(232, 0, 127, 32, -offset + 381, self.y, self.image_width, self.image_height)

    def update(self):
        pass
