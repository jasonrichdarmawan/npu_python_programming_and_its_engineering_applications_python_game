from game_window import GAME_WINDOW
from base_dir import BASE_DIR
import pygame
import os

# 加载子弹图片 Load bullet image
BULLET_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "bullet.png")
BULLET_IMAGE = pygame.image.load(BULLET_IMAGE_PATH)
BULLET_WIDTH = 10
BULLET_HEIGHT = 20
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_HEIGHT))

# 子弹类 Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def draw(self):
        GAME_WINDOW.blit(BULLET_IMAGE, (self.x, self.y))