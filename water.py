from pico2d import load_image


class Water:
    image = None

    def __init__(self, king):
        if Water.image is None:
            Water.image = load_image("water.png")  # 물 텍스처 로드

        self.king = king
        self.image_width = 1780  # 이미지의 실제 너비
        self.screen_width = 800  # 화면의 너비
        self.y_position = 80     # 물 이미지의 Y 위치

    def draw(self):
        # 카메라 위치에 따른 오프셋 계산
        offset = self.king.camera_x % self.image_width

        # 왼쪽과 오른쪽에 이미지를 반복적으로 그림
        self.image.opacify(0.8)
        self.image.draw(self.image_width - offset, self.y_position, self.image_width, 284)
        self.image.draw(-offset - 1, self.y_position, self.image_width, 284)

    def update(self):
        pass
