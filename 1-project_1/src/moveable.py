from .direction import Direction

class Moveable:
    def __init__(self, speed: int, x: int, y: int):
        self.__speed = speed
        self.__x = x
        self.__y = y

    def get_position(self) -> tuple[int, int]:
        return self.__x, self.__y
    
    def set_x(self, x: int):
        self.__x = x
    
    def set_y(self, y: int):
        self.__y = y

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.__x -= self.__speed
        elif direction == Direction.RIGHT:
            self.__x += self.__speed
        elif direction == Direction.UP:
            self.__y -= self.__speed
        elif direction == Direction.DOWN:
            self.__y += self.__speed