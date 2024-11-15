# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 17:34:09 2024

@author: HP
"""

import pygame
import math
import random

# 初始化pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Battle Game")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 帧率设置
FPS = 60
clock = pygame.time.Clock()

# 坦克类
class Tank:
    def __init__(self, x, y, color, is_player=True):
        self.x = x
        self.y = y
        self.color = color
        self.is_player = is_player
        self.angle = 0
        self.bullets = []
        self.health = 100
        self.speed = 2
        self.reload_time = 0

    def draw(self):
        tank_body = [
            (self.x - 15, self.y - 10),
            (self.x + 15, self.y - 10),
            (self.x + 15, self.y + 10),
            (self.x - 15, self.y + 10)
        ]
        rotated_body = [self.rotate_point(point[0], point[1], self.x, self.y, self.angle) for point in tank_body]
        pygame.draw.polygon(screen, self.color, rotated_body)

        turret_center = (self.x + 15 * math.cos(math.radians(self.angle)), self.y + 15 * math.sin(math.radians(self.angle)))
        turret_end = (self.x + 30 * math.cos(math.radians(self.angle)), self.y + 30 * math.sin(math.radians(self.angle)))
        pygame.draw.line(screen, self.color, turret_center, turret_end, 3)

    def move_forward(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.keep_in_bounds()

    def rotate_left(self):
        self.angle -= 3

    def rotate_right(self):
        self.angle += 3

    def fire(self):
        if self.reload_time == 0:
            bullet = Bullet(self.x + 15 * math.cos(math.radians(self.angle)),
                            self.y + 15 * math.sin(math.radians(self.angle)), self.angle, self.is_player)
            self.bullets.append(bullet)
            self.reload_time = 30  # 模拟射击间隔

    def update(self):
        if self.reload_time > 0:
            self.reload_time -= 1
        for bullet in self.bullets:
            bullet.move()
            if not self.is_player and math.sqrt((bullet.x - player_tank.x) ** 2 + (bullet.y - player_tank.y) ** 2) < 20:
                player_tank.health -= 20
                self.bullets.remove(bullet)
            elif self.is_player and math.sqrt((bullet.x - enemy_tank.x) ** 2 + (bullet.y - enemy_tank.y) ** 2) < 20:
                enemy_tank.health -= 20
                self.bullets.remove(bullet)
            elif not (0 <= bullet.x <= WIDTH and 0 <= bullet.y <= HEIGHT):
                self.bullets.remove(bullet)

    def keep_in_bounds(self):
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT

    def rotate_point(self, px, py, ox, oy, angle):
        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
        return qx, qy

# 子弹类
class Bullet:
    def __init__(self, x, y, angle, is_player):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 5
        self.is_player = is_player

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

# 创建玩家坦克和敌人坦克
player_tank = Tank(100, 100, GREEN, True)
enemy_tank = Tank(700, 500, RED, False)

# 游戏主循环
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_tank.move_forward()
            elif event.key == pygame.K_LEFT:
                player_tank.rotate_left()
            elif event.key == pygame.K_RIGHT:
                player_tank.rotate_right()
            elif event.key == pygame.K_SPACE:
                player_tank.fire()

    screen.fill(BLACK)

    # 敌人坦克的人工智能逻辑
    if random.randint(0, 100) < 5:
        enemy_tank.fire()
    if random.randint(0, 100) < 30:
        if enemy_tank.x > player_tank.x:
            enemy_tank.rotate_left()
        else:
            enemy_tank.rotate_right()
    enemy_tank.move_forward()
    enemy_tank.update()

    player_tank.update()
    player_tank.draw()
    enemy_tank.draw()

    pygame.display.flip()

pygame.quit()