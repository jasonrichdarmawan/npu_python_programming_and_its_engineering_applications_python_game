from direction import Direction

class Moveable:
    def __init__(self, speed, width, height, x, y: int):
        self.speed = speed
        self.width = width
        self.height = height
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