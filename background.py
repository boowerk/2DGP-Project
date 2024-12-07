from pico2d import load_image, load_music


class Background:
    hills = None
    rocks = None
    backdrop = None
    sky = None
    music = None

    def __init__(self, king):
        if Background.hills is None:
            Background.hills = load_image("backdrop_hills.png")

        if Background.rocks is None:
            Background.rocks = load_image("backdrop_rocks.png")

        if Background.backdrop is None:
            Background.backdrop = load_image("backdrop_canvas.png")

        if Background.sky is None:
            Background.sky = load_image("sky.png")

        if not Background.music:
            Background.music = load_music('Bloom.wav')
            Background.music.set_volume(10)
            Background.music.repeat_play()


        self.king = king
        self.hills_y = 420
        self.rocks_y = 440
        self.backdrop_y = 440
        self.image_width = 1792  # 배경 이미지의 너비
        self.screen_width = 800  # 화면 너비

    def draw(self):
        backdrop_offset = self.king.camera_x % self.image_width
        self.backdrop.draw(self.image_width - backdrop_offset, self.backdrop_y, self.image_width, 1000)
        self.backdrop.draw(-backdrop_offset, self.backdrop_y, self.image_width, 1000)

        # rocks: 1배속
        offset = self.king.camera_x % self.image_width
        self.sky.draw(self.image_width - offset, self.rocks_y, self.image_width, 328)
        self.sky.draw(-offset, self.rocks_y, self.image_width, 328)

        # rocks: 1배속
        rocks_offset = self.king.camera_x % self.image_width
        self.rocks.draw(self.image_width - rocks_offset, self.rocks_y, self.image_width, 328)
        self.rocks.draw(-rocks_offset + 200, self.rocks_y, self.image_width, 328)

        # hills: 2배속
        hills_offset = self.king.camera_x % self.image_width
        self.hills.draw(self.image_width - hills_offset, self.hills_y, self.image_width, 328)
        self.hills.draw(-hills_offset + 200, self.hills_y, self.image_width, 328)

    def update(self):
        pass
