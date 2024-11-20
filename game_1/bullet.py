from game_window import GAME_WINDOW
from assets import get_image, get_image_metadata
from moveable import Moveable
from direction import Direction

# 子弹类 Bullet
class Bullet(Moveable):
    def __init__(self, speed, x, y):
        self.__image = get_image("bullet")
        self.__image_metadata = get_image_metadata("bullet")
        super().__init__(speed, self.__image_metadata["width"], self.__image_metadata["height"], x, y)

    def move(self, direction: Direction):
        super().move(direction)

    def draw(self):
        GAME_WINDOW.blit(self.__image, (self.x, self.y))