from bullet import Bullet
from game_window import GAME_WINDOW
from moveable import Moveable
from direction import Direction
from assets import get_image, get_image_metadata
from typing import Callable

# 战斗机类 Fighter Jet class
class FighterJet(Moveable):
    def __init__(self, type: str, speed: int, x: int, y: int, append_bullet_in_flight: Callable[[Moveable], None]):
        self.image = get_image(type)
        self.image_metadata = get_image_metadata(type)
    
        super().__init__(speed, self.image, x, y)

        self.append_bullet_in_flight = append_bullet_in_flight

        self.bullets_left = 10

        self.right_boundary = GAME_WINDOW.get_width() - self.image_metadata["width"]
        self.bottom_boundary = GAME_WINDOW.get_height() - self.image_metadata["height"]

        self.__check_boundaries()
    
    def __check_boundaries(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.right_boundary:
            self.x = self.right_boundary
        if self.y < 0:
            self.y = 0
        elif self.y > self.bottom_boundary:
            self.y = self.bottom_boundary

    def move(self, direction: Direction):
        super().move(direction)
        self.__check_boundaries()

    def shoot(self):
        if self.bullets_left < 0:
            return
        self.bullets_left -= 1
        
        bullet_image_metadata = get_image_metadata("bullet")
        bullet_width = bullet_image_metadata["width"]
        bullet_height = bullet_image_metadata["height"]

        bullet_x = self.x + self.image_metadata["width"] // 2 - bullet_width // 2
        bullet_y = self.y + self.image_metadata["height"] + bullet_height
        bullet = Bullet(10, Direction.UP, bullet_x, bullet_y)
        self.append_bullet_in_flight(bullet)