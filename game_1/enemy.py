import pygame
import random
from game_window import GAME_WINDOW, GAME_WINDOW_WIDTH
from base_dir import BASE_DIR
import os

# 加载敌机图片 Load enemy image
ENEMY_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "enemy.png")
ENEMY_IMAGE = pygame.image.load(ENEMY_IMAGE_PATH)
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

# 敌机类 Enemy aircraft
class Enemy:
    def __init__(self):
        self.x = random.randint(0, GAME_WINDOW_WIDTH - ENEMY_WIDTH)
        self.y = random.randint(-200, - ENEMY_HEIGHT)
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self):
        GAME_WINDOW.blit(ENEMY_IMAGE, (self.x, self.y))