from .direction import Direction
from .assets import get_image, get_image_metadata
import pygame

class Renderable:
    def __init__(self, name: str):
        self.__image = get_image(name)
        image_metadata = get_image_metadata(name)
        self.__direction = self.__init_current_direction(image_metadata['direction'])
            
    def get_image(self) -> pygame.Surface:
        return self.__image

    def set_image(self, new_direction: Direction = None):
        if new_direction is None:
            return
        if self.__direction == new_direction:
            return

        current_angle = self.__calculate_angle(self.__direction)
        target_angle = self.__calculate_angle(new_direction)
        relative_angle = self.__calculate_relative_angle(current_angle, 
                                                         target_angle)
    
        self.__image = pygame.transform.rotate(self.__image, relative_angle)
        self.__direction = new_direction

    def get_direction(self) -> Direction:
        return self.__direction

    def __init_current_direction(self, direction: str) -> Direction:
        match direction:
            case "up": return Direction.UP
            case "right": return Direction.RIGHT
            case "down": return Direction.DOWN
            case "left": return Direction.LEFT
            case _: raise ValueError(f"Invalid direction: {direction}")
    
    def __calculate_angle(self, direction: Direction) -> int:
        match direction:
            case Direction.UP: return 0
            case Direction.LEFT: return 90
            case Direction.DOWN: return 180
            case Direction.RIGHT: return 270
            case _: raise ValueError(f"Invalid direction: {direction}")

    def __calculate_relative_angle(self, current_angle: int, target_angle: int) -> int:
        relative_angle = target_angle - current_angle
        return relative_angle