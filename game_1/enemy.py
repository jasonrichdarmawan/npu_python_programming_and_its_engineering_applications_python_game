import random
from game_window import GAME_WINDOW, GAME_WINDOW_WIDTH
from assets import get_image, get_image_metadata

# 敌机类 Enemy aircraft
class Enemy:
    def __init__(self):
        self.image = get_image("enemy")
        self.image_metadata = get_image_metadata("enemy")
        self.x = random.randint(0, GAME_WINDOW_WIDTH - self.image_metadata["width"])
        self.y = random.randint(-200, - self.image_metadata["height"])
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self):
        GAME_WINDOW.blit(self.image, (self.x, self.y))