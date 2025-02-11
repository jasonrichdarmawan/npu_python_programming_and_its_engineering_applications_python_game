from .direction import Direction
from .collidable import Collidable

# 子弹类 Bullet
class Bullet(Collidable):
    def __init__(self, speed: int, direction: Direction, x: int, y: int):
        Collidable.__init__(self, speed, x, y, "bullet")
        self.__current_direction = direction

    def move(self, direction: Direction = None):
        if direction is None:
            super().move(self.__current_direction)
            return

        super().move(direction)