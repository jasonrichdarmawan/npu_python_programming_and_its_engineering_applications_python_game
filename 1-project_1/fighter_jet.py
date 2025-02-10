from bullet import Bullet
from game_window import GAME_WINDOW
from moveable import Moveable
from direction import Direction
from assets import get_image_metadata
from typing import Callable
from renderable import Renderable

# 战斗机类 Fighter Jet class
class FighterJet(Moveable, Renderable):
    def __init__(self, type: str, speed: int, x: int, y: int, bullets_capacity):    
        Moveable.__init__(self, speed, x, y)
        Renderable.__init__(self, type)

        self.__append_bullet_in_flight: Callable[[Bullet], None] = None
        self.__bullets_left = bullets_capacity

        image = self.get_image()
        self.__right_boundary = GAME_WINDOW.get_width() - image.get_width()
        self.__bottom_boundary = GAME_WINDOW.get_height() - image.get_height()

        self.__handle_boundaries()

    def set_append_bullet_in_flight(self, callback: Callable[[Bullet], None]):
        self.__append_bullet_in_flight = callback

    def get_right_boundary(self) -> int:
        return self.__right_boundary
    
    def get_bottom_boundary(self) -> int:
        return self.__bottom_boundary

    def move(self, direction: Direction):
        super().move(direction)
        super().set_image(direction)
        self.__handle_boundaries()

    def shoot(self):
        if self.__bullets_left < 0:
            return

        self.__bullets_left -= 1
        
        direction = self.get_direction()
        bullet_x, bullet_y = self.__calculate_bullet_position(self.get_direction())
        bullet = Bullet(10, direction, bullet_x, bullet_y)
        self.__append_bullet_in_flight(bullet)

    def __handle_boundaries(self):
        x, y = self.get_position()
        if x < 0:
            self.set_x(0)
        elif x > self.__right_boundary:
            self.set_x(self.__right_boundary)
        if y < 0:
            self.set_y(0)
        elif y > self.__bottom_boundary:
            self.set_y(self.__bottom_boundary)

    def __calculate_bullet_position(self, direction: Direction):
        fighter_jet_image = self.get_image()
        x, y = self.get_position()

        bullet_image_metadata = get_image_metadata("bullet")
        bullet_width = bullet_image_metadata["width"]
        bullet_height = bullet_image_metadata["height"]

        match direction:
            case Direction.UP:
                bullet_x = x + fighter_jet_image.get_width() // 2 - bullet_width // 2
                bullet_y = y - bullet_height
            case Direction.LEFT:
                bullet_x = x - bullet_width
                bullet_y = y + fighter_jet_image.get_height() // 2 - bullet_width // 2
            case Direction.DOWN:
                bullet_x = x + fighter_jet_image.get_width() // 2 - bullet_width // 2
                bullet_y = y + fighter_jet_image.get_height() + bullet_height
            case Direction.RIGHT:
                bullet_x = x + fighter_jet_image.get_height() + bullet_height
                bullet_y = y + fighter_jet_image.get_width() // 2 - bullet_width // 2
            case _: raise ValueError(f"Invalid direction: {direction}")

        return bullet_x, bullet_y