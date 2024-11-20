from game_window import GAME_WINDOW
from assets import get_image, get_image_metadata
from moveable import Moveable
from direction import Direction

# 子弹类 Bullet
class Bullet(Moveable):
    def __init__(self, speed, direction, x, y):
        self.image = get_image("bullet")
        self.image_metadata = get_image_metadata("bullet")
        super().__init__(speed, self.image, x, y)
        self.direction = direction

    def move(self):
        super().move(self.direction)

    def draw(self):
        GAME_WINDOW.blit(self.__image, (self.x, self.y))