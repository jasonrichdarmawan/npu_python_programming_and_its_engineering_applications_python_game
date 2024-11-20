from direction import Direction

class Moveable:
    def __init__(self, speed: int, x: int, y: int):
        self.speed = speed
        self.x = x
        self.y = y

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.x -= self.speed
        elif direction == Direction.RIGHT:
            self.x += self.speed
        elif direction == Direction.UP:
            self.y -= self.speed
        elif direction == Direction.DOWN:
            self.y += self.speed