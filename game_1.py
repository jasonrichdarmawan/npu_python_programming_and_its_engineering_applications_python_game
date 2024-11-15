# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 14:44:55 2024

@author: HP
"""

import pygame
import random

# 初始化Pygame Initializing Pygame
pygame.init()

# 游戏窗口大小 Game window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 颜色定义 Color definition
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 创建游戏窗口 Create game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Air Combat Game")

# 加载战斗机图片 Load fighter image
fighter_image = pygame.image.load("fighter_2.png")
fighter_width = 50
fighter_height = 50
fighter_image = pygame.transform.scale(fighter_image, (fighter_width, fighter_height))

# 加载敌机图片 Load enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_width = 30
enemy_height = 30
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# 加载子弹图片 Load bullet image
bullet_image = pygame.image.load("bullet.png")
bullet_width = 10
bullet_height = 20
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))

# 战斗机类 Fighter class
class Fighter:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2 - fighter_width // 2
        self.y = WINDOW_HEIGHT - fighter_height - 10
        self.speed = 5
        self.bullets = []

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > WINDOW_WIDTH - fighter_width:
            self.x = WINDOW_WIDTH - fighter_width

    def shoot(self):
        bullet = Bullet(self.x + fighter_width // 2 - bullet_width // 2, self.y)
        self.bullets.append(bullet)

    def draw(self):
        window.blit(fighter_image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()

# 子弹类 Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed

    def draw(self):
        window.blit(bullet_image, (self.x, self.y))

# 敌机类 Enemy aircraft
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH - enemy_width)
        self.y = random.randint(-200, -enemy_height)
        self.speed = 3

    def move(self):
        self.y += self.speed

    def draw(self):
        window.blit(enemy_image, (self.x, self.y))

# 创建战斗机对象 Create a fighter object
fighter = Fighter()
enemy_1 = Enemy()

# LEE
enemies = [enemy_1]
# LEE

# 游戏主循环 Main Game Loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(30)  # 设置帧率为60帧每秒 Set the frame rate to 60 frames per second
    window.fill(BLACK)

    # 处理事件 Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        fighter.move_left()
    if keys[pygame.K_RIGHT]:
        fighter.move_right()
    if keys[pygame.K_SPACE]:
        fighter.shoot()

    # 移动和绘制敌机 Moving and drawing enemy aircraft
    for enemy in enemies:
        enemy.move()
        enemy.draw()
        if enemy.y > WINDOW_HEIGHT:
            enemies.remove(enemy)
            new_enemy = Enemy()
            enemies.append(new_enemy)

    # 移动和绘制子弹 Moving and drawing bullets
    for bullet in fighter.bullets:
        bullet.move()
        bullet.draw()
        if bullet.y < 0:
            fighter.bullets.remove(bullet)

    # 检测碰撞 Detecting collisions
    for bullet in fighter.bullets:
        for enemy in enemies:
            if pygame.Rect(bullet.x, bullet.y, bullet_width, bullet_height).colliderect(
                pygame.Rect(enemy.x, enemy.y, enemy_width, enemy_height)
            ):
                fighter.bullets.remove(bullet)
                enemies.remove(enemy)

    # 绘制战斗机 Drawing fighter jets
    fighter.draw()

    # 更新屏幕 Update screen
    pygame.display.update()

# 退出游戏
pygame.quit()