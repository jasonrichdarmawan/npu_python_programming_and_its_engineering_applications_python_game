from fighter_jet import FighterJet
from moveable import Moveable
import pygame

class GameEngine:
    def __init__(self, fighter_jet: list[FighterJet], enemies: list[FighterJet]):
        self.fighter_jet = fighter_jet
        self.enemies = enemies

    def check_collision(self, obj1: Moveable, obj2: Moveable):
        rect1 = pygame.Rect(obj1.x, obj1.y, obj1.image_metadata["width"], obj1.image_metadata["height"])
        rect2 = pygame.Rect(obj2.x, obj2.y, obj2.image_metadata["width"], obj2.image_metadata["height"])
        return rect1.colliderect(rect2)