import pygame
from bullet import Bullet, BULLET_WIDTH
from game_window import WINDOW
from base_dir import BASE_DIR
import os

# 加载战斗机图片 Load fighter image
FIGHTER_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "fighter_2.png")
FIGHTER_IMAGE = pygame.image.load(FIGHTER_IMAGE_PATH)
FIGHTER_WIDTH = 50
FIGHTER_HEIGHT = 50
FIGHTER_IMAGE = pygame.transform.scale(FIGHTER_IMAGE, (FIGHTER_WIDTH, FIGHTER_HEIGHT))

# 战斗机类 Fighter class
class Fighter:
    def __init__(self):
        self.x = WINDOW.get_width() // 2 - FIGHTER_WIDTH // 2
        self.y = WINDOW.get_height() - FIGHTER_HEIGHT - 10
        self.speed = 5
        self.bullets: list[Bullet] = []

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > WINDOW.get_width() - FIGHTER_WIDTH:
            self.x = WINDOW.get_width() - FIGHTER_WIDTH

    def shoot(self):
        bullet_x = self.x + FIGHTER_WIDTH // 2 - BULLET_WIDTH // 2
        bullet_y = self.y
        bullet = Bullet(bullet_x, bullet_y)
        self.bullets.append(bullet)

    def draw(self):
        WINDOW.blit(FIGHTER_IMAGE, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()