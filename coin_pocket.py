from pico2d import load_image, load_font


class Coin_pocket:
    image = None
    font = None

    def __init__(self, king):
        if Coin_pocket.image == None:
            Coin_pocket.image = load_image('sack.png')
        if Coin_pocket.font is None:
            Coin_pocket.font = load_font('DeterminationSansK2.ttf', 24)  # 폰트 파일과 크기 설정
        self.king = king
        self.x, self.y = 750, 550
        self.frame = 0

        pass

    def update(self):
        if self.king.coin_count <= 0:
            self.frame = 0
        elif self.king.coin_count <= 3:
            self.frame = 1
        elif self.king.coin_count <= 6:
            self.frame = 2
        elif self.king.coin_count <= 9:
            self.frame = 3
        elif self.king.coin_count <= 12:
            self.frame = 4
        elif self.king.coin_count <= 15:
            self.frame = 5
        elif self.king.coin_count > 18:
            self.frame = 6
        pass

    def draw(self):
        text = f"Coin Count: {self.king.coin_count}"
        self.font.draw(650, 490, text, (255, 255, 255))

        self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y, 72, 64)
        pass