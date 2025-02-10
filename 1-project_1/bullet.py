from moveable import Moveable
from direction import Direction
from renderable import Renderable

# 子弹类 Bullet
class Bullet(Moveable, Renderable):
    def __init__(self, speed, direction, x, y):
        Moveable.__init__(self, speed, x, y)
        Renderable.__init__(self, "bullet")
        self.current_direction = direction

    def move(self, direction: Direction = None):
        if direction is None:
            super().move(self.current_direction)
            return

        super().move(direction)