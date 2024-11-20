from direction import Direction
import pygame

class Moveable:
    def __init__(self, speed, image: pygame.Surface, x, y: int):
        self.speed = speed
        self.image = image
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