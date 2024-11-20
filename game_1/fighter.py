import pygame
from bullet import Bullet, BULLET_WIDTH
from game_window import GAME_WINDOW
from base_dir import BASE_DIR
import os
from moveable import Moveable
from direction import Direction

# 加载战斗机图片 Load fighter image
FIGHTER_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "fighter_2.png")
FIGHTER_IMAGE = pygame.image.load(FIGHTER_IMAGE_PATH)
FIGHTER_WIDTH = 50
FIGHTER_HEIGHT = 50
FIGHTER_IMAGE = pygame.transform.scale(FIGHTER_IMAGE, (FIGHTER_WIDTH, FIGHTER_HEIGHT))

# 战斗机类 Fighter class
class Fighter(Moveable):
    def __init__(self, speed: int, x: int, y: int):
        super().__init__(speed, x, y)
        self.bullets: list[Bullet] = []

        self.right_boundary = GAME_WINDOW.get_width() - FIGHTER_WIDTH
        self.bottom_boundary = GAME_WINDOW.get_height() - FIGHTER_HEIGHT

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
        bullet_x = self.x + FIGHTER_WIDTH // 2 - BULLET_WIDTH // 2
        bullet_y = self.y
        bullet = Bullet(bullet_x, bullet_y)
        self.bullets.append(bullet)

    def draw(self):
        GAME_WINDOW.blit(FIGHTER_IMAGE, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()