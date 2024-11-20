from game_window import GAME_WINDOW
from assets import get_image
from moveable import Moveable
from direction import Direction

# 子弹类 Bullet
class Bullet(Moveable):
    def __init__(self, speed, x, y):
        super().__init__(speed, x, y)
        self.__image = get_image("bullet")

    def move(self, direction: Direction):
        super().move(direction)

    def draw(self):
        GAME_WINDOW.blit(self.__image, (self.x, self.y))