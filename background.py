from pico2d import load_image


class Background:
    hills = None
    rocks = None

    def __init__(self, king):
        if Background.hills == None:
            Background.hills = load_image("backdrop_hills.png")

        if Background.rocks == None:
            Background.rocks = load_image("backdrop_rocks.png")

        self.king = king

        pass

    def draw(self):
        self.hills.draw(0 - self.king.camera_x, 420, 1792, 328)
        pass

    def update(self):
        pass